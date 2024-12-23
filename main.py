from encryption.key_generation import generate_keys
from encryption.encrypt_audio import encrypt_audio
from encryption.decrypt_audio import decrypt_audio
from steganography.embed_audio import embed_data_into_image
from steganography.extract_audio import extract_data_from_image
from utils.graph_generator import plot_waveform

def main():
    choice = input("Do you want to perform encryption or decryption? (e/d): ").strip().lower()

    if choice == 'e':
        # Generate RSA keys
        generate_keys()

        # Read audio file
        with open('audio.wav', 'rb') as audio_file:
            audio_data = audio_file.read()

        # Encrypt audio data
        encrypted_aes_key, nonce, tag, ciphertext = encrypt_audio(audio_data)

        # Plot original audio waveform
        plot_waveform(audio_data, 'Original Audio Waveform')

        # Embed encrypted data into image
        embed_data_into_image('image.png', (encrypted_aes_key, nonce, tag, ciphertext), 'stego_image.png')

        print("Encryption completed and data embedded into stego_image.png")

    elif choice == 'd':
        # Extract encrypted data from image
        extracted_data = extract_data_from_image('stego_image.png')
        encrypted_aes_key_ext, nonce_ext, tag_ext, ciphertext_ext = extracted_data

        # Decrypt audio data
        decrypted_audio_data = decrypt_audio(encrypted_aes_key_ext, nonce_ext, tag_ext, ciphertext_ext)

        # Plot decrypted audio waveform
        plot_waveform(decrypted_audio_data, 'Decrypted Audio Waveform')

        # Save decrypted audio to file
        with open('decrypted_audio.wav', 'wb') as audio_file:
            audio_file.write(decrypted_audio_data)

        print("Decryption completed and audio saved to decrypted_audio.wav")

    else:
        print("Invalid choice. Please enter 'e' for encryption or 'd' for decryption.")

if __name__ == "__main__":
    main()