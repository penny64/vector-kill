import pyglet

import events


SPRITE_GROUPS = {}
WINDOW = pyglet.window.Window()
DT = 0.1


def boot():
	set_fps(60)

@WINDOW.event
def on_draw():
	global DT
	
	DT = pyglet.clock.tick()
	
	WINDOW.clear()
	events.trigger('loop')

def get_delta():
	return DT

def get_max_fps():
	return FPS

def set_fps(fps):
	global FPS
	
	FPS = float(fps)
	pyglet.clock.set_fps_limit(FPS)

def get_fps():
	return FPS*(FPS*get_delta())

def get_average_fps():
	return pyglet.clock.get_fps()


def load_image(image_name):
	_image = pyglet.image.load(image_name)
	
	return _image

def create_sprite_group():
	return pyglet.graphics.Batch()

def create_sprite(image, x, y, batch=None):
	pyglet.sprite.Sprite(image, x, y, batch=batch)

def draw_sprite_group(sprite_group):
	sprite_group.draw()
	