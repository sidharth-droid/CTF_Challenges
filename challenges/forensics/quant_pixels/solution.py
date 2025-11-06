# solution_challenge4_fixed.py
import numpy as np
from PIL import Image
from scipy.fftpack import dct, idct
import struct

def extract_lwe_from_dct(image_array, n=128, q=3329):
    """Extract LWE instance from DCT coefficients"""
    # Convert to YCbCr and extract from chroma channels
    dct_coeffs = dct(dct(image_array[:,:,1].astype(float), axis=0), axis=1)
    
    h, w = dct_coeffs.shape
    mid_freq = dct_coeffs[h//4:3*h//4, w//4:3*w//4].flatten()
    
    # Extract LWE values from fractional parts
    scale_factor = 0.001
    extracted_data = []
    
    for i in range(n*n + n):  # A is n*n, b is n
        # Extract the embedded value from fractional part
        fractional = abs(mid_freq[i] - round(mid_freq[i]))
        extracted_value = int(round(fractional / scale_factor)) % 100
        extracted_data.append(extracted_value)
    
    # Reshape into A and b
    A = np.array(extracted_data[:n*n]).reshape((n, n))
    b = np.array(extracted_data[n*n:])
    
    return A, b

def gram_schmidt(A):
    """Gram-Schmidt orthogonalization for lattice reduction"""
    m, n = A.shape
    Q = np.zeros((m, n))
    R = np.zeros((n, n))
    
    for j in range(n):
        v = A[:, j].astype(float)
        for i in range(j):
            R[i, j] = np.dot(Q[:, i], A[:, j])
            v = v - R[i, j] * Q[:, i]
        R[j, j] = np.linalg.norm(v)
        Q[:, j] = v / R[j, j]
    
    return Q, R

def babai_nearest_plane(A, b, q=3329):
    """Babai's nearest plane algorithm for CVP"""
    Q, R = gram_schmidt(A)
    
    # Solve in the orthogonal basis
    y = np.linalg.lstsq(Q, b, rcond=None)[0]
    
    # Round to nearest integer (nearest plane)
    s_approx = np.round(y).astype(int) % q
    
    return s_approx

def extract_lsb_flag(image_array):
    """Extract flag from LSB of blue channel"""
    height, width = image_array.shape[:2]
    
    extracted_bytes = []
    current_byte = 0
    bit_count = 0
    
    # Extract all LSBs sequentially
    for y in range(height):
        for x in range(width):
            lsb = image_array[y, x, 2] & 1
            current_byte = (current_byte >> 1) | (lsb << 7)
            bit_count += 1
            
            if bit_count == 8:
                extracted_bytes.append(current_byte)
                current_byte = 0
                bit_count = 0
    
    return bytes(extracted_bytes)

def decrypt_flag(encrypted_bytes, s):
    """Decrypt flag using recovered secret key"""
    key = sum(s) % 256
    print(f"Using decryption key: {key}")
    
    # Simple XOR decryption
    decrypted = bytes(byte ^ key for byte in encrypted_bytes)
    return decrypted

def find_flag_in_data(data):
    """Find CTF flag pattern in decrypted data"""
    # Try to find CTF{ pattern
    data_str = data.decode('latin-1', errors='ignore')
    
    start = data_str.find('CTF{')
    if start != -1:
        end = data_str.find('}', start)
        if end != -1:
            return data_str[start:end+1]
    
    # Try hex decoding
    try:
        hex_str = data.hex()
        # Look for CTF in hex (435446)
        if '435446' in hex_str:
            idx = hex_str.find('435446')
            potential = bytes.fromhex(hex_str[idx:idx+100])
            return potential.decode('latin-1', errors='ignore')
    except:
        pass
    
    return None

def solve():
    # Load the image
    print("Loading image...")
    img = Image.open('quantum_image.png')
    img_array = np.array(img)
    
    print("Step 1: Extracting LWE instance from DCT coefficients...")
    A, b = extract_lwe_from_dct(img_array)
    
    print(f"A shape: {A.shape}, b shape: {b.shape}")
    
    print("Step 2: Solving LWE using Babai's nearest plane...")
    s_recovered = babai_nearest_plane(A, b)
    
    print(f"Recovered secret key sum: {sum(s_recovered)}")
    
    print("Step 3: Extracting encrypted flag from spatial domain...")
    encrypted_flag_data = extract_lsb_flag(img_array)
    
    print(f"Total extracted data length: {len(encrypted_flag_data)} bytes")
    
    print("Step 4: Searching for encrypted flag...")
    # The flag might be at different positions, try different offsets
    flag_found = False
    
    for offset in range(0, min(1000, len(encrypted_flag_data) - 100)):
        # Try different lengths around typical flag size
        for length in [50, 100, 150, 200]:
            encrypted_slice = encrypted_flag_data[offset:offset+length]
            
            # Try decryption with recovered key
            decrypted = decrypt_flag(encrypted_slice, s_recovered)
            
            # Check if we found the flag
            flag = find_flag_in_data(decrypted)
            if flag and 'CTF{' in flag:
                print(f"🎉 Flag found at offset {offset}: {flag}")
                flag_found = True
                break
        
        if flag_found:
            break
    
    if not flag_found:
        print("Flag not found with recovered key. The LWE solution might need improvement.")
        print("Trying brute force on key...")
        
        # Brute force the key space
        for key_guess in range(256):
            decrypted = bytes(byte ^ key_guess for byte in encrypted_flag_data[:200])
            flag = find_flag_in_data(decrypted)
            if flag and 'CTF{' in flag:
                print(f"Flag found with key {key_guess}: {flag}")
                flag_found = True
                break
    
    if not flag_found:
        print("Could not find flag. Debug info:")
        print(f"First 100 bytes of extracted data: {encrypted_flag_data[:100].hex()}")
        print(f"Recovered secret sum: {sum(s_recovered)}")
        
        # Try to find any readable text
        for key in [sum(s_recovered) % 256, 0, 255]:
            test_decrypt = bytes(byte ^ key for byte in encrypted_flag_data[:200])
            try:
                text = test_decrypt.decode('latin-1', errors='ignore')
                if any(c.isprintable() for c in text):
                    print(f"With key {key}: {text[:100]}")
            except:
                pass

if __name__ == "__main__":
    solve()
