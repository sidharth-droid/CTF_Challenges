# create_challenge4_working.py
import numpy as np
from PIL import Image
import random

def generate_lwe_instance(n=64, q=3329):  # Reduced size for solvability
    """Generate Learning With Errors parameters"""
    A = np.random.randint(0, q, (n, n))
    s = np.random.randint(0, q, n)  # Secret key
    e = np.random.normal(0, 1, n).astype(int)  # Smaller error
    b = (A @ s + e) % q
    return A, b, s, e

def embed_lwe_in_dct(image_array, A, b, q=3329):
    """Embed LWE instance in DCT coefficients"""
    from scipy.fftpack import dct, idct
    
    # Work on green channel
    dct_coeffs = dct(dct(image_array[:,:,1].astype(float), axis=0), axis=1)
    
    h, w = dct_coeffs.shape
    mid_freq = dct_coeffs[h//4:3*h//4, w//4:3*w//4].flatten()
    
    scale_factor = 0.001
    
    # Embed A matrix and b vector
    lwe_data = np.concatenate([A.flatten(), b])
    
    for i in range(min(len(lwe_data), len(mid_freq))):
        embedded_value = mid_freq[i] + (lwe_data[i] % 100) * scale_factor * random.choice([-1, 1])
        mid_freq[i] = embedded_value
    
    embedded_block = mid_freq.reshape((h//2, w//2))
    dct_coeffs[h//4:3*h//4, w//4:3*w//4] = embedded_block
    
    # Inverse DCT
    reconstructed = idct(idct(dct_coeffs, axis=0), axis=1)
    image_array[:,:,1] = np.clip(reconstructed, 0, 255).astype(np.uint8)
    
    return image_array

def encrypt_flag(flag, s):
    """Simple XOR encryption using secret key"""
    flag_bytes = flag.encode()
    key = sum(s) % 256
    
    encrypted = bytes(byte ^ key for byte in flag_bytes)
    return encrypted

def create_challenge_image():
    # Generate random noise image (smaller for testing)
    width, height = 512, 512
    image_array = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
    
    # Generate LWE instance (smaller for solvability)
    A, b, s, e = generate_lwe_instance(n=64)
    
    secret_sum = sum(s) % 256
    print(f"Secret key sum: {secret_sum}")
    
    # Embed LWE in image
    embedded_image = embed_lwe_in_dct(image_array.copy(), A, b)
    
    # Encrypt flag
    flag = "CTF{L4tt1c3_St3g0_1s_Qu4ntum_S4f3}"
    encrypted_flag = encrypt_flag(flag, s)
    
    print(f"Flag: {flag}")
    print(f"Encrypted flag: {encrypted_flag.hex()}")
    
    # Embed encrypted flag at the beginning of blue channel LSBs
    encrypted_bits = []
    for byte in encrypted_flag:
        for bit in range(8):
            encrypted_bits.append((byte >> bit) & 1)
    
    # Embed at fixed position (beginning)
    for i, bit in enumerate(encrypted_bits):
        if i < embedded_image[:,:,2].size:
            y = i // width
            x = i % width
            embedded_image[y, x, 2] = (embedded_image[y, x, 2] & 0xFE) | bit
    
    # Add padding zeros after the flag
    flag_end = len(encrypted_bits)
    for i in range(flag_end, flag_end + 1000):  # Add some padding
        if i < embedded_image[:,:,2].size:
            y = i // width
            x = i % width
            embedded_image[y, x, 2] = embedded_image[y, x, 2] & 0xFE  # Set to 0
    
    # Save the image
    img = Image.fromarray(embedded_image)
    img.save('quantum_image.png')
    
    print("Challenge image created: quantum_image.png")
    print(f"Flag starts at byte offset: 0")
    print(f"Flag length: {len(encrypted_flag)} bytes")
    
    return s, secret_sum

def create_readme():
    readme = """Quantum-Resistant Steganography Challenge

This image contains a message hidden using quantum-resistant steganography. 
The algorithm uses Learning With Errors (LWE) lattice-based cryptography 
to embed information in the frequency domain.

The implementation uses DCT coefficients in the chroma channels to hide 
an LWE instance. You'll need to:

1. Extract the LWE problem from the frequency domain
2. Solve the LWE instance to recover the secret key
3. Use the secret key to decrypt the flag embedded in spatial domain LSBs

This steganography method is theoretically quantum-resistant due to the 
hardness of the LWE problem.

Good luck!
"""
    with open('readme.txt', 'w') as f:
        f.write(readme)

if __name__ == "__main__":
    secret_key, secret_sum = create_challenge_image()
    create_readme()
    
    # Save secret for verification (admin only)
    with open('admin_secret.txt', 'w') as f:
        f.write(f"Secret sum: {secret_sum}\n")
        f.write(f"Secret key: {','.join(map(str, secret_key))}\n")
        f.write(f"Expected flag: CTF{{L4tt1c3_St3g0_1s_Qu4ntum_S4f3}}\n")
    
    print("Challenge files created successfully!")
    print(f"Admin secret saved to admin_secret.txt")
