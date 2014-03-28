import entities
import numbers
import display
import events
import worlds


def register_entity(entity, sprite_group):
	entity['image'] = display.load_image('ball.png')
	entity['sprite'] = display.create_sprite(entity['image'], 0, 0, sprite_group)
	entity['last_rotation'] = 0
	entity['next_rotation'] = 0
	entity['rotation_speed'] = 0
	
	entities.create_event(entity, 'set_rotation')
	entities.create_event(entity, 'rotate_by')
	
	entities.register_event(entity, 'set_rotation', set_rotation)
	entities.register_event(entity, 'rotate_by', rotate_by)
	
	events.register_event('loop', tick, entity)
	events.register_event('loop', loop, entity)


###############
#System Events#
###############

def draw():
	display.draw_sprite_group('soldiers')

def loop(entity):
	_dt = worlds.get_interp()
	
	entity['sprite'].x = int(round(numbers.interp(entity['last_position'][0], entity['position'][0], _dt)))
	entity['sprite'].y = numbers.interp(display.get_window_size()[1]-entity['last_position'][1],
	                                    display.get_window_size()[1]-entity['position'][1],
	                                    _dt)
	entity['sprite'].rotation = numbers.interp(entity['last_rotation'], entity['next_rotation'], _dt)

def tick(entity):
	entity['last_rotation'] = entity['sprite'].rotation

########
#Events#
########

def set_rotation(entity, degrees):
	entity['sprite'].rotation = degrees

def rotate_by(entity, degrees):
	entity['rotation_speed'] = degrees
	entity['next_rotation'] = entity['last_rotation']+degrees
