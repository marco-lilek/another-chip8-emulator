#!/usr/bin/python

from operator import xor
from sprites import *
import logging
import random

log = logging.getLogger(__name__)
log.debug('test')

class OutOfMemException(Exception):
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)

class CPU:
  WORDSIZE = 2
  NUM_REG = 16
  MEM_SIZE = 0x1000

  def __init__(self, keyboard, screen):
    self.M = [0] * CPU.MEM_SIZE # 4096 bytes

    self.V = [0] * CPU.NUM_REG # general purpose 8 bit registers

    self.I = 0 # 16 bit register
    self.F = 0 # flag register
    self.DT = 0
    self.ST = 0

    self.SP = 0 # depth of the stack
    self.stack = [0] * 16
    self.PC = 0x200

    self.keyboard = keyboard
    self.screen = screen

  def load(self, filename):
    self._loadSprites()
    self._loadProgram(filename)

  def _loadSprites(self):
    loc = 0x000
    self.spritesLoc = []
    for sprite in SPRITE_DATA:
      self.spritesLoc.append(loc)
      for byte in sprite:
        self.M[loc] = byte
        loc += 1

  def _loadProgram(self, filename):
    f = open(filename, 'rb')
    byte = f.read(1)
    loc = 0x200
    while byte != '':
      self.M[loc] = ord(byte)
      loc += 1
      byte = f.read(1)
    f.close()

  def dumpMem(self):
    print('M {}'.format([hex(x) for x in self.M]))

  def dumpReg(self):
    print('V {}'.format(self.V))
    print('VF {}'.format(self.V[0xf]))
    print('I {}'.format(self.I))
    print('F {}'.format(self.F))
    print('DT {}'.format(self.DT))
    print('ST {}'.format(self.ST))
    print('SP {}'.format(self.SP))
    print('stack {}'.format(self.stack))
    print('PC {}'.format(self.PC))

  def runCycle(self):
    if self.PC+1 >= CPU.MEM_SIZE:
      raise OutOfMemException('outside mem bounds')

    instr = (self.M[self.PC] << 8) | self.M[self.PC+1]
    log.debug('{} {}'.format(self.PC, hex(instr)))
    self.PC += CPU.WORDSIZE

    opl = (instr >> 12) & 0xf
    op = ((instr >> 8) & 0xf0) | (instr & 0xf)
    opf = (instr & 0xff) | ((instr >> 4) & 0xf00)
    x = (instr >> 8) & 0xf
    y = (instr >> 4) & 0xf
    kk = instr & 0xff
    nnn = instr & 0xfff
    n = instr & 0xf

    if op == 0x00:
      #log.info('CLS')
      #self.screen.redraw()
      pass
    elif op == 0x0e:
      log.debug('RET')
      self.SP -= 1
      self.PC = self.stack[self.SP]
    elif opl == 0x1:
      log.debug('JP addr')
      self.PC = nnn
    elif opl == 0x2:
      log.debug('CALL addr')
      self.stack[self.SP] = self.PC
      self.SP += 1
      self.PC = nnn
    elif opl == 0x3:
      log.debug('SE Vx, byte')
      if self.V[x] == kk:
        self.PC += CPU.WORDSIZE
    elif opl == 0x4:
      log.debug('SNE Vx, byte')
      if self.V[x] != kk:
        self.PC += CPU.WORDSIZE
    elif opl == 0x5:
      log.debug('SE Vx, Vy')
      if self.V[x] == self.V[y]:
        self.PC += CPU.WORDSIZE
    elif opl == 0x6:
      log.debug('LD Vx, byte')
      self.V[x] = kk
    elif opl == 0x7:
      log.debug('ADD Vx, byte')
      self.V[x] += kk
      self.V[0xf] = int(self.V[x] > 0xff)
      self.V[x] &= 0xff
    elif op == 0x80:
      log.debug('LD Vx, Vy')
      self.V[x] = self.V[y]
    elif op == 0x81:
      log.debug('OR Vx, Vy')
      self.V[x] |= self.V[y]
    elif op == 0x82:
      log.debug('AND Vx, Vy')
      self.V[x] &= self.V[y]
    elif op == 0x83:
      log.debug('XOR Vx, Vy')
      self.V[x] = xor(self.V[x], self.V[y])
    elif op == 0x84:
      log.debug('ADD Vx, Vy')
      self.V[x] += self.V[y]
      self.V[0xf] = int(self.V[x] > 0xff)
      self.V[x] &= 0xff
    elif op == 0x85:
      log.debug('SUB Vx, Vy')
      self.V[0xf] = int(self.V[x] > self.V[y])
      self.V[x] -= self.V[y]

      if not self.V[0xf]:
        self.V[x] += 0x100
    elif op == 0x86:
      log.debug('SHR Vx {,Vy}')
      self.V[0xf] = int(self.V[x] & 0x1 == 0x1)
      self.V[x] = (self.V[x] >> 1) & 0xff
    elif op == 0x87:
      log.debug('SUBN Vx, Vy')
      self.V[0xf] = int(self.V[y] > self.V[x])
      self.V[y] -= self.V[x]

      if not self.V[0xf]:
        self.V[y] += 0x100
    elif op == 0x8e:
      log.debug('SHL Vx {,Vy}')
      self.V[0xf] = int(self.V[x] & 0x80 > 0) 
      self.V[x] = self.V[x] << 1
    elif op == 0x90:
      log.debug('SNE Vx, Vy')
      if self.V[x] != self.V[y]:
        self.PC += CPU.WORDSIZE
    elif opl == 0xa:
      log.debug('LD I, addr')
      self.I = nnn
    elif opl == 0xb:
      log.debug('JP V0, addr')
      self.PC = nnn + self.V[0]
    elif opl == 0xc:
      log.debug('RND Vx, byte')
      rnum = random.randint(0,0xff) # TODO random number gen
      self.V[x] = rnum & kk
    elif opl == 0xd:
      log.debug('DRW Vx, Vy, nibble')
      self.V[0xf] = self.screen.writeSprite(self.M[self.I:(self.I+n)], 
        self.V[x], self.V[y])
      self.screen.redraw()
    elif op == 0xee:
      log.debug('SKP Vx')
      if self.keyboard.checkKeyFromV(self.V[x]):
        self.PC += CPU.WORDSIZE
    elif op == 0xe1:
      log.debug('SKNP Vx')
      if not self.keyboard.checkKeyFromV(self.V[x]):
        self.PC += CPU.WORDSIZE
    elif opf == 0xf07:
      log.debug('LD Vx, DT')
      self.V[x] = self.DT
    elif opf == 0xf0a:
      log.debug('LD Vx, K')
      self.V[x] = self.keyboard.waitForKeyPress(self.V[x])
    elif opf == 0xf15:
      log.debug('LD DT, Vx')
      self.DT = self.V[x]
    elif opf == 0xf18:
      log.debug('LD ST, Vx')
      self.ST = self.V[x]
    elif opf == 0xf1e:
      log.debug('ADD I, Vx')
      self.I += self.V[x]
    elif opf == 0xf29:
      log.debug('LD F, Vx')
      self.I = self.spritesLoc[self.V[x]]
    elif opf == 0xf33:
      log.debug('LD B, Vx')
      self.M[self.I] = self.V[x] // 100 % 10
      self.M[self.I+1] = self.V[x] // 10 % 10 
      self.M[self.I+2] = self.V[x] % 10
    elif opf == 0xf55:
      log.debug('LD [I], Vx')
      for i in range(x+1):
        self.M[self.I+i] = self.V[i]
    elif opf == 0xf65:
      log.debug('LD Vx, [I]')
      for i in range(x+1):
        self.V[i] = self.M[self.I+i]
    else:
      raise Exception('unrecogined instruction {} {}'.format(hex(instr), bin(instr)))
