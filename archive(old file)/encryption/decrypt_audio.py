import rsa
from Crypto.Cipher import AES

def decrypt_audio(encrypted_aes_key, nonce, tag, ciphertext):
    # Decrypt AES key with RSA
    with open('private.pem', 'rb') as priv_file:
        private_key = rsa.PrivateKey.load_pkcs1(priv_file.read())
    aes_key = rsa.decrypt(encrypted_aes_key, private_key)

    # Decrypt audio data with AES
    cipher = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
    audio_data = cipher.decrypt_and_verify(ciphertext, tag)

    return audio_data