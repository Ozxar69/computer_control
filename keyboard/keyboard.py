from time import sleep

from pynput.keyboard import Controller, Key


def play_pause():
    keyboard = Controller()
    sleep(0.3)
    keyboard.press(Key.space)
    keyboard.release(Key.space)
    return True
