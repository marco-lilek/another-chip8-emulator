from pynput.keyboard import Key, Listener, KeyCode
from threading import Condition
import logging

logger = logging.getLogger(__name__)

class Keyboard:
  NUM_KEYS = 16 #TODO: dont hardcode
  KEYS = {
    0x0: 'x',
    0x1: '1',
    0x2: '2',
    0x3: '3',
    0x4: 'q',
    0x5: 'w',
    0x6: 'e',
    0x7: 'a',
    0x8: 's',
    0x9: 'd',
    0xa: 'z',
    0xb: 'c',
    0xc: '4',
    0xd: 'r',
    0xe: 'f',
    0xf: 'v'
  }

  KEYMAP = {}
  for k,v in KEYS.items():
    KEYMAP[KeyCode(char=v)] = k

  def __init__(self):
    logger.info('initialized keyboard')
    self.keyState = [False] * Keyboard.NUM_KEYS
    self.listener = Listener(on_press=self._onPress, on_release=self._onRelease)
    self.listener.__enter__()
    self.keyPressCV = Condition()
    self.waitForKey = False
    self.lastPressedKey = None


  def dumpKeystate(self):
    print('keyboard {}'.format([int(x) for x in self.keyState]))

  def _onPress(self, key):
    logger.debug('{0} pressed'.format(key))
    if key in Keyboard.KEYMAP:
      self.keyPressCV.acquire()
      if self.waitForKey:
        self.keyPressCV.notify()
        self.waitForKey = False
        self.lastPressedKey = key
      self.keyState[Keyboard.KEYMAP[key]] = True
      self.keyPressCV.release()

  def _onRelease(self, key):
    logger.debug('{0} released'.format(key))
    if key in Keyboard.KEYMAP:
      self.keyState[Keyboard.KEYMAP[key]] = False

  def checkKey(self, key):
    return self.keyState[Keyboard.KEYMAP[KeyCode(char=key)]]

  def checkKeyFromV(self, v):
    return self.checkKey(Keyboard.KEYS[v])

  def waitForKeyPress(self, v):
    self.keyPressCV.acquire()
    self.waitForKey = True
    self.keyPressCV.wait()
    keycode = Keyboard.KEYMAP[self.lastPressedKey]
    self.keyPressCV.release()
    return keycode
    
if __name__ == '__main__':
  k = Keyboard()
  while True:
    pass

'''
  KEYMAP = {
    KeyCode(char='a'):0x1,
    KeyCode(char='s'):0x2,
    KeyCode(char='d'):0x3,
    KeyCode(char='f'):0xc,
    KeyCode(char='z'):0x4,
    KeyCode(char='x'):0x5,
    KeyCode(char='c'):0x6,
    KeyCode(char='v'):0xd,
    KeyCode(char='j'):0x7,
    KeyCode(char='k'):0x8,
    KeyCode(char='l'):0x9,
    KeyCode(char=';'):0xe,
    KeyCode(char='n'):0xa,
    KeyCode(char='m'):0x0,
    KeyCode(char=','):0xb,
    KeyCode(char='.'):0xf
  }
'''
