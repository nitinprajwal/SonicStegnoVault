import wave
import pickle
import base64
import numpy as np
from utils.error_handling import handle_size_mismatch

def embed_data_into_audio(cover_audio_path, data_tuple, output_path):
    """
    Embed arbitrary data (e.g., encrypted audio) into a cover WAV audio file using LSB steganography.
    """
    # Serialize and encode the payload
    data = pickle.dumps(data_tuple)
    data_b64 = base64.b64encode(data)
    bits = ''.join(format(byte, '08b') for byte in data_b64)
    # Prefix length of payload bits as 32-bit header
    length_header = '{:032b}'.format(len(bits))
    full_bits = length_header + bits

    # Read cover audio
    with wave.open(cover_audio_path, 'rb') as audio:
        params = audio.getparams()
        frames = audio.readframes(params.nframes)
    # Convert to numpy array
    sampwidth = params.sampwidth
    dtype = np.int16 if sampwidth == 2 else np.uint8
    samples = np.frombuffer(frames, dtype=dtype)

    # Check capacity
    if len(full_bits) > samples.size:
        handle_size_mismatch()

    # Embed bits into LSB of samples
    modified = samples.copy()
    for idx, bit in enumerate(full_bits):
        modified[idx] = (int(modified[idx]) & ~1) | int(bit)

    # Write stego audio
    stego_frames = modified.tobytes()
    with wave.open(output_path, 'wb') as out:
        out.setparams(params)
        out.writeframes(stego_frames)
