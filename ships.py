import movement
import entities
import numbers
import sprites
import effects
import bullet
import events
import ai

import random


def create(sprite_name, x=0, y=0, speed=10, turn_rate=0.1, acceleration=0.5, max_velocity=15):
	_soldier = entities.create_entity()
	_soldier['hp'] = 10
	_soldier['death_timer'] = -1
	_soldier['speed'] = speed
	_soldier['turn_rate'] = turn_rate
	
	entities.add_entity_to_group('soldiers', _soldier)
	movement.register_entity(_soldier, x=x, y=y)
	sprites.register_entity(_soldier, 'soldiers', sprite_name)
	entities.create_event(_soldier, 'shoot')
	entities.create_event(_soldier, 'hit')
	entities.create_event(_soldier, 'kill')
	entities.create_event(_soldier, 'score')
	entities.register_event(_soldier, 'tick', tick)
	entities.register_event(_soldier, 'kill', destroy)
	entities.register_event(_soldier, 'delete', explode)
	entities.register_event(_soldier, 'hit', damage)
	entities.register_event(_soldier, 'moved', set_direction)
	entities.trigger_event(_soldier, 'set_minimum_velocity', velocity=[-max_velocity, -max_velocity])
	entities.trigger_event(_soldier, 'set_maximum_velocity', velocity=[max_velocity, max_velocity])
	entities.trigger_event(_soldier, 'set_acceleration', acceleration=acceleration)
	entities.trigger_event(_soldier, 'set_friction', friction=0)
	
	return _soldier

def create_energy_ship():
	_entity = create(sprite_name='ball.png', acceleration=.05, turn_rate=0.3)
	
	entities.register_event(_entity, 'tick', tick_energy_ship)
	entities.register_event(_entity, 'shoot', shoot)
	
	return _entity

def create_eyemine(x=0, y=0):
	_entity = create(x=x, y=y, sprite_name='eyemine_body.png', speed=15, acceleration=0.1, max_velocity=15)
	effects.create_image(_entity['position'][0],
	                     _entity['position'][1],
	                     'eyemine_subbody.png',
	                     parent_entity=_entity,
	                     rotate_by=3,
	                     background=True)
	effects.create_image(_entity['position'][0],
	                     _entity['position'][1],
	                     'eyemine_eye1.png',
	                     parent_entity=_entity,
	                     background=False)
	effects.create_image(_entity['position'][0],
	                     _entity['position'][1],
	                     'eyemine_eye2.png',
	                     parent_entity=_entity,
	                     rotate_with_parent=True,
	                     background=False)
	entities.register_event(_entity, 'tick', tick_eyemine)
	entities.register_event(_entity,
	                        'hit',
	                        lambda _entity, target_id, **kwargs: target_id in entities.ENTITIES and entities.trigger_event(_entity,
	                                                                                                                       'set_direction',
	                                                                                                                       direction=numbers.direction_to(_entity['position'],
	                                                                                                                                                      entities.get_entity(target_id)['position'])))
	entities.register_event(_entity, 'hit', lambda _entity, target_id, **kwargs: ai.track_target(_entity, target_id))
	ai.guard(_entity)
	
	return _entity

def create_missile_turret(x=0, y=0):
	_entity = create(x=x, y=y, sprite_name='eyemine_body.png', speed=0, acceleration=0, max_velocity=0)
	_entity['fire_rate'] = 0
	_entity['fire_rate_max'] = 20
	
	entities.register_event(_entity, 'shoot', shoot_turret)
	entities.register_event(_entity, 'tick', tick_turret)

def tick(entity):
	if entity['hp']<=0:
		entities.trigger_event(entity, 'kill')

def tick_energy_ship(entity):
	if random.randint(0, 4):
		_displace = (random.uniform(-entity['velocity'][0], entity['velocity'][0]),
		             random.uniform(-entity['velocity'][1], entity['velocity'][1]))
		
		effects.create_particle(entity['position'][0]+_displace[0], entity['position'][1]+_displace[1], 'ball_shadow.png', scale_rate=.9)

def tick_eyemine(entity):
	if entity['current_speed']>=35:
		entities.trigger_event(entity, 'kill')
		return entities.delete_entity(entity)
	
	for soldier_id in entities.get_sprite_group('soldiers'):
		if entity['_id'] == soldier_id:
			continue
		
		if numbers.distance(entity['position'], entities.get_entity(soldier_id)['position'], old=True)>50:
			continue
		
		entities.trigger_event(entities.get_entity(soldier_id), 'hit', damage=6, target_id=entity['_id'])
		entities.trigger_event(entity, 'kill')
		entities.delete_entity(entity)
		
		break

