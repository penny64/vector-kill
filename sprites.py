import display


def register_entity(entity):
	entity['image'] = display.load_image('ball.png')

def draw(entities):
	_draws = display.create_sprite_group()
	
	for entity in entities:
		display.create_sprite(entity['image'], entity['position'][0], entity['position'][1], batch=_draws)
	
	display.draw_sprite_group(_draws)