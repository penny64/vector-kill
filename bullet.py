import movement
import entities
import numbers
import sprites
import effects
import shapes
import events
import ai

import random


def create(x, y, direction, speed, sprite_name, owner_id, damage=3, life=30, turn_rate=.15, radius=50):
	_entity = entities.create_entity()
	
	movement.register_entity(_entity, x=x, y=y, direction=direction, speed=speed, turn_rate=turn_rate)
	sprites.register_entity(_entity, 'effects_foreground', sprite_name)
	entities.create_event(_entity, 'hit')
	entities.create_event(_entity, 'destroy')
	entities.register_event(_entity, 'tick', tick)
	entities.register_event(_entity, 'tick', tick_bullet)
	entities.register_event(_entity, 'destroy', destroy)
	entities.register_event(_entity, 'hit_edge', lambda entity: entities.trigger_event(entity, 'destroy'))
	entities.trigger_event(_entity, 'set_friction', friction=0)
	entities.trigger_event(_entity, 'thrust')
	entities.add_entity_to_group('bullets', _entity)
	
	_entity['life'] = life
	_entity['owner_id'] = owner_id
	_entity['damage'] = damage
	_entity['damage_radius'] = radius
	_entity['enemy_sprite_groups'] = [name for name in entities.GROUPS if not name in entities.get_entity(_entity['owner_id'])['_groups'] and not name in entities.IGNORE_ENTITY_GROUPS]
	
	return _entity

def create_bullet(x, y, direction, speed, sprite_name, owner_id, damage=3, life=3000, scale=.2, radius=50):
	_bullet = create(x, y, direction, speed, sprite_name, owner_id, damage=damage, life=life)
	_owner = entities.get_entity(_bullet['owner_id'])
	_bullet['sprite'].anchor_x = 0
	_bullet['sprite'].anchor_y = sprites.get_size(_bullet['sprite'])[1]/2
	
	entities.trigger_event(_bullet, 'set_scale', scale=scale)
	entities.trigger_event(_bullet, 'set_rotation', degrees=_bullet['direction'])
	
	return _bullet

def create_missile(x, y, direction, speed, sprite_name, owner_id, life=3000, scale=.2, turn_rate=.15, tracking=True, drunk=True, radius=50):
	_bullet = create(x, y, direction, speed, sprite_name, owner_id, life=life, turn_rate=turn_rate, radius=radius)
	_owner = entities.get_entity(_bullet['owner_id'])
	_bullet['sprite'].anchor_x = 0
	_bullet['sprite'].anchor_y = sprites.get_size(_bullet['sprite'])[1]/2
	
	entities.trigger_event(_bullet, 'set_scale', scale=scale)
	entities.register_event(_bullet, 'tick', tick_missile)
	entities.register_event(_bullet, 'hit', hit_missile)
	
	if drunk:
		entities.register_event(_bullet, 'tick', tick_drunk)
	
	if tracking:
		_bullet['target_id'] = ai.find_target(_owner, max_distance=1600)
		
		if _bullet['target_id']:
			_target = entities.get_entity(_bullet['target_id'])
			
			entities.register_event(_bullet, 'tick', tick_track)
			entities.register_event(_target,
			                        'delete',
			                        lambda target: _bullet['_id'] in entities.ENTITIES and entities.unregister_event(_bullet,
			                                                                                                         'tick',
			                                                                                                         tick_track))
			
			if 'player' in _owner and _owner['player']:
				effects.create_particle(_target['position'][0],
					                    _target['position'][1],
					                    'crosshair.png',
					                    background=False,
					                    scale_rate=.95,
					                    fade_rate=.98,
					                    spin=random.choice([-3, -6, 3, 6]))
	else:
		_bullet['target_id'] = None
	
	_bullet['engine_power'] = 100
	
	return _bullet

def create_laser(x, y, direction, owner_id, damage=12, length=20):
	_vel = numbers.velocity(direction, length)
	
	for i in range(length):
		_vel = numbers.velocity(direction, 3*(length*i))
		_bullet = create(x+_vel[0], y+_vel[1], direction, 0, 'laser.png', owner_id, damage=damage, life=10)
		entities.trigger_event(_bullet, 'set_rotation', degrees=direction)
		entities.register_event(_bullet, 'hit', hit_laser)

def destroy(bullet):
	for i in range(random.randint(2, 3)):
		_effect = effects.create_particle(bullet['position'][0]+random.randint(-2, 2),
		                                  bullet['position'][1]+random.randint(-2, 2),
		                                  'explosion.png',
		                                  background=False,
		                                  scale=random.uniform(.4, .8),
		                                  flashes=random.randint(5, 7),
		                                  flash_chance=0.7,
		                                  direction=bullet['direction']+random.randint(-45, 45),
		                                  speed=bullet['current_speed']*.5)
	
	return entities.delete_entity(bullet)

