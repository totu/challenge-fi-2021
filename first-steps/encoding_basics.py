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

