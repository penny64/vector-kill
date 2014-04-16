import pyglet

from pyglet.gl import *

import numbers
import events


LOADED_IMAGES = {}
SPRITE_GROUPS = {}
WINDOW = pyglet.window.Window(width=1024, height=768)
DT = 1.0
FPS = 60
TPS = 50
CAMERA = {'center_on': [0, 0],
          'next_center_on': [400, 400],
          'camera_move_speed': 0.025,
          'zoom': 1,
          'next_zoom': 2.5,
          'zoom_speed': 0.025}


@WINDOW.event
def on_draw():
	WINDOW.clear()
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glPushMatrix()
	events.trigger_event('camera')
	
	CAMERA['center_on'] = numbers.interp_velocity(CAMERA['center_on'], CAMERA['next_center_on'], CAMERA['camera_move_speed'])
	CAMERA['zoom'] = numbers.interp(CAMERA['zoom'], CAMERA['next_zoom'], CAMERA['zoom_speed'])
	
	glOrtho(CAMERA['center_on'][0]-(1024*(.5*CAMERA['zoom'])),
	        CAMERA['center_on'][0]+(1024*(.5*CAMERA['zoom'])),
	        CAMERA['center_on'][1]+(768*(.5*CAMERA['zoom']))+765,
	        CAMERA['center_on'][1]-(768*(.5*CAMERA['zoom']))+765, 0.0, 1.0)
	
	events.trigger_event('draw')
	glPopMatrix()

def boot():
	set_fps(FPS)
	set_tps(TPS)

def get_window():
	return WINDOW

def get_window_size():
	return WINDOW.width, WINDOW.height

def set_clock_delta(dt):
	global DT
	
	DT = 1-dt

def get_clock_delta():
	return DT

def set_tps(tps):
	global TPS
	
	TPS = float(tps)

def get_tps():
	return TPS

def reschedule(func, interval):
	pyglet.clock.unschedule(func)
	pyglet.clock.schedule_interval(func, interval)

def set_fps(fps):
	global FPS
	
	FPS = float(fps)

def get_fps():
	return FPS*(get_clock_delta())

def get_max_fps():
	return FPS

def set_caption(caption):
	WINDOW.set_caption(caption)

def load_image(image_name):
	if image_name in LOADED_IMAGES:
		return LOADED_IMAGES[image_name]
	
	_image = pyglet.image.load(image_name)
	_image.anchor_x = _image.width/2
	_image.anchor_y = _image.height/2
	
	LOADED_IMAGES[image_name] = _image
	
	return _image

def create_sprite_group(group_name):
	SPRITE_GROUPS[group_name] = {'group': pyglet.graphics.Batch(),
	                             'sprites': []}

def create_sprite(image, x, y, group_name):
	_group = SPRITE_GROUPS[group_name]
	_sprite = pyglet.sprite.Sprite(image, x, y, batch=_group['group'])
	_group['sprites'].append(_sprite)
	
	return _sprite

def draw_sprite_group(group_name):
	SPRITE_GROUPS[group_name]['group'].draw()