def tick_missile(bullet):
	if not random.randint(0, 3):
		_displace = (random.randint(-2, 2),
		             random.randint(-2, 2))
		
		effects.create_particle(bullet['position'][0]+_displace[0],
		                        bullet['position'][1]+_displace[1],
		                        'explosion.png',
		                        scale=0.2,
		                        scale_rate=.95,
		                        fade_rate=.7)
	
	bullet['engine_power'] -= 1
	
	if not bullet['engine_power']:
		entities.trigger_event(bullet, 'destroy')
	
	entities.trigger_event(bullet, 'set_rotation', degrees=bullet['direction'])

def tick_drunk(bullet):
	bullet['direction'] += random.randint(-6, 6)
	bullet['velocity'] = numbers.velocity(bullet['direction']+random.randint(-12, 12), bullet['speed'])

def tick_track(bullet):
	if bullet['target_id']:
		_target = entities.get_entity(bullet['target_id'])
		_current_direction = bullet['direction']
		_direction_to = numbers.direction_to(bullet['position'], _target['position'])
		_degrees_to = _current_direction-_direction_to
		
		if (_degrees_to > 0 and abs(_degrees_to) <= 180) or (_degrees_to < 0 and abs(_degrees_to) > 180):
			bullet['direction'] -= 12
		elif (_degrees_to > 0 and abs(_degrees_to) > 180) or (_degrees_to < 0 and abs(_degrees_to) <= 180):
			bullet['direction'] += 12
		
		entities.trigger_event(bullet, 'thrust')

def hit_missile(bullet, target_id):
	for i in range(random.randint(2, 3)):
		_effect = effects.create_particle(bullet['position'][0]+random.randint(-6, 6),
		                                  bullet['position'][1]+random.randint(-6, 6),
		                                  'explosion.png',
		                                  background=False,
		                                  scale=random.uniform(.4, .8),
		                                  flashes=random.randint(15, 25),
		                                  flash_chance=0.7)
		
		_effect['velocity'] = numbers.interp_velocity(bullet['velocity'], entities.get_entity(target_id)['velocity'], .1)
		_effect['velocity'][0] = numbers.clip(_effect['velocity'][0], -6, 6)
		_effect['velocity'][1] = numbers.clip(_effect['velocity'][1], -6, 6)
		
	entities.trigger_event(entities.get_entity(target_id), 'accelerate', velocity=numbers.interp_velocity(entities.get_entity(target_id)['velocity'], bullet['velocity'], .4))

def hit_laser(bullet, target_id):
	for i in range(random.randint(2, 3)):
		_effect = effects.create_particle(bullet['position'][0]+random.randint(-6, 6),
		                                  bullet['position'][1]+random.randint(-6, 6),
		                                  'explosion.png',
		                                  background=False,
		                                  scale=random.uniform(.4, .8),
		                                  flashes=random.randint(15, 25),
		                                  flash_chance=0.7)
		
		_effect['velocity'] = numbers.interp_velocity(bullet['velocity'], entities.get_entity(target_id)['velocity'], .1)
		_effect['velocity'][0] = numbers.clip(_effect['velocity'][0], -6, 6)
		_effect['velocity'][1] = numbers.clip(_effect['velocity'][1], -6, 6)
	
	entities.trigger_event(entities.get_entity(target_id), 'accelerate', velocity=numbers.interp_velocity(entities.get_entity(target_id)['velocity'], bullet['velocity'], .4))

def tick_bullet(bullet):
	if bullet['life']>0:
		bullet['life'] -= 1
	else:
		entities.delete_entity(bullet)

def tick(bullet):
	for soldier_id in entities.get_sprite_groups(bullet['enemy_sprite_groups']):
		if bullet['owner_id'] == soldier_id:
			continue
		
		_entity = entities.get_entity(soldier_id)
		
		if numbers.distance(bullet['position'], _entity['position'], old=True)-_entity['collision_radius']>bullet['damage_radius']:
			continue
		
		if bullet['owner_id'] in entities.ENTITIES and 'player' in entities.get_entity(bullet['owner_id']):
			effects.create_particle(bullet['position'][0],
				                   bullet['position'][1],
				                   'hitmarker.png',
				                   direction=random.randint(0, 359),
				                   speed=random.randint(25, 30),
				                   background=False,
				                   fade_rate=0.8,
			                        scale_rate=1.02)
		
		entities.trigger_event(bullet, 'hit', target_id=soldier_id)
		entities.trigger_event(_entity, 'hit', damage=bullet['damage'], target_id=bullet['owner_id'])
		entities.delete_entity(bullet)
