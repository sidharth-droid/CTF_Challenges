# Original flag
flag = "FLAG{Super_Hard_Rev_CTF}"

# XOR key
xor_key = 0x73

# Encrypt the flag
encrypted_flag = [ord(c) ^ xor_key for c in flag]

# Print the encrypted values in C array format
print("char encrypted_flag[] = {", ", ".join(f"0x{c:02X}" for c in encrypted_flag), "};")
