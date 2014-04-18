import movement
import entities
import numbers
import sprites
import effects
import events

import random


def create_bullet(x, y, direction, speed, sprite_name, owner_id, life=30):
	_entity = entities.create_entity()
	_entity['life'] = life
	
	movement.register_entity(_entity, x=x, y=y)
	sprites.register_entity(_entity, 'effects_foreground', sprite_name)
	entities.create_event(_entity, 'hit')
	entities.register_event(_entity, 'create', setup_missile)
	entities.register_event(_entity, 'hit', hit_missile)
	entities.register_event(_entity, 'tick', tick_missile)
	entities.register_event(_entity, 'tick', tick)
	entities.trigger_event(_entity, 'set_friction', friction=0)
	
	_entity['sprite'].scale = 0.2
	_entity['owner_id'] = owner_id
	
	entities.trigger_event(_entity, 'create')

def setup_missile(bullet):
	_owner = entities.get_entity(bullet['owner_id'])
	_closest_target = {'enemy_id': None, 'distance': 0}
	bullet['sprite'].anchor_x = 0
	bullet['sprite'].anchor_y = bullet['sprite'].height/2
	
	for soldier_id in entities.get_sprite_group('soldiers'):
		if bullet['owner_id'] == soldier_id:
			continue
		
		_distance = numbers.distance(bullet['position'], entities.get_entity(soldier_id)['position'])
		
		if not _closest_target['enemy_id'] or _distance<_closest_target['distance']:
			_closest_target['distance'] = _distance
			_closest_target['enemy_id'] = soldier_id
	
	if _closest_target['enemy_id']:
		bullet['target_pos'] = entities.get_entity(_closest_target['enemy_id'])['position']
		effects.create_particle(bullet['target_pos'][0],
		                        bullet['target_pos'][1],
		                        'crosshair.png',
		                        background=False,
		                        scale_rate=.95,
		                        fade_rate=.98,
		                        spin=random.choice([-3, -6, 3, 6]))
	else:
		bullet['target_pos'] = None
	
	bullet['direction'] = numbers.direction_to(_owner['position'],
	                                           (_owner['position'][0]+_owner['velocity'][0],
	                                            _owner['position'][1]+_owner['velocity'][1]))+random.randint(-6, 6)
	entities.trigger_event(bullet, 'set_rotation', degrees=bullet['direction'])
	bullet['engine_power'] = 100

def tick_missile(bullet):
	if random.randint(0, 4):
		_displace = (random.randint(-2, 2),
		             random.randint(-2, 2))
		
		effects.create_particle(bullet['position'][0]+_displace[0],
		                        bullet['position'][1]+_displace[1],
		                        'explosion.png',
		                        scale=0.2,
		                        scale_rate=.95,
		                        fade_rate=.7)
	
	if bullet['target_pos']:
		_direction_to = numbers.direction_to(bullet['position'], bullet['target_pos'])
		_degrees_to = abs(bullet['direction']-_direction_to)
		
		if _degrees_to>=180:
			_direction_to += 360
		
		if bullet['engine_power']>0:
			_new_direction = numbers.interp(bullet['direction'], _direction_to, 0.1)+random.randint(-4, 4)
			_direction_difference = abs(bullet['direction']-_new_direction)
			_speed = 60*numbers.clip(1-(numbers.distance(bullet['position'], bullet['target_pos'])/1100), 0.3, 1.0)
			bullet['engine_power'] -= numbers.clip(_direction_difference-10, 0, 100)
			bullet['direction'] = _new_direction
			bullet['velocity'] = numbers.velocity(bullet['direction'], _speed)
			entities.trigger_event(bullet, 'set_rotation', degrees=bullet['direction'])
	else:
		bullet['engine_power'] -= 1
		bullet['direction'] += random.randint(-7, 7)
		bullet['velocity'] = numbers.velocity(bullet['direction'], 15)
	
	if bullet['engine_power']<0 and bullet['engine_power']>-20:
		bullet['engine_power'] -= 1
	elif bullet['engine_power'] <= -20:
		for i in range(random.randint(2, 3)):
			_effect = effects.create_particle(bullet['position'][0]+random.randint(-2, 2),
				                             bullet['position'][1]+random.randint(-2, 2),
				                             'explosion.png',
				                             background=False,
				                             scale=random.uniform(.4, .8),
				                             flashes=random.randint(5, 7),
				                             flash_chance=0.7)
			
			_effect['velocity'] = numbers.velocity(bullet['direction']+random.randint(-12, 12), 10)
		
		return entities.delete_entity(bullet)

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

def tick_bullet(bullet):
	#_entity['velocity'] = numbers.velocity(direction+random.randint(-3, 3), speed)
	
	if bullet['life']>0:
		bullet['life'] -= 1
	else:
		entities.delete_entity(bullet)

def tick(bullet):
	for soldier_id in entities.get_sprite_group('soldiers'):
		if bullet['owner_id'] == soldier_id:
			continue
		
		if numbers.distance(bullet['position'], entities.get_entity(soldier_id)['position'], old=True)>50:
			continue
		
		entities.trigger_event(bullet, 'hit', target_id=soldier_id)
		entities.trigger_event(entities.get_entity(soldier_id), 'hit', damage=3, target_id=bullet['owner_id'])
		entities.delete_entity(bullet)
