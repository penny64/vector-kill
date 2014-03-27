import entities
import display
import events


def register_entity(entity, sprite_group):
	entity['image'] = display.load_image('ball.png')
	entity['sprite'] = display.create_sprite(entity['image'], 0, 0, sprite_group)
	
	entities.create_event(entity, 'set_rotation')
	entities.create_event(entity, 'rotate_by')
	
	entities.register_event(entity, 'set_rotation', set_rotation)
	entities.register_event(entity, 'rotate_by', rotate_by)
	
	events.register_event('tick', tick, entity)


###############
#System Events#
###############

def draw():
	display.draw_sprite_group('soldiers')

def tick(entity):
	_window_size = display.get_window_size()
	
	entity['sprite'].x = entity['position'][0]
	entity['sprite'].y = _window_size[1]-entity['position'][1]


########
#Events#
########

def set_rotation(entity, degrees):
	entity['sprite'].rotation = degrees

def rotate_by(entity, degrees):
	entity['sprite'].rotation += degrees
