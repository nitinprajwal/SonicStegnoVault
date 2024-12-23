import numpy as np
import librosa
from typing import Dict, Any

def get_audio_features(y: np.ndarray, sr: int) -> Dict[str, Any]:
    """Extract comprehensive audio features"""
    if len(y) == 0:
        raise ValueError("Empty audio signal")
        
    features = {}
    
    # Basic features
    features['Duration (s)'] = len(y) / sr
    features['Sample Rate'] = sr
    features['Number of Samples'] = len(y)
    
    # Amplitude features
    features['Peak Amplitude'] = float(np.max(np.abs(y)))
    features['RMS Energy'] = float(np.sqrt(np.mean(y**2)))
    features['Dynamic Range (dB)'] = float(20 * np.log10(np.max(np.abs(y)) / (np.min(np.abs(y[y != 0])) + 1e-6)))
    
    # Spectral features
    spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    features['Mean Spectral Centroid'] = float(np.mean(spectral_centroids))
    features['Std Spectral Centroid'] = float(np.std(spectral_centroids))
    
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
    features['Mean Spectral Rolloff'] = float(np.mean(spectral_rolloff))
    
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
    features['Mean Spectral Bandwidth'] = float(np.mean(spectral_bandwidth))
    
    # Temporal features
    zero_crossings = librosa.zero_crossings(y)
    features['Zero Crossing Rate'] = float(sum(zero_crossings) / len(y))
    
    # Rhythm features
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    features['Tempo (BPM)'] = float(tempo)
    
    # MFCCs
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    for i in range(13):
        features[f'MFCC_{i+1}'] = float(np.mean(mfccs[i]))
    
    # Chroma features
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    features['Mean Chroma Energy'] = float(np.mean(chroma))
    
    return features

def get_audio_statistics(y: np.ndarray) -> Dict[str, float]:
    """Calculate statistical features of audio signal"""
    return {
        'Mean': float(np.mean(y)),
        'Std Dev': float(np.std(y)),
        'Skewness': float(float(np.mean(((y - np.mean(y))/np.std(y))**3))),
        'Kurtosis': float(float(np.mean(((y - np.mean(y))/np.std(y))**4))),
        'Median': float(np.median(y)),
        'Q1': float(np.percentile(y, 25)),
        'Q3': float(np.percentile(y, 75))
    }