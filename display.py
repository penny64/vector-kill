import pyglet

from pyglet.gl import *

import numbers
import events
import worlds

import time
import sys


if '--rabbyt' in sys.argv:
	RABBYT = True
	#import rabbyt
	import lib2d
else:
	RABBYT = False

LOADED_IMAGES = {}
SPRITE_GROUPS = {}
SPRITE_GROUPS_DRAW_ORDER = []
LABELS = {}
TEXT_GROUPS = {}
LABEL_ID = 1
WINDOW = pyglet.window.Window(width=800, height=600, vsync=False)
DT = 1.0
FPS = 120
TPS = 120
LEVEL_GRID = []
CAMERA = {'center_on': [0, 0],
          'next_center_on': [400, 400],
          'camera_move_speed': 0.05,
          'zoom': 0,
          'next_zoom': 2.5,
          'zoom_speed': 0.09}


class Sprite(pyglet.sprite.Sprite):
	def set_position_and_rotate_and_scale(self, x, y, degrees, scale):
		self._x = x
		self._y = y
		self._rotation = degrees
		#self._update_position()
		self._scale = scale
		self._update_position()
	
	def set_scale(self, scale):
		self._scale = scale
		img = self._texture
		x1 = int(self._x - img.anchor_x * scale)
		y1 = int(self._y - img.anchor_y * scale)
		x2 = int(x1 + img.width * scale)
		y2 = int(y1 + img.height * scale)
		self._vertex_list.vertices[:] = [x1, y1, x2, y1, x2, y2, x1, y2]


@WINDOW.event
def on_draw():
	_window_width, _window_height = get_window_size()
	
	if RABBYT:
		lib2d.clear(100)
	else:
		gl.glClearColor(.1, .1, .1, 1)
	
	WINDOW.clear()
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glPushMatrix()
	events.trigger_event('camera')
	
	CAMERA['center_on'] = numbers.interp_velocity(CAMERA['center_on'], CAMERA['next_center_on'], CAMERA['camera_move_speed'])
	CAMERA['zoom'] = numbers.interp(CAMERA['zoom'], CAMERA['next_zoom'], CAMERA['zoom_speed'])
	
	#glOrtho(CAMERA['center_on'][0]-(_window_width*(.5*CAMERA['zoom']*.9)),
	#        CAMERA['center_on'][0]+(_window_width*(.5*CAMERA['zoom']*.9)),
	#        CAMERA['center_on'][1]+(_window_height*(.5*CAMERA['zoom']*.9))+_window_height,
	#        CAMERA['center_on'][1]-(_window_height*(.5*CAMERA['zoom']*.9))+_window_height, 0.0, 1.0)
	
	#events.trigger_event('draw')
	#glPopMatrix()
	#glPushMatrix()
	
	glOrtho(CAMERA['center_on'][0]-(_window_width*(.5*CAMERA['zoom'])),
	        CAMERA['center_on'][0]+(_window_width*(.5*CAMERA['zoom'])),
	        CAMERA['center_on'][1]+(_window_height*(.5*CAMERA['zoom']))+_window_height,
	        CAMERA['center_on'][1]-(_window_height*(.5*CAMERA['zoom']))+_window_height, 0.0, 1.0)
	
	pyglet.graphics.draw(len(LEVEL_GRID)/2, GL_LINES,
	                     ('v2f', LEVEL_GRID),
	                     ('c4f', (.07, .07, .07, 1.0) * (len(LEVEL_GRID)/2)))
	
	if RABBYT:
		lib2d.render()
	else:
		events.trigger_event('draw')
	
	glPopMatrix()
	glPushMatrix()
	glOrtho(0, _window_width, 0, _window_height, 0.0, 1.0)
	
	for label in LABELS.values():
		label.draw()
	
	glPopMatrix()

def boot():
	if RABBYT:
		lib2d.init()
	
	set_fps(FPS)
	set_tps(TPS)
	events.register_event('tick', tick)
	pyglet.font.add_file('thin_design.ttf')

def load(level_editor=False):
	if level_editor:
		return True
	
	global LEVEL_GRID
	
	for i in range((worlds.get_size()[0]/100)+1):
		LEVEL_GRID.extend((100*i, 0, 100*i, worlds.get_size()[1]))
	
	for i in range((worlds.get_size()[1]/100)+1):
		LEVEL_GRID.extend((0, 100*i, worlds.get_size()[1], 100*i))

def shutdown():
	pyglet.app.exit()

def screenshot():
	pyglet.image.get_buffer_manager().get_color_buffer().save('screenshot.png')

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

def create_text_group(group_name):
	TEXT_GROUPS[group_name] = []

def clear_text_group(group_name):
	for label in TEXT_GROUPS[group_name]:
		#TODO: Fix
		if label in LABELS:
			del LABELS[label]
	
	TEXT_GROUPS[group_name] = []

def create_sprite_group(group_name):
	SPRITE_GROUPS[group_name] = {'batch': pyglet.graphics.Batch(),
	                             'sprites': []}
	
	SPRITE_GROUPS_DRAW_ORDER.append(group_name)

def create_sprite(image, x, y, group_name):
	_group = SPRITE_GROUPS[group_name]
	
	if RABBYT:
		#_sprite = rabbyt.Sprite(image)
		_sprite = lib2d.Sprite(image)
	else:
		_sprite = Sprite(image, x, y, batch=_group['batch'])
	
	_group['sprites'].append(_sprite)
	
	return _sprite

def delete_sprite(entity):
	if not entity['sprite'] in SPRITE_GROUPS[entity['sprite_group']]['sprites']:
		print('Trying to remove entity from a sprite group it isn\'t in: %s (%s)' % (entity['_id'], entity['sprite_group']))
		
		return False
	
	SPRITE_GROUPS[entity['sprite_group']]['sprites'].remove(entity['sprite'])
	entity['sprite_group'] = None
	
	if not RABBYT:
		entity['sprite'].delete()

def draw_sprite_group(group_name):
	SPRITE_GROUPS[group_name]['batch'].draw()

def print_text(x, y, text, text_group=None, font_name=None, font_size=None, color=(255, 0, 255, 0), fade_in_speed=255, show_for=3, fade_out_speed=2, center=False):
	global LABEL_ID
	
	_label = pyglet.text.HTMLLabel(text, x=x, y=y)
	_label.color = tuple(color)
	_label.fade_in_speed = fade_in_speed
	_label.fade_out_speed = fade_out_speed
	_label.show_for = show_for
	_label.time_created = time.time()
	_label.text_group = text_group
	
	if font_name:
		_label.font_name = font_name
	
	if font_size:
		_label.font_size = font_size
	
	if center:
		_label.anchor_x = 'center'
	
	if text_group:
		TEXT_GROUPS[text_group].append(str(LABEL_ID))
	
	_label._id = str(LABEL_ID)
	LABELS[str(LABEL_ID)] = _label
	LABEL_ID += 1

def tick():
	_remove_labels = []
	
	for label in LABELS.values():
		if time.time()-label.time_created > label.show_for and not label.show_for == -1:
			if label.color[3]>0:
				label.color = (label.color[0], label.color[1], label.color[2], numbers.clip(label.color[3]-label.fade_out_speed, 0, 255))
			else:
				_remove_labels.append(label)
		else:
			if label.color[3] < 255:
				label.color = (label.color[0], label.color[1], label.color[2], numbers.clip(label.color[3]+label.fade_in_speed, 0, 255))
	
	for label in _remove_labels:
		del LABELS[label._id]
