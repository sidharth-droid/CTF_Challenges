import numpy as np
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
import os

def quantum_period_to_key(period_binary):
    """Convert the quantum period to encryption key"""
    period_str = str(period_binary)
    # Use period as seed for key derivation
    digest = hashes.Hash(hashes.SHA256())
    digest.update(period_str.encode())
    key = digest.finalize()
    return key

def encrypt_data(plaintext, key):
    """Encrypt using AES in CTR mode"""
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CTR(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return iv + ciphertext

def main():
    # The secret period from quantum circuit (this is what solvers must find)
    secret_period = 0b101101  # 45 in decimal
    
    # Flag to encrypt
    flag = b"CTF{Qu4ntum_B4ckd00r_1n_Pl41n_S1ght}" + b"\x00" * (256 - 38)  # Pad to 256 bytes
    
    # Generate key from quantum period
    key = quantum_period_to_key(secret_period)
    
    # Encrypt the flag
    encrypted_data = encrypt_data(flag, key)
    
    # Save encrypted file
    with open('encrypted_quantum.bin', 'wb') as f:
        f.write(encrypted_data)
    
    print("Encrypted file created!")
    print(f"Key (for verification): {key.hex()}")

if __name__ == "__main__":
    main()
