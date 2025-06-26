import cv2
import pickle
import base64
import numpy as np
from utils.error_handling import handle_size_mismatch

def extract_data_from_video(stego_video_path):
    """
    Extract embedded data from a stego video file using LSB steganography on frames.
    """
    cap = cv2.VideoCapture(stego_video_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video file: {stego_video_path}")
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Extract bits
    bits = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        for i in range(height):
            for j in range(width):
                for c in range(3):
                    bits.append(str(int(frame[i, j, c]) & 1))
    cap.release()
    bit_str = ''.join(bits)
    if len(bit_str) < 32:
        handle_size_mismatch()
    length = int(bit_str[:32], 2)
    data_bits = bit_str[32:32 + length]
    if len(data_bits) < length:
        handle_size_mismatch()

    data_bytes = bytes(int(data_bits[i:i+8], 2) for i in range(0, length, 8))
    try:
        data_b64 = data_bytes
        data = base64.b64decode(data_b64)
        return pickle.loads(data)
    except Exception:
        handle_size_mismatch()
