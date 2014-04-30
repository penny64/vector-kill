import movement
import entities
#import threads
import numbers
import sprites
import events

import random


def create_particle(x, y, sprite_name, background=True, scale=1, rotation=0, friction=0, scale_min=0.15, scale_max=5, direction=0, speed=0, scale_rate=1.0, fade_rate=1.0, spin=0, flashes=-1, flash_chance=0, streamer=False, streamer_chance=0.3, swerve_rate=0, swerve_speed=25, force_smooth_draw=False):
	_entity = entities.create_entity()
	_entity['scale_rate'] = scale_rate
	_entity['scale_min'] = scale_min
	_entity['scale_max'] = scale_max
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
		_entity['streamer_chance'] = streamer_chance
	
	movement.register_entity(_entity, x=x, y=y)
	entities.add_entity_to_group('effects', _entity)
	entities.trigger_event(_entity, 'set_direction', direction=direction)
	entities.trigger_event(_entity, 'set_speed', speed=speed)
	entities.trigger_event(_entity, 'thrust')
	
	if _entity['speed'] or force_smooth_draw:
		_smooth_draw = True
	else:
		_smooth_draw = False
		entities.register_event(_entity, 'moved', lambda entity, **kwargs: entities.trigger_event(entity, 'redraw'))
		
		#TODO: Hack
		entities.register_event(_entity, 'moved', lambda entity, **kwargs: entities.unregister_event(entity, 'tick', movement.tick))
	
	if background:
		sprites.register_entity(_entity, 'effects_background', sprite_name, scale=scale, smooth_draw=_smooth_draw)
	else:
		sprites.register_entity(_entity, 'effects_foreground', sprite_name, scale=scale, smooth_draw=_smooth_draw)
	
	if swerve_rate:
		_entity['sprite'].opacity = 0
	
	entities.register_event(_entity, 'tick', tick_particle)
	entities.trigger_event(_entity, 'set_friction', friction=friction)
	entities.trigger_event(_entity, 'set_rotation', degrees=rotation)
	
	return _entity

def create_image(x, y, sprite_name, parent_entity=None, rotate_by=0, rotate_with_parent=False, background=False, scale=1):
	_entity = entities.create_entity(group='effects')
	
	if parent_entity:
		_entity['parent_entity'] = parent_entity['_id']
	else:
		_entity['parent_entity'] = None
	
	_entity['rotate_by'] = rotate_by
	_entity['rotate_with_parent'] = rotate_with_parent
	
	movement.register_entity(_entity, x=x, y=y, no_tick=True)
	entities.register_event(_entity, 'loop', tick_image)
	
	if parent_entity:
		entities.register_event(parent_entity, 'delete', lambda parent_entity: entities.delete_entity(_entity))
	
	if background:
		sprites.register_entity(_entity, 'effects_background', sprite_name, scale=scale)
	else:
		sprites.register_entity(_entity, 'effects_foreground', sprite_name, scale=scale)
	
	return _entity

def tick_particle(particle):
	if particle['spin']:
		entities.trigger_event(particle, 'rotate_by', degrees=particle['spin'])
	
	if particle['fade_rate']:
		entities.trigger_event(particle, 'fade_by', amount=particle['fade_rate'])
	
	particle['sprite'].visible = True
	
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
	
	if particle['streamer'] and random.uniform(0, 1)>1-particle['streamer_chance']:
		if particle['swerve_rate']:
			_image = 'streamer.png'
		else:
			_image = particle['sprite_name']
		
		_effect = create_particle(particle['position'][0],
		                          particle['position'][1],
		                          _image,
		                          background=particle['background'],
		                          direction=particle['direction'],
		                          scale=particle['sprite'].scale,
		                          scale_min=particle['scale_min'],
		                          scale_rate=particle['scale_rate'])
		
		if particle['swerve_rate']:
			entities.trigger_event(_effect, 'set_rotation', degrees=particle['direction'])
			entities.trigger_event(_effect, 'set_scale', scale=particle['swerve_speed']/float(particle['swerve_speed_max']))
			_effect['sprite'].opacity = 255*particle['swerve_speed']/float(particle['swerve_speed_max'])
	
	if not particle['scale_rate'] == 1:
		if particle['sprite'].scale < particle['scale_min']:
			entities.delete_entity(particle)
		elif particle['sprite'].scale > particle['scale_max']:
			entities.delete_entity(particle)
		else:
			entities.trigger_event(particle, 'set_scale', scale=particle['sprite'].scale*particle['scale_rate'])

def tick_image(image):
	if image['parent_entity']:
		_parent_entity = entities.get_entity(image['parent_entity'])
		entities.trigger_event(image, 'set_position', x=_parent_entity['position'][0], y=_parent_entity['position'][1])
		
		if image['rotate_with_parent']:
			entities.trigger_event(image, 'set_rotation', degrees=_parent_entity['direction'])
		elif image['rotate_by']:
			entities.trigger_event(image, 'rotate_by', degrees=image['rotate_by'])
		