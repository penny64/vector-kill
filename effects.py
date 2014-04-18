import movement
import entities
import numbers
import sprites
import events

import random


def create_particle(x, y, sprite_name, background=True, scale=1, friction=0, scale_min=0.15, direction=0, speed=0, scale_rate=1.0, fade_rate=1.0, spin=0, flashes=-1, flash_chance=0, streamer=False, swerve_rate=0, swerve_speed=25):
	_entity = entities.create_entity()
	_entity['scale_rate'] = scale_rate
	_entity['scale_min'] = scale_min
	_entity['fade_rate'] = fade_rate
	_entity['flash_chance'] = flash_chance
	_entity['flashes'] = flashes
	_entity['spin'] = spin
	_entity['streamer'] = streamer
	_entity['swerve_rate'] = swerve_rate
	_entity['swerve_speed'] = swerve_speed
	_entity['swerve_speed_max'] = swerve_speed
	
	if streamer:
		_entity['sprite_name'] = sprite_name
		_entity['background'] = background
	
	movement.register_entity(_entity, x=x, y=y)
	
	_entity['velocity'] = numbers.velocity(direction, speed)
	
	if background:
		sprites.register_entity(_entity, 'effects_background', sprite_name, scale=scale)
	else:
		sprites.register_entity(_entity, 'effects_foreground', sprite_name, scale=scale)
	
	entities.register_event(_entity, 'tick', tick_particle)
	entities.trigger_event(_entity, 'set_friction', friction=friction)
	
	return _entity

def tick_particle(particle):
	entities.trigger_event(particle, 'rotate_by', degrees=particle['spin'])
	particle['sprite'].visible = True
	particle['sprite'].opacity *= particle['fade_rate']
	
	if particle['swerve_rate']:
		particle['direction'] += (random.randint(int(round(particle['swerve_rate']*.25)), particle['swerve_rate'])*particle['swerve_speed']/float(particle['swerve_speed_max']))*random.choice([-1, 1])
		particle['velocity'] = numbers.velocity(particle['direction'], particle['swerve_speed'])
		particle['swerve_speed'] -= 1
		
		if particle['swerve_speed']<=0:
			entities.delete_entity(particle)
				
			return False
	
	if particle['flashes']>-1:
		if random.uniform(0, 1)>1-particle['flash_chance']:
			particle['sprite'].visible = False
			particle['flashes'] -= 1
		
			if not particle['flashes']:
				entities.delete_entity(particle)
				
				return False
	
	if particle['streamer'] and not random.randint(0, 3):
		_effect = create_particle(particle['position'][0],
		                          particle['position'][1],
		                          particle['sprite_name'],
		                          background=particle['background'],
		                          scale=particle['sprite'].scale,
		                          scale_min=particle['scale_min'],
		                          scale_rate=particle['scale_rate'])
		
		if particle['swerve_rate']:
			_effect['sprite'].scale = particle['swerve_speed']/float(particle['swerve_speed_max'])
	
	if particle['sprite'].scale <= particle['scale_min']:
		entities.delete_entity(particle)
	else:
		particle['sprite'].scale *= particle['scale_rate']
