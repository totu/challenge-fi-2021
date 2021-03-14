#!/usr/bin/env python3

challenge = "DJ?EyPMRU_qFcpc0.0/{"
print("".join([chr(ord(x) + 2) for x in challenge]))

challenge = "OEHNrMljfdy`elE`blHY{ft"
print("".join([chr(ord(x) ^ 9) for x in challenge]))
