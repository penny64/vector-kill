import movement
import entities
import numbers
import sprites
import effects
import bullet
import events

import random


def create(sprite_name):
	_soldier = entities.create_entity()
	_soldier['hp'] = 10
	_soldier['death_timer'] = -1
	
	entities.add_entity_to_group('soldiers', _soldier)
	movement.register_entity(_soldier)
	sprites.register_entity(_soldier, 'soldiers', sprite_name)
	entities.create_event(_soldier, 'shoot')
	entities.create_event(_soldier, 'hit')
	entities.create_event(_soldier, 'kill')
	entities.create_event(_soldier, 'score')
	entities.register_event(_soldier, 'tick', tick)
	entities.register_event(_soldier, 'kill', destroy)
	entities.register_event(_soldier, 'delete', explode)
	entities.register_event(_soldier, 'shoot', shoot)
	entities.register_event(_soldier, 'hit', damage)
	entities.register_event(_soldier, 'moved', set_direction)
	entities.trigger_event(_soldier, 'set_minimum_velocity', velocity=[-15, -15])
	entities.trigger_event(_soldier, 'set_maximum_velocity', velocity=[15, 15])
	entities.trigger_event(_soldier, 'set_acceleration', acceleration=.05)
	entities.trigger_event(_soldier, 'set_friction', friction=0)
	
	return _soldier

def create_energy_ship():
	_entity = create(sprite_name='ball.png')
	
	entities.register_event(_entity, 'tick', tick_energy_ship)
	
	return _entity

def create_eyemine():
	_entity = create(sprite_name='eyemine_body.png')
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
	                     background=False)
	
	
	return _entity

def tick(entity):
	if entity['hp']<=0:
		entities.trigger_event(entity, 'kill')

def tick_energy_ship(entity):
	if random.randint(0, 4):
		_displace = (random.uniform(-entity['velocity'][0], entity['velocity'][0]),
		             random.uniform(-entity['velocity'][1], entity['velocity'][1]))
		
		effects.create_particle(entity['position'][0]+_displace[0], entity['position'][1]+_displace[1], 'ball_shadow.png', scale_rate=.9)

def set_direction(entity, **kwargs):
	_direction = numbers.distance([0, 0], kwargs['position_change'])*numbers.clip(kwargs['position_change'][0], -1, 1)
	entities.trigger_event(entity, 'rotate_by', degrees=_direction*.5)

def destroy(entity):
	if entity['death_timer'] == -1:
		entity['death_timer'] = 25
	
	if entity['death_timer']:
		entity['death_timer'] -= 1
	else:
		entities.delete_entity(entity)
	
	for i in range(random.randint(1, 2)):
		_effect = effects.create_particle(entity['position'][0]+random.randint(-20, 20),
		                                  entity['position'][1]+random.randint(-20, 20),
		                                  'smoke.png',
		                                  background=True,
		                                  scale=random.uniform(.5, 1.1),
		                                  scale_min=0.05,
		                                  scale_rate=.98)
		
		_effect['velocity'] = numbers.interp_velocity(entity['velocity'],
		                                              (entity['velocity'][0]+random.randint(-8, 8),
		                                               entity['velocity'][1]+random.randint(-8, 8)), .1)
	
	for i in range(random.randint(1, 2)):
		_effect = effects.create_particle(entity['position'][0]+random.randint(-20, 20),
		                                  entity['position'][1]+random.randint(-20, 20),
		                                  'explosion.png',
		                                  background=False,
		                                  scale=random.uniform(.5, 1.3),
		                                  flashes=random.randint(10, 15),
		                                  flash_chance=0.85)
		
		entity['velocity'] = numbers.interp_velocity(entity['velocity'],
		                                             (entity['velocity'][0]+random.randint(-8, 8),
		                                              entity['velocity'][1]+random.randint(-8, 8)), .2)
		_effect['velocity'] = numbers.interp_velocity(entity['velocity'],
		                                              (entity['velocity'][0]+random.randint(-8, 8),
		                                               entity['velocity'][1]+random.randint(-8, 8)), .3)

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
		                                  streamer=True)
		
		_effect['velocity'] = [entity['velocity'][0]+random.randint(-4, 4),
		                       entity['velocity'][1]+random.randint(-4, 4)]
	
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
	bullet.create_bullet(entity['position'][0], entity['position'][1], direction, 30, 'bullet.png', entity['_id'])

def damage(entity, damage, target_id):
	entity['hp'] -= damage
	
	if entity['hp']<=0 and entity['death_timer'] == -1:
		entities.trigger_event(entity, 'set_friction', friction=0.05)
		entities.trigger_event(entities.get_entity(target_id), 'score', target_id=entity['_id'])
	
	#entities.delete_entity(entity)
