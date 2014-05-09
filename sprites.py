import entities
import numbers
import display
import events
import worlds

import pyglet


def register_entity(entity, sprite_group, sprite_name, scale=1, smooth_draw=True):
	if display.RABBYT:
		entity['image'] = sprite_name
	else:
		entity['image'] = display.load_image(sprite_name)
	
	entity['sprite'] = display.create_sprite(entity['image'], 0, 0, sprite_group)
	entity['sprite_group'] = sprite_group
	entity['last_rotation'] = 0
	entity['next_rotation'] = 0
	entity['rotation_speed'] = 0
	entity['last_scale'] = scale
	entity['next_scale'] = scale
	entity['smooth_draw'] = smooth_draw
	entity['scale_only'] = False
	
	entities.create_event(entity, 'redraw')
	entities.create_event(entity, 'set_scale')
	entities.create_event(entity, 'set_rotation')
	entities.create_event(entity, 'rotate_by')
	entities.create_event(entity, 'fade_by')
	entities.register_event(entity, 'tick', tick)
	entities.register_event(entity, 'redraw', lambda _entity: entities.register_event(_entity, 'loop', loop))
	entities.register_event(entity, 'delete', display.delete_sprite)
	entities.register_event(entity, 'set_scale', set_scale)
	entities.register_event(entity, 'set_rotation', set_rotation)
	entities.register_event(entity, 'rotate_by', rotate_by)
	entities.register_event(entity, 'fade_by', fade_by)
	entities.register_event(entity, 'loop', loop)


###############
#System Events#
###############

def draw():
	for group_name in display.SPRITE_GROUPS_DRAW_ORDER:
		display.draw_sprite_group(group_name)
		#display.draw_sprite_group('ships')
		#display.draw_sprite_group('effects_foreground')

def loop(entity):
	if not entity['smooth_draw']:
		entity['sprite'].set_position_and_rotate_and_scale(entity['position'][0],
		                                                   display.get_window_size()[1]+entity['position'][1],
		                                                   entity['next_rotation'],
		                                                   entity['next_scale'])
		
		if not entity['last_scale'] and not entity['next_scale']:
			entities.unregister_event(entity, 'loop', loop)
		else:
			_dt = worlds.get_interp()
			img = entity['sprite']._texture
			_scale = numbers.interp(entity['last_scale'], entity['next_scale'], _dt)
			x1 = int(entity['sprite']._x - img.anchor_x * _scale)
			y1 = int(entity['sprite']._y - img.anchor_y * _scale)
			x2 = int(x1 + img.width * _scale)
			y2 = int(y1 + img.height * _scale)
			entity['sprite']._scale = _scale
			
			if not entity['sprite']._visible:
				entity['sprite']._vertex_list.vertices[:] = [0, 0, 0, 0, 0, 0, 0, 0]
			else:
				entity['sprite']._vertex_list.vertices[:] = [x1, y1, x2, y1, x2, y2, x1, y2]
		
		return False
	
	_dt = worlds.get_interp()
	_rot = numbers.interp(entity['last_rotation'], entity['next_rotation'], _dt)

	entity['sprite'].set_position_and_rotate_and_scale(int(round(numbers.interp(entity['last_position'][0], entity['position'][0], _dt))),
	                                                   numbers.interp(display.get_window_size()[1]+entity['last_position'][1],
	                                                                  display.get_window_size()[1]+entity['position'][1],
	                                                                  _dt),
	                                                   _rot,
	                                                   numbers.interp(entity['last_scale'], entity['next_scale'], _dt))

def tick(entity):
	if not display.RABBYT:
		entity['last_rotation'] = entity['sprite'].rotation

########
#Events#
########

def set_scale(entity, scale):
	entity['last_scale'] = scale
	entity['next_scale'] = scale

def set_rotation(entity, degrees):
	if display.RABBYT:
		entity['sprite'].rot(degrees)
	else:
		entity['last_rotation'] = degrees
		entity['next_rotation'] = degrees

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
		