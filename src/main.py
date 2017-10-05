#!/usr/bin/python

from cpu import *
from keyboard import *
from screen import *
import logging
import sys
from time import sleep

import traceback

import random
random.seed()

logging.basicConfig(level=logging.DEBUG)

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

      sleep(0.001)
      cpu.DT -= 1
      cpu.ST -= 1

      if cpu.DT < 0:
        cpu.DT = 0
      if cpu.ST < 0:
        cpu.ST = 0
  except OutOfMemException:
    pass
  except IndexError:
    traceback.print_exc()
    cpu.dumpReg()


  #cpu.dumpMem()
  #cpu.dumpReg()
  #keyboard.dumpKeystate()
  #screen.dumpBytes()
