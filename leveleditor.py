import pyglet

import movement
import entities
import controls
import numbers
import display
import sprites
import worlds
import events
import maps
import ui

import cProfile
import sys


CURSOR = None
MAP = {}
MOUSE_BUTTONS = {1: 0, 4: 0}


def boot():
	entities.create_entity_group('cursor')
	entities.create_entity_group('tiles_foreground')
	entities.create_entity_group('effects')
	display.create_sprite_group('tiles_foreground')
	display.create_sprite_group('effects_foreground')
	display.create_sprite_group('ui_foreground')
	cursor()

def commands():
	global MAP
	
	if controls.key_pressed('s'):
		maps.save_map('test', MAP)
	
	elif controls.key_pressed('l'):
		MAP = maps.load_map('test')

@display.WINDOW.event
def on_mouse_press(x, y, button, modifiers):
	_x, _y = int(round(CURSOR['position'][0])), int(round(CURSOR['position'][1]))
	_chunk_key = get_chunk_key_at(int(round(CURSOR['position'][0])), int(round(CURSOR['position'][1])))
	
	MOUSE_BUTTONS[button] = 1
	
	if button == 1 and not MAP[_chunk_key]['solid']:
		_tile = entities.create_entity('tiles_foreground')
		sprites.register_entity(_tile, 'tiles_foreground', 'wall_full.png')
		movement.register_entity(_tile, x=(_x/100)*100, y=(_y/100)*100)
		_tile['sprite'].image.anchor_x = 0
		_tile['sprite'].image.anchor_y = 0
		
		MAP[_chunk_key]['solid'] = True
		MAP[_chunk_key]['tile'] = _tile['_id']
	elif button == 4 and MAP[_chunk_key]['solid']:
		MAP[_chunk_key]['solid'] = False
		entities.delete_entity(entities.get_entity(MAP[_chunk_key]['tile']))

@display.WINDOW.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
	display.CAMERA['next_zoom'] += .4*scroll_y
	
	display.CAMERA['next_center_on'][0] = numbers.interp(display.CAMERA['next_center_on'][0], CURSOR['position'][0], .5)
	display.CAMERA['next_center_on'][1] = numbers.interp(display.CAMERA['next_center_on'][1], CURSOR['position'][1], .5)

@display.WINDOW.event
def on_mouse_drag(x, y, dx, dy, button, modifiers):
	if button == 4:
		display.CAMERA['next_center_on'][0] -= dx*3
		display.CAMERA['next_center_on'][1] += dy*3

@display.WINDOW.event
def on_mouse_motion(x, y, dx, dy):
	entities.trigger_event(CURSOR, 'set_position', x=CURSOR['position'][0]+dx, y=CURSOR['position'][1]-dy)

def cursor():
	global CURSOR
	
	CURSOR = entities.create_entity(group='cursor')
	movement.register_entity(CURSOR, x=0, y=0)
	sprites.register_entity(CURSOR, 'ui_foreground', 'crosshair.png')


def window(dt):
	display.set_caption('%s - %ifps - %stps - %s' % ('Level Editor',
	                                                 round(display.get_fps()),
	                                                 entities.TICKS_PER_SECOND,
	                                                 len(entities.ENTITIES)))

def get_chunk_key_at(x, y):
	return '%s,%s' % ((x/100)*100, (y/100)*100)

def main():
	global MAP
	
	for x in range(10000/100):
		for y in range(10000/100):
			MAP['%s,%s' % (x*100, y*100)] = {'solid': False}
	
	events.register_event('boot', display.boot)
	events.register_event('boot', entities.boot)
	events.register_event('boot', worlds.create, world_name='game')
	events.register_event('boot', boot)
	events.register_event('boot', ui.boot)
	events.register_event('boot', controls.boot, display.get_window())
	events.register_event('load', display.load, level_editor=False)
	events.register_event('input', commands)
	events.register_event('loop', controls.loop)
	events.register_event('logic', worlds.logic)
	events.register_event('frame', window)
	events.register_event('shutdown', display.shutdown)
	
	events.trigger_event('boot')
	events.trigger_event('load')
	
	if display.RABBYT:
		while not display.WINDOW.has_exit:
			display.lib2d.step(pyglet.clock.tick())
			display.WINDOW.dispatch_events()
			display.WINDOW.dispatch_event('on_draw')
			display.WINDOW.flip()
	else:
		while not display.WINDOW.has_exit:
			events.trigger_event('loop')
			display.WINDOW.dispatch_events()
			display.WINDOW.dispatch_event('on_draw')
			display.WINDOW.flip()

if __name__ == '__main__':
	if '--debug' in sys.argv:
		cProfile.run('main()','profile.dat')
	else:
		main()
