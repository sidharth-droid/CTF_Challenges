Quantum-Resistant Steganography Challenge

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
