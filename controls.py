from pyglet.window import key

import display


KEYS = None


def boot(window):
    global KEYS
    
    KEYS = key.KeyStateHandler()
    window.push_handlers(KEYS)

def loop():
    # Check if the spacebar is currently pressed:
    if KEYS[key.SPACE]:
        pass

def key_pressed(char):
    return KEYS[ord(char)]
