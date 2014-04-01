from pyglet.window import key

import display


KEYS_HELD = None
KEYS_PRESSED = {}
KEYS_RELEASED = []


def boot(window):
    global KEYS_HELD
    
    KEYS_HELD = key.KeyStateHandler()
    window.push_handlers(KEYS_HELD)

def loop():
    global KEYS_RELEASED
    
    _held = set(KEYS_HELD.keys())
    _pressed = set(KEYS_PRESSED.keys())
    _add_to_pressed = {key: 0 for key in _held-_pressed}
    
    KEYS_PRESSED.update(_add_to_pressed)
    
    for char in KEYS_PRESSED:
        _pressed_for_frames = (KEYS_PRESSED[char]+1) * KEYS_HELD.get(char)
        
        if not _pressed_for_frames and KEYS_PRESSED[char]:
            KEYS_RELEASED.append(char)
        
        KEYS_PRESSED[char] = _pressed_for_frames
    
    #TODO: Fire input event here
    if key_pressed(' '):
        display.set_tps(60)
        
        print 'press'
    elif key_held(' '):
        print 'held'
    elif key_released(' '):
        print 'release'
    
    KEYS_RELEASED = []

def key_pressed(char):
    return KEYS_PRESSED.get(ord(char)) == 1

def key_released(char):
    return ord(char) in KEYS_RELEASED

def key_held(char):
    return KEYS_HELD.get(ord(char))