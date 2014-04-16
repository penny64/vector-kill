from pyglet.window import key

import display
import worlds
import events

NUM_2 = key.NUM_2
NUM_4 = key.NUM_4
NUM_6 = key.NUM_6
NUM_8 = key.NUM_8
KEYS_HELD = None
KEYS_PRESSED = {}
KEYS_RELEASED = []


def boot(window):
    global KEYS_HELD
    
    KEYS_HELD = key.KeyStateHandler()
    
    window.push_handlers(KEYS_HELD)
    events.register_event('input', system_input)

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
    
    events.trigger_event('input')
    
    KEYS_RELEASED = []

def key_pressed_ord(char_ord):
    return KEYS_PRESSED.get(char_ord) == 1

def key_released_ord(char_ord):
    return char_ord in KEYS_RELEASED

def key_held_ord(char_ord):
    return KEYS_HELD.get(char_ord)

def key_pressed(char):
    return KEYS_PRESSED.get(ord(char)) == 1

def key_released(char):
    return ord(char) in KEYS_RELEASED

def key_held(char):
    return KEYS_HELD.get(ord(char))


def system_input():
    if key_pressed(' '):
        display.set_tps(60)
        display.reschedule(worlds.loop, 1/display.get_tps())
        
        print 'press'
    elif key_held(' '):
        print 'held'
    elif key_released(' '):
        print 'release'
    elif key_held('o'):
        display.CAMERA['next_zoom'] -= .1
    elif key_held('p'):
        display.CAMERA['next_zoom'] += .1
    elif key_held('['):
        display.CAMERA['next_zoom'] = 2.5
