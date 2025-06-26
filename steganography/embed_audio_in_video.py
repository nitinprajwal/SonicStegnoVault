import cv2
import pickle
import base64
import numpy as np
from utils.error_handling import handle_size_mismatch

def embed_data_into_video(cover_video_path, data_tuple, output_path):
    """
    Embed arbitrary data (e.g., encrypted audio) into a cover video file using LSB steganography on frames.
    """
    # Serialize and encode payload
    data = pickle.dumps(data_tuple)
    data_b64 = base64.b64encode(data)
    bits = ''.join(format(b, '08b') for b in data_b64)
    # Prefix length header
    length_header = '{:032b}'.format(len(bits))
    full_bits = length_header + bits

    cap = cv2.VideoCapture(cover_video_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video file: {cover_video_path}")
    # Video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    capacity = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) * width * height * 3
    if len(full_bits) > capacity:
        handle_size_mismatch()

    bit_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Embed into frame
        for i in range(height):
            for j in range(width):
                for c in range(3):
                    if bit_idx < len(full_bits):
                        frame[i, j, c] = (int(frame[i, j, c]) & ~1) | int(full_bits[bit_idx])
                        bit_idx += 1
                    else:
                        break
                if bit_idx >= len(full_bits):
                    break
            if bit_idx >= len(full_bits):
                break
        out.write(frame)
    cap.release()
    out.release()
    if bit_idx < len(full_bits):
        handle_size_mismatch()
