#!/usr/bin/env python3

# Plaintexts
p1 = b"Dispose of all evidence immediately after use."
p2 = b"Used an invisble material"
p3 = b"FLAG{ReusedKeysAreBadNews}"

# Pad (47 bytes)
pad = b"TopSecretKey1234567890RepeatedToFitLengthOf47Bytes!"

# Encrypt: ci = pi XOR pad
c1 = bytes(x ^ y for x, y in zip(p1, pad))
c2 = bytes(x ^ y for x, y in zip(p2, pad))
c3 = bytes(x ^ y for x, y in zip(p3, pad))

# Save to files
with open("c1", "wb") as f:
    f.write(c1)
with open("c2", "wb") as f:
    f.write(c2)
with open("c3", "wb") as f:
    f.write(c3)
with open("p2", "wb") as f:
    f.write(p2)