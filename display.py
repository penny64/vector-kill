import pyglet

from pyglet.gl import *

import numbers
import events

import time


LOADED_IMAGES = {}
SPRITE_GROUPS = {}
LABELS = []
WINDOW = pyglet.window.Window(width=800, height=600, vsync=False)
DT = 1.0
FPS = 120
TPS = 60
CAMERA = {'center_on': [0, 0],
          'next_center_on': [400, 400],
          'camera_move_speed': 0.05,
          'zoom': 0,
          'next_zoom': 2.5,
          'zoom_speed': 0.025}


@WINDOW.event
def on_draw():
	_window_width, _window_height = get_window_size()
	
	WINDOW.clear()
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glPushMatrix()
	events.trigger_event('camera')
	
	CAMERA['center_on'] = numbers.interp_velocity(CAMERA['center_on'], CAMERA['next_center_on'], CAMERA['camera_move_speed'])
	CAMERA['zoom'] = numbers.interp(CAMERA['zoom'], CAMERA['next_zoom'], CAMERA['zoom_speed'])
	
	glOrtho(CAMERA['center_on'][0]-(_window_width*(.5*CAMERA['zoom'])),
	        CAMERA['center_on'][0]+(_window_width*(.5*CAMERA['zoom'])),
	        CAMERA['center_on'][1]+(_window_height*(.5*CAMERA['zoom']))+_window_height,
	        CAMERA['center_on'][1]-(_window_height*(.5*CAMERA['zoom']))+_window_height, 0.0, 1.0)
	events.trigger_event('draw')
	glPopMatrix()
	glPushMatrix()
	glOrtho(0, _window_width, 0, _window_height, 0.0, 1.0)
	
	for label in LABELS:
		label.draw()
	
	glPopMatrix()

def boot():
	set_fps(FPS)
	set_tps(TPS)
	events.register_event('tick', tick)

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
	SPRITE_GROUPS[group_name] = {'batch': pyglet.graphics.Batch(),
	                             'sprites': []}

def create_sprite(image, x, y, group_name):
	_group = SPRITE_GROUPS[group_name]
	_sprite = pyglet.sprite.Sprite(image, x, y, batch=_group['batch'])
	_group['sprites'].append(_sprite)
	
	return _sprite

def delete_sprite(entity):
	SPRITE_GROUPS[entity['sprite_group']]['sprites'].remove(entity['sprite'])
	entity['sprite'].delete()

def draw_sprite_group(group_name):
	SPRITE_GROUPS[group_name]['batch'].draw()

def print_text(x, y, text, color=(255, 0, 255, 0), fade_in_speed=255, show_for=3, fade_out_speed=2, center=False):
	_label = pyglet.text.HTMLLabel(text, x=x, y=y)
	_label.color = tuple(color)
	_label.fade_in_speed = fade_in_speed
	_label.fade_out_speed = fade_out_speed
	_label.show_for = show_for
	_label.time_created = time.time()
	
	if center:
		_label.anchor_x = 'center'
	
	LABELS.append(_label)

def tick():
	_remove_labels = []
	
	for label in LABELS:
		if time.time()-label.time_created > label.show_for:
			if label.color[3]>0:
				label.color = (label.color[0], label.color[1], label.color[2], numbers.clip(label.color[3]-label.fade_out_speed, 0, 255))
			else:
				_remove_labels.append(label)
		else:
			if label.color[3] < 255:
				label.color = (label.color[0], label.color[1], label.color[2], numbers.clip(label.color[3]+label.fade_in_speed, 0, 255))
	
	for label in _remove_labels:
		LABELS.remove(label)
