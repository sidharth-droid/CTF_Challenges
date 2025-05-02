import wave

# Flag to hide
flag = "FLAG{Hidden_In_SounD}"

# Convert flag to binary
flag_bin = ''.join(format(ord(c), '08b') for c in flag)

# Open audio file (carrier) in read mode
input_audio = "input.wav"
output_audio = "stego.wav"

with wave.open(input_audio, "rb") as audio:
    params = audio.getparams()
    frames = bytearray(audio.readframes(audio.getnframes()))

# Modify LSB of each byte to encode the flag
for i in range(len(flag_bin)):
    frames[i] = (frames[i] & 0xFE) | int(flag_bin[i])

# Save new stego audio file
with wave.open(output_audio, "wb") as stego_audio:
    stego_audio.setparams(params)
    stego_audio.writeframes(frames)

print(f"Stego file created: {output_audio}")
