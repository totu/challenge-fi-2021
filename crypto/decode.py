#!/usr/bin/env python3

data = []
mask = 255
with open("asd", "rb") as filu:
    while byte := filu.read(1):
        data.append(int(byte.hex(), 16))

out = []
a = [chr(x ^ 0xa5 ^ mask) for x in data[1::2]]
b = [chr(x ^ mask) for x in data[::2]]
for x in zip(a,b):
    out.append(x[0])
    out.append(x[1])
print("".join(out))


