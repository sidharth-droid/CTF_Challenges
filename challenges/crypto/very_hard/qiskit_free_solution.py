#!/usr/bin/env python3
"""
Simple solution that doesn't require Qiskit installation
Players can analyze the circuit manually and use this to decrypt
"""
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes

def manual_circuit_analysis():
    """
    Manual analysis of the quantum circuit
    The QASM file reveals the period through its structure
    """
    print("Manual QASM Circuit Analysis:")
    print("=" * 40)
    
    # Read and analyze the QASM file
    with open('quantum_circuit.qasm', 'r') as f:
        lines = f.readlines()
    
    print("Circuit structure:")
    for line in lines:
        line = line.strip()
        if line and not line.startswith('//') and not line.startswith('include'):
            print(f"  {line}")
    
    print("\nKey observations:")
    print("1. 6-qubit Simon's algorithm variant")
    print("2. Oracle uses CX gates that encode a secret period") 
    print("3. Added rz(pi/8) gates create interference patterns")
    print("4. The period is revealed in high-probability measurement states")
    
    # The secret period is encoded in the oracle structure
    # From analyzing the CX gate pattern:
    # q[0] affects both outputs -> contributes to period
    # q[1] affects output 0 -> contributes to period  
    # q[2] affects output 1 -> contributes to period
    # q[3] affects both outputs -> contributes to period
    
    # This forms the binary period: 101101
    secret_period = 0b101101
    
    print(f"\nDerived period from circuit analysis: {secret_period} (binary: {bin(secret_period)})")
    return secret_period

def quantum_period_to_key(period_binary):
    """Convert the quantum period to encryption key"""
    period_str = str(period_binary)
    digest = hashes.Hash(hashes.SHA256())
    digest.update(period_str.encode())
    return digest.finalize()

def decrypt_data(ciphertext, key):
    """Decrypt the data using AES-CTR"""
    iv = ciphertext[:16]
    encrypted = ciphertext[16:]
    
    cipher = Cipher(algorithms.AES(key), modes.CTR(iv))
    decryptor = cipher.decryptor()
    return decryptor.update(encrypted) + decryptor.finalize()

def main():
    print("Schrödinger's Cypher - Manual Solution")
    print("=" * 50)
    
    period = manual_circuit_analysis()
    key = quantum_period_to_key(period)
    
    print(f"Derived AES key: {key.hex()}")
    
    try:
        with open('encrypted_quantum.bin', 'rb') as f:
            encrypted_data = f.read()
        
        decrypted_data = decrypt_data(encrypted_data, key)
        flag = decrypted_data.rstrip(b'\x00')
        
        print(f"\n🎉 Success! Flag: {flag.decode()}")
        
    except FileNotFoundError:
        print("Error: encrypted_quantum.bin not found")
        print("Run the encryption script first to generate the challenge file")

if __name__ == "__main__":
    main()
