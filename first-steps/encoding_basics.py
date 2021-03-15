#!/usr/bin/env python3
import base64
b64 = "RkxBR3tMb29rc19yZWFsbHlfY3J5cHRpY19idXRfaXNfZWFzaWx5X3JldmVyc2VkfQ=="
print(base64.b64decode(b64))

rot13 = "SYNT{jryy_guvf_jnf_rnfl}"
known_first = "F"
chiper = ord(known_first) - ord(rot13[0]) 


anwser = []
for c in rot13:
    if ord(c) > ord("Z"):
        if c not in ["{", "}", "_"]:
            c = ord(c) - 13
            if c < ord("a"):
                c = c - ord("a") + ord("z") + 1
            c = chr(c)

    anwser.append(c)

print("".join(anwser))


binary = "1101 1011 10 001 000111 110010 0111 1 1 1001 110010 0111 000 000 1001 110010 0111 1 1 1001 110010 0111 1 1 1001 110010 0111 000 000 1001 110010 00 110 1011 0 11 1001 1011 1 110010 1011 10 0100 1 101 111 110010 000 01 110010 0 000 1001 110010 000 1101 110010 1 10 0101 1111 110010 000 0 1111 1 101"
binary = binary.split(" ")
print([int(x, 2) for x in binary])


# print("".join([chr(ord(x)+chiper) for x in rot13 if x not in ["{", "}", "_"]]))