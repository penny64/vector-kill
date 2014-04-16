import pyglet

from pyglet.gl import *

import numbers
import events


LOADED_IMAGES = {}
SPRITE_GROUPS = {}
LABELS = []
WINDOW = pyglet.window.Window(width=800, height=600)
DT = 1.0
FPS = 120
TPS = 60
CAMERA = {'center_on': [0, 0],
          'next_center_on': [400, 400],
          'camera_move_speed': 0.01,
          'zoom': 0,
          'next_zoom': 2.5,
          'zoom_speed': 0.025}


@WINDOW.event
def on_draw():
	_window_with, _window_height = get_window_size()
	
	WINDOW.clear()
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glPushMatrix()
	events.trigger_event('camera')
	
	CAMERA['center_on'] = numbers.interp_velocity(CAMERA['center_on'], CAMERA['next_center_on'], CAMERA['camera_move_speed'])
	CAMERA['zoom'] = numbers.interp(CAMERA['zoom'], CAMERA['next_zoom'], CAMERA['zoom_speed'])
	
	glOrtho(CAMERA['center_on'][0]-(_window_with*(.5*CAMERA['zoom'])),
	        CAMERA['center_on'][0]+(_window_with*(.5*CAMERA['zoom'])),
	        CAMERA['center_on'][1]+(_window_height*(.5*CAMERA['zoom']))+_window_height,
	        CAMERA['center_on'][1]-(_window_height*(.5*CAMERA['zoom']))+_window_height, 0.0, 1.0)
	
	while LABELS:
		LABELS.pop(0).draw()
	
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

def print_text(x, y, text, color=(255, 0, 255, 150)):
	_label = pyglet.text.HTMLLabel('<b>Hello</b>, <i>world</i>', x=10, y=10)
	_label.color = color
	
	LABELS.append(_label)
