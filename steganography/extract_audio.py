from PIL import Image
import numpy as np
import base64
import pickle

def extract_data_from_image(image_path):
    # Open the image
    image = Image.open(image_path)
    image_data = np.array(image)
    
    bits = ''
    for i in range(image_data.shape[0]):
        for j in range(image_data.shape[1]):
            pixel = image_data[i, j]
            for k in range(3):
                bits += str(pixel[k] & 1)
    
    # Convert bits to bytes
    data_bytes = int(bits, 2).to_bytes(len(bits) // 8, byteorder='big')
    
    # Decode from base64
    try:
        data_b64 = data_bytes.split(b'\x00')[0]  # Remove any padding zeros
        data = base64.b64decode(data_b64)
        data_tuple = pickle.loads(data)
    except Exception as e:
        print("Error during data extraction:", e)
        exit()

    return data_tuple