import wave
import numpy as np

def compress_audio_numpy(input_file, output_file, compression_factor):
    try:
        # Open the input file
        with wave.open(input_file, 'rb') as wav_in:
            # Get the input audio parameters
            n_channels = wav_in.getnchannels()
            sampwidth = wav_in.getsampwidth()
            framerate = wav_in.getframerate()
            n_frames = wav_in.getnframes()
            
            # Read the audio data
            data = wav_in.readframes(n_frames)
            audio_data = np.frombuffer(data, dtype=np.int16)
            
            # Compress the audio data (reduce bit depth)
            # Adjust compression based on the compression factor
            compressed_data = (audio_data / compression_factor).astype(np.int8)
            
            # Create the output file
            with wave.open(output_file, 'wb') as wav_out:
                wav_out.setnchannels(n_channels)
                wav_out.setsampwidth(1)  # Reduced sample width to 8 bits
                wav_out.setframerate(framerate)
                wav_out.writeframes(compressed_data.tobytes())
                
        print("Audio compression completed successfully!")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")

# Usage
input_file = "audio.wav"
output_file = "compressed_audio.wav"

# Ask the user for the compression factor
compression_factor = int(input("Enter the compression factor (e.g., 256 for 8-bit): "))
compress_audio_numpy(input_file, output_file, compression_factor)
