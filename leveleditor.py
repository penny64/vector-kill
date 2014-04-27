import pyglet

import movement
import entities
import controls
import display
import sprites
import worlds
import events
import ui

import cProfile
import sys


CURSOR = None
MAP = {}

def boot():
	entities.create_entity_group('cursor')
	entities.create_entity_group('tiles_foreground')
	display.create_sprite_group('tiles_foreground')
	display.create_sprite_group('ui_foreground')
	cursor()
	
	for x in range(10000/100):
		for y in range(10000/100):
			MAP['%s,%s' % (x*100, y*100)] = {'solid': False}

def loop(dt):
	display.set_clock_delta(dt)
	events.trigger_event('loop')

@display.WINDOW.event
def on_mouse_press(x, y, button, modifiers):
	_x = int(round(x*(display.CAMERA['zoom']/2)))
	_y = int(round(y*(display.CAMERA['zoom']/2)))
	_chunk_key = get_chunk_key_at(_x, _y)
	
	if button == 1:
		_tile = entities.create_entity('tiles_foreground')
		sprites.register_entity(_tile, 'tiles_foreground', 'laser.png')
		movement.register_entity(_tile, x=(_x/100)*100, y=(_y/100)*100)
		
		MAP[_chunk_key]['solid'] = True
		MAP[_chunk_key]['tile'] = _tile['_id']
	else:
		MAP[_chunk_key]['solid'] = False

@display.WINDOW.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
	display.CAMERA['next_zoom'] += .4*scroll_y

@display.WINDOW.event
def on_mouse_drag(x, y, dx, dy, button, modifiers):
	display.CAMERA['next_center_on'][0] -= dx*3
	display.CAMERA['next_center_on'][1] += dy*3

@display.WINDOW.event
def on_mouse_motion(x, y, dx, dy):
	pass
	#entities.trigger_event(CURSOR, 'set_position', x=x, y=-y*)

def cursor():
	global CURSOR
	
	#CURSOR = entities.create_entity(group='cursor')
	#movement.register_entity(CURSOR, x=0, y=0)
	#sprites.register_entity(CURSOR, 'ui_foreground', 'crosshair.png')


def window(dt):
	display.set_caption('%s - %ifps - %stps - %s' % ('Level Editor',
	                                                 round(display.get_fps()),
	                                                 entities.TICKS_PER_SECOND,
	                                                 len(entities.ENTITIES)))

def get_chunk_key_at(x, y):
	return '%s,%s' % ((x/100)*100, (y/100)*100)

def main():
	events.register_event('boot', display.boot)
	events.register_event('boot', entities.boot)
	events.register_event('boot', worlds.create, world_name='game')
	events.register_event('boot', boot)
	events.register_event('boot', ui.boot)
	events.register_event('boot', controls.boot, display.get_window())
	events.register_event('loop', controls.loop)
	events.register_event('load', display.load, level_editor=False)
	events.register_event('shutdown', display.shutdown)
	
	events.trigger_event('boot')
	events.trigger_event('load')
	
	pyglet.clock.schedule_interval(loop, 1/display.get_max_fps())
	pyglet.clock.schedule_interval(window, 1/10.0)
	pyglet.clock.schedule_interval(worlds.loop, 1/display.get_tps())
	
	if display.RABBYT:
		while not display.WINDOW.has_exit:
			display.lib2d.step(pyglet.clock.tick())
			display.WINDOW.dispatch_events()
			display.WINDOW.dispatch_event('on_draw')
			display.WINDOW.flip()
	else:
		pyglet.app.run()

if __name__ == '__main__':
	if '--debug' in sys.argv:
		cProfile.run('main()','profile.dat')
	else:
		main()
