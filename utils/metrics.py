import numpy as np
from skimage.metrics import peak_signal_noise_ratio, mean_squared_error

def calculate_psnr(original, modified):
    """Calculate Peak Signal-to-Noise Ratio between original and modified images"""
    return peak_signal_noise_ratio(original, modified)

def calculate_mse(original, modified):
    """Calculate Mean Squared Error between original and modified images"""
    return mean_squared_error(original, modified)

def calculate_embedding_capacity(image):
    """Calculate maximum embedding capacity in bytes"""
    return (image.shape[0] * image.shape[1] * 3) // 8  # 3 channels, 1 bit per channel