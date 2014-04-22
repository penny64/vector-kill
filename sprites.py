import entities
import numbers
import display
import events
import worlds

import pyglet


def register_entity(entity, sprite_group, sprite_name, scale=1):
	if display.RABBYT:
		entity['image'] = sprite_name
	else:
		entity['image'] = display.load_image(sprite_name)
	
	entity['sprite'] = display.create_sprite(entity['image'], 0, 0, sprite_group)
	entity['sprite_group'] = sprite_group
	entity['last_rotation'] = 0
	entity['next_rotation'] = 0
	entity['rotation_speed'] = 0
	entity['sprite'].scale = scale
	
	entities.create_event(entity, 'set_rotation')
	entities.create_event(entity, 'rotate_by')
	entities.create_event(entity, 'fade_by')
	entities.register_event(entity, 'tick', tick)
	entities.register_event(entity, 'delete', display.delete_sprite)
	entities.register_event(entity, 'set_rotation', set_rotation)
	entities.register_event(entity, 'rotate_by', rotate_by)
	entities.register_event(entity, 'fade_by', fade_by)
	entities.register_event(entity, 'loop', loop)


###############
#System Events#
###############

def draw():
	display.draw_sprite_group('effects_background')
	display.draw_sprite_group('ships')
	display.draw_sprite_group('effects_foreground')

def loop(entity):
	if not entity['_id'] in entities.ENTITIES:
		return False
	
	_dt = worlds.get_interp()
	
	entity['sprite'].x = int(round(numbers.interp(entity['last_position'][0], entity['position'][0], _dt)))
	entity['sprite'].y = numbers.interp(display.get_window_size()[1]+entity['last_position'][1],
	                                    display.get_window_size()[1]+entity['position'][1],
	                                    _dt)
	
	if not display.RABBYT:
		entity['sprite'].rotation = numbers.interp(entity['last_rotation'], entity['next_rotation'], _dt)

def tick(entity):
	if not display.RABBYT:
		entity['last_rotation'] = entity['sprite'].rotation

########
#Events#
########

def set_rotation(entity, degrees):
	if display.RABBYT:
		entity['sprite'].rot(degrees)
	else:
		entity['next_rotation'] = degrees
		entity['sprite'].rotation = degrees

def rotate_by(entity, degrees):
	entity['rotation_speed'] = degrees
	entity['next_rotation'] = entity['last_rotation']-degrees

def fade_by(entity, amount):
	if display.RABBYT:
		pass
		#entity['sprite'].alpha *= amount
	else:
		entity['sprite'].opacity *= amount

def get_size(sprite):
	if display.RABBYT:
		return (sprite.right-sprite.left, sprite.top-sprite.bottom)
	else:
		return sprite.width, sprite.height
		