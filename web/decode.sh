#!/usr/bin/env sh
CRT=$(openssl x509 -in server.crt -text -noout)
echo $CRT | rg -i flag
