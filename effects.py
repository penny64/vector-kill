import movement
import entities
import numbers
import sprites
import events

import random


def create_particle(x, y, sprite_name, background=True, scale=1, scale_min=0.15, direction=0, speed=0, scale_rate=1.0, fade_rate=1.0, spin=0, flashes=-1, flash_chance=0):
	_entity = entities.create_entity()
	_entity['scale_rate'] = scale_rate
	_entity['scale_min'] = scale_min
	_entity['fade_rate'] = fade_rate
	_entity['flash_chance'] = flash_chance
	_entity['flashes'] = flashes
	_entity['spin'] = spin
	
	movement.register_entity(_entity, x=x, y=y)
	
	_entity['velocity'] = numbers.velocity(direction, speed)
	
	if background:
		sprites.register_entity(_entity, 'effects_background', sprite_name, scale=scale)
	else:
		sprites.register_entity(_entity, 'effects_foreground', sprite_name, scale=scale)
	
	entities.register_event(_entity, 'tick', tick_particle)
	
	return _entity

def tick_particle(particle):
	entities.trigger_event(particle, 'rotate_by', degrees=particle['spin'])
	particle['sprite'].visible = True
	
	if particle['flashes']>-1:
		if random.uniform(0, 1)>1-particle['flash_chance']:
			particle['sprite'].visible = False
			particle['flashes'] -= 1
		
			if not particle['flashes']:
				entities.delete_entity(particle)
				
				return False
	
	if particle['sprite'].scale <= particle['scale_min']:
		entities.delete_entity(particle)
	else:
		particle['sprite'].scale *= particle['scale_rate']
