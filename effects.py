import movement
import entities
import sprites
import events


def create_particle(x, y, sprite_name, background=True):
	_entity = entities.create_entity()
	
	movement.register_entity(_entity, x=x, y=y)
	
	if background:
		sprites.register_entity(_entity, 'effects_background', sprite_name)
	else:
		sprites.register_entity(_entity, 'effects_foreground', sprite_name)
	
	entities.register_event(_entity, 'tick', tick_particle)

def tick_particle(particle):
	if particle['sprite'].scale <= .15:
		entities.delete_entity(particle)
	else:
		particle['sprite'].scale *= .9
