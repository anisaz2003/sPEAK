import time
import pyperclip
from pynput.keyboard import Controller, Key


class Paster:
    def __init__(self):
        self._kb = Controller()

    def paste(self, text: str):
        if not text:
            return
        pyperclip.copy(text)
        time.sleep(0.05)  # let clipboard settle
        self._kb.press(Key.ctrl)
        self._kb.press("v")
        self._kb.release("v")
        self._kb.release(Key.ctrl)
