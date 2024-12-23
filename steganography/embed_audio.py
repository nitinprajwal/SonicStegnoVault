from PIL import Image
import numpy as np
import base64
from utils.error_handling import handle_size_mismatch

def embed_data_into_image(image_path, data_tuple, output_path):
    import pickle
    data = pickle.dumps(data_tuple)
    data_b64 = base64.b64encode(data)
    data_bits = ''.join(format(byte, '08b') for byte in data_b64)
    
    image = Image.open(image_path)
    image_data = np.array(image)
    
    total_bits = image_data.size * 3
    if len(data_bits) > total_bits:
        handle_size_mismatch()
    
    data_index = 0
    for i in range(image_data.shape[0]):
        for j in range(image_data.shape[1]):
            pixel = image_data[i, j]
            for k in range(3):  # R, G, B channels
                if data_index < len(data_bits):
                    pixel[k] = (pixel[k] & 0b11111110) | int(data_bits[data_index])
                    data_index += 1
            image_data[i, j] = pixel
            if data_index >= len(data_bits):
                break
        if data_index >= len(data_bits):
            break
    
    encoded_image = Image.fromarray(image_data)
    
    # Save the image with maximum compression
    encoded_image.save(output_path, format='PNG', optimize=True)
