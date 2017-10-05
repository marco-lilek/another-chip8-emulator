import pygame
import sys
import logging

from operator import xor
from time import sleep

logger = logging.getLogger(__name__)

class Screen:
  CANVAS_W = 64
  CANVAS_H = 32

  PS = 5 # pixel size

  BLACK = (0, 0, 0)
  WHITE = (255, 255, 255)

  def __init__(self):
    logger.info('initialized screen')
    pygame.init()
    self.screen = pygame.display.set_mode(
      (Screen.CANVAS_W * Screen.PS, Screen.CANVAS_H * Screen.PS))
    self.grid = []
    for x in xrange(Screen.CANVAS_W):
      col = []
      for y in xrange(Screen.CANVAS_H):
        col.append(0)
      self.grid.append(col)

  def writeByte(self, byte, x, y):
    numBits = 8
    collision = 0
    while numBits > 0:
      newVal = xor((byte >> (numBits - 1)) & 0x1, self.grid[x][y])

      collision = self.grid[x][y] and not newVal
      self.grid[x][y] = newVal
      x += 1
      if x == Screen.CANVAS_W:
        x = 0
      numBits -= 1
    return collision

  def redraw(self): # TODO: only update changed pixels
    self.screen.fill(Screen.BLACK)
    for x in xrange(Screen.CANVAS_W):
      for y in xrange(Screen.CANVAS_H):
        if self.grid[x][y]:
          pygame.draw.rect(self.screen, Screen.WHITE, 
            (x*Screen.PS, y*Screen.PS, Screen.PS, Screen.PS), 0)
    pygame.display.update()


  def writeSprite(self, sprite, x, y):
    collision = 0
    for b in xrange(len(sprite)):
      collision = self.writeByte(sprite[b], x, y) or collision
      y += 1
      if y == Screen.CANVAS_H:
        y = 0

    return int(collision)

  def dumpBytes(self):
    for y in xrange(Screen.CANVAS_H):
      for x in xrange(Screen.CANVAS_W):
        print self.grid[x][y],
      print('')

if __name__ == '__main__':
    screen = Screen()
    print screen.writeByte(0xff, 63, 0)
    print screen.writeByte(0xff, 0, 5)
    screen.dumpBytes()
    screen.redraw()