#!/usr/bin/python

from cpu import *
from keyboard import *
from screen import *
import logging
import sys
from time import sleep

import random
random.seed()

logging.basicConfig(level=logging.INFO)

LOOP60HZ = 5
if __name__ == '__main__':
  keyboard = Keyboard()
  screen = Screen()

  cpu = CPU(keyboard, screen)
  cpu.load(sys.argv[1])
  
  try:
    while True:
      for i in xrange(LOOP60HZ):
        cpu.runCycle()

      sleep(0.01)
      cpu.DT -= 1
      cpu.ST -= 1

      if cpu.DT < 0:
        cpu.DT = 0
      if cpu.ST < 0:
        cpu.ST = 0
  except OutOfMemException:
    pass

  #cpu.dumpMem()
  cpu.dumpReg()
  keyboard.dumpKeystate()
  #screen.dumpBytes()
