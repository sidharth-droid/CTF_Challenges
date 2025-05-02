import wave

# Extract hidden binary data from the stego audio file
def extract_flag(stego_audio):
    with wave.open(stego_audio, "rb") as audio:
        frames = bytearray(audio.readframes(audio.getnframes()))
    
    # Extract LSBs to retrieve the flag
    binary_flag = ''.join(str(frames[i] & 1) for i in range(8 * 25))  # Assuming 25-character flag
    flag = ''.join(chr(int(binary_flag[i:i+8], 2)) for i in range(0, len(binary_flag), 8))
    
    return flag

# Decode the flag
stego_audio = "stego.wav"
flag = extract_flag(stego_audio)
print(f"Extracted Flag: {flag}")
