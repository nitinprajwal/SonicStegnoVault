import wave
import pickle
import base64
import numpy as np

from utils.error_handling import handle_size_mismatch

def extract_data_from_audio(stego_audio_path):
    """
    Extract embedded data from a stego WAV audio file using LSB steganography.
    """
    with wave.open(stego_audio_path, 'rb') as audio:
        params = audio.getparams()
        frames = audio.readframes(params.nframes)
    sampwidth = params.sampwidth
    dtype = np.int16 if sampwidth == 2 else np.uint8
    samples = np.frombuffer(frames, dtype=dtype)

    # Extract bits
    bits = ''.join(str(int(sample) & 1) for sample in samples)
    # Get payload length
    if len(bits) < 32:
        handle_size_mismatch()
    length = int(bits[:32], 2)
    data_bits = bits[32:32 + length]

    # Convert bits to bytes
    data_bytes = bytes(int(data_bits[i:i+8], 2) for i in range(0, len(data_bits), 8))

    # Decode and deserialize
    try:
        data_b64 = data_bytes
        data = base64.b64decode(data_b64)
        return pickle.loads(data)
    except Exception:
        handle_size_mismatch()
