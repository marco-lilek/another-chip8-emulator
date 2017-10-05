#!/usr/bin/python

i = 1
with open('roms/BLINKY', 'rb') as f:
  while i < 10:
    hb = ord(f.read(1))
    lb = ord(f.read(1))
    print hex((hb >> 4) & 0xf),
    print hex(hb & 0xf),
    print hex((lb >> 4) & 0xf),
    print hex(lb & 0xf)
    i += 1