def tick_turret(entity):
	if entity['fire_rate']:
		entity['fire_rate'] -= 1
		
		return False
	
	_target_id = ai.find_target(entity, max_distance=1600)
	
	if _target_id:
		entities.trigger_event(entity, 'shoot', target_id=_target_id)
		entity['fire_rate'] = entity['fire_rate_max']

def shoot_turret(entity, target_id):
	_direction = numbers.direction_to(entity['position'], entities.get_entity(target_id)['position'])
	
	bullet.create_missile(entity['position'][0], entity['position'][1], _direction, 30, 'bullet.png', entity['_id'], turn_rate=.05)

def set_direction(entity, **kwargs):
	_direction = numbers.distance([0, 0], kwargs['position_change'])*numbers.clip(kwargs['position_change'][0], -1, 1)
	entities.trigger_event(entity, 'rotate_by', degrees=_direction*.5)

def destroy(entity):
	if entity['death_timer'] == -1:
		entity['death_timer'] = 15
	
	if entity['death_timer']:
		entity['death_timer'] -= 1
	else:
		_effect = effects.create_particle(entity['position'][0]+random.randint(-20, 20),
		                                  entity['position'][1]+random.randint(-20, 20),
		                                  'shockwave.png',
		                                  background=True,
		                                  scale=0,
		                                  scale_min=-.1,
		                                  scale_max=2,
		                                  scale_rate=1.1)
		entities.delete_entity(entity)
	
	for i in range(random.randint(1, 2)):
		_effect = effects.create_particle(entity['position'][0]+random.randint(-20, 20),
		                                  entity['position'][1]+random.randint(-20, 20),
		                                  'smoke.png',
		                                  background=True,
		                                  scale=random.uniform(.5, 1.1),
		                                  scale_min=0.05,
		                                  scale_rate=.96,
		                                  friction=0.3,
		                                  direction=entity['direction']+random.randint(-90, 90),
		                                  speed=random.uniform(entity['current_speed']*.3, entity['current_speed']*.5))
	
	for i in range(random.randint(1, 2)):
		_effect = effects.create_particle(entity['position'][0]+random.randint(-20, 20),
		                                  entity['position'][1]+random.randint(-20, 20),
		                                  'explosion.png',
		                                  background=False,
		                                  scale=random.uniform(.5, 1.3),
		                                  flashes=random.randint(10, 15),
		                                  flash_chance=0.85,
		                                  direction=entity['direction']+random.randint(-90, 90),
		                                  speed=entity['current_speed']*.3)
		
		entity['velocity'] = numbers.interp_velocity(entity['velocity'],
		                                             (entity['velocity'][0]+random.randint(-8, 8),
		                                              entity['velocity'][1]+random.randint(-8, 8)), .2)

def explode(entity):
	for i in range(random.randint(2, 4)):
		_effect = effects.create_particle(entity['position'][0]+random.randint(-20, 20),
		                                  entity['position'][1]+random.randint(-20, 20),
		                                  'smoke.png',
		                                  background=True,
		                                  scale=random.uniform(.5, 1.3),
		                                  scale_min=0.05,
		                                  scale_rate=.9,
		                                  friction=0.1,
		                                  streamer=True,
		                                  direction=entity['direction']+random.randint(-90, 90),
		                                  speed=entity['current_speed']*.7)
	
	for i in range(random.randint(4, 6)):
		_effect = effects.create_particle(entity['position'][0]+random.randint(-20, 20),
		                                  entity['position'][1]+random.randint(-20, 20),
		                                  'explosion.png',
		                                  background=True,
		                                  scale=random.uniform(1.0, 1.3),
		                                  scale_min=0.05,
		                                  scale_rate=.91,
		                                  friction=0,
		                                  streamer=True,
		                                  streamer_chance=1,
		                                  swerve_rate=15)
		_effect['direction'] = random.randint(0, 359)
		_effect['velocity'] = numbers.velocity(_effect['direction'], 40)

def shoot(entity, direction=0, speed=30):
	bullet.create_missile(entity['position'][0], entity['position'][1], entity['direction'], 30, 'bullet.png', entity['_id'])

def damage(entity, damage, target_id):
	entity['hp'] -= damage
	
	if entity['hp']<=0 and entity['death_timer'] == -1:
		entities.trigger_event(entity, 'set_friction', friction=0.05)
		
		if target_id in entities.ENTITIES:
			entities.trigger_event(entities.get_entity(target_id), 'score', target_id=entity['_id'])
	
	#entities.delete_entity(entity)
