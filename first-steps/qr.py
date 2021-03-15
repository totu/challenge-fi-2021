#!/usr/bin/env python3

from pyzbar.pyzbar import decode
from PIL import Image

qr = decode(Image.open("code.png"))[0]
# for i in range(0, len(l), 8):
#     a = []
#     for x in range(8):
#         a.append(l[i+x])
#     print(chr(int("".join(a), 2)))

MORSE_CODE_DICT = {
    ".-": "A",
    "-...": "B",
    "-.-.": "C",
    "-..": "D",
    ".": "E",
    "..-.": "F",
    "--.": "G",
    "....": "H",
    "..": "I",
    ".---": "J",
    "-.-": "K",
    ".-..": "L",
    "--": "M",
    "-.": "N",
    "---": "O",
    ".--.": "P",
    "--.-": "Q",
    ".-.": "R",
    "...": "S",
    "-": "T",
    "..-": "U",
    "...-": "V",
    ".--": "W",
    "-..-": "X",
    "-.--": "Y",
    "--..": "Z",
    ".----": "1",
    "..---": "2",
    "...--": "3",
    "....-": "4",
    ".....": "5",
    "-....": "6",
    "--...": "7",
    "---..": "8",
    "----.": "9",
    "-----": "0",
    "--..--": ",",
    ".-.-.-": ".",
    "..--..": "?",
    "-..-.": "/",
    "-....-": "-",
    "-.--.": "(",
    "-.--.-": ")",
}

morse = (
    " ".join([x for x in qr.data.decode().split(" ")])
    .replace("1", ".")
    .replace("0", "-")
)
print(morse)
asd = ""
for c in morse.split(" "):
    if c in MORSE_CODE_DICT:
        asd += MORSE_CODE_DICT[c]
    else:
        asd += c

print(asd)

print(qr.data)

# ints = [int(x[::-1], 2) for x in qr.data.decode().split(" ")]
# for i in range(255):
#     print(str(i) + ":" + "".join([chr(x+i) for x in ints]))
