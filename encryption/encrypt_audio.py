import rsa
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def encrypt_audio(audio_data):
    # Generate a random AES key
    aes_key = get_random_bytes(16)  # 128-bit key

    # Encrypt audio data with AES
    cipher = AES.new(aes_key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(audio_data)

    # Encrypt AES key with RSA
    with open('public.pem', 'rb') as pub_file:
        public_key = rsa.PublicKey.load_pkcs1(pub_file.read())
    encrypted_aes_key = rsa.encrypt(aes_key, public_key)

    return encrypted_aes_key, cipher.nonce, tag, ciphertext