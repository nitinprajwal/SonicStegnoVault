import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import seaborn as sns

def plot_waveform(audio_data, title):
    # Convert audio data to numpy array
    audio_array = np.frombuffer(audio_data, dtype=np.int16)
    
    # Create a figure with multiple subplots
    fig = plt.figure(figsize=(15, 10))
    
    # Set the style using a valid option
    sns.set_style("darkgrid")  # Using seaborn's built-in style instead
    
    # 1. Standard Waveform Plot
    ax1 = fig.add_subplot(221)
    time = np.arange(len(audio_array)) / len(audio_array)
    ax1.plot(time, audio_array, color='#2ecc71', alpha=0.7, linewidth=0.5)
    ax1.set_title('Waveform', color='#2c3e50', fontsize=10)
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Amplitude')
    
    # 2. Spectrogram
    ax2 = fig.add_subplot(222)
    frequencies, times, spectrogram = signal.spectrogram(audio_array, fs=44100)
    # Add small constant to avoid log of zero
    spectrogram = np.maximum(spectrogram, 1e-10)  # Avoid log(0)
    pcm = ax2.pcolormesh(times, frequencies, 10 * np.log10(spectrogram), 
                        cmap='magma', shading='gouraud')
    fig.colorbar(pcm, ax=ax2, label='Intensity [dB]')
    ax2.set_title('Spectrogram', color='#2c3e50', fontsize=10)
    ax2.set_ylabel('Frequency [Hz]')
    ax2.set_xlabel('Time [sec]')
    
    # 3. Amplitude Distribution
    ax3 = fig.add_subplot(223)
    sns.histplot(audio_array, bins=100, color='#e74c3c', ax=ax3)
    ax3.set_title('Amplitude Distribution', color='#2c3e50', fontsize=10)
    ax3.set_xlabel('Amplitude')
    ax3.set_ylabel('Count')
    
    # 4. Rolling RMS Energy
    ax4 = fig.add_subplot(224)
    frame_size = 2048
    hop_size = 512
    rms = []
    for i in range(0, len(audio_array)-frame_size, hop_size):
        frame = audio_array[i:i+frame_size]
        frame_squared = frame**2
        mean_squared = np.mean(frame_squared) if np.mean(frame_squared) > 0 else 1e-10
        rms.append(np.sqrt(mean_squared))
    ax4.plot(np.arange(len(rms))/len(rms), rms, color='#9b59b6', linewidth=1)
    ax4.set_title('Energy Over Time', color='#2c3e50', fontsize=10)
    ax4.set_xlabel('Time (normalized)')
    ax4.set_ylabel('RMS Energy')
    
    # Overall plot settings
    plt.suptitle(title, fontsize=14, color='#2c3e50', y=0.95)
    plt.tight_layout()
    plt.show()