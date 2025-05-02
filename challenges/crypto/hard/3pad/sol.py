

with open("c1", "br") as c1_f:
    c1 = c1_f.read()

with open("c2", "br") as c2_f:
    c2 = c2_f.read()

with open("c3", "br") as c3_f:
    c3 = c3_f.read()


with open("p2", "br") as p2_f:
    p2 = p2_f.read()



pad = bytes(x ^ y for x, y in zip(c2, p2))


p1 = bytes(x ^ y for x, y in zip(pad, c1))

print(p1.decode("ascii"))

print(p2.decode("ascii"))

p3 = bytes(x ^ y for x, y in zip(pad, c3))

flag = p3.decode("ascii")

print(flag)
