import movement
import entities
import numbers
import sprites
import effects
import bullet
import events

import random


def create():
	_soldier = entities.create_entity()
	_soldier['hp'] = 10
	_soldier['death_timer'] = -1
	
	entities.add_entity_to_group('soldiers', _soldier)
	movement.register_entity(_soldier)
	sprites.register_entity(_soldier, 'soldiers', 'ball.png')
	entities.create_event(_soldier, 'shoot')
	entities.create_event(_soldier, 'hit')
	entities.create_event(_soldier, 'kill')
	entities.register_event(_soldier, 'tick', tick)
	entities.register_event(_soldier, 'kill', destroy)
	entities.register_event(_soldier, 'shoot', shoot)
	entities.register_event(_soldier, 'hit', damage)
	entities.register_event(_soldier, 'moved', set_direction)
	entities.trigger_event(_soldier, 'set_minimum_velocity', velocity=[-15, -15])
	entities.trigger_event(_soldier, 'set_maximum_velocity', velocity=[15, 15])
	entities.trigger_event(_soldier, 'set_acceleration', acceleration=.05)
	entities.trigger_event(_soldier, 'set_friction', friction=0)
	
	return _soldier

def set_direction(entity, **kwargs):
	_direction = numbers.distance([0, 0], kwargs['position_change'])*numbers.clip(kwargs['position_change'][0], -1, 1)
	entities.trigger_event(entity, 'rotate_by', degrees=_direction*.5)

def tick(entity):
	if random.randint(0, 4):
		_displace = (random.uniform(-entity['velocity'][0], entity['velocity'][0]),
		             random.uniform(-entity['velocity'][1], entity['velocity'][1]))
		
		effects.create_particle(entity['position'][0]+_displace[0], entity['position'][1]+_displace[1], 'ball_shadow.png', scale_rate=.9)
	
	if entity['hp']<=0:
		entities.trigger_event(entity, 'kill')

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
		                                  scale=random.uniform(.5, 1.3),
		                                  scale_min=0.05,
		                                  scale_rate=.98)
		
		_effect['velocity'] = numbers.interp_velocity(entity['velocity'],
		                                              (entity['velocity'][0]+random.randint(-8, 8),
		                                               entity['velocity'][1]+random.randint(-8, 8)), .8)
	
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
		                                               entity['velocity'][1]+random.randint(-8, 8)), .8)

def shoot(entity, direction=0, speed=30):
	bullet.create_bullet(entity['position'][0], entity['position'][1], direction, 30, 'ball_shadow.png', entity['_id'])

def damage(entity, damage, target_id):
	entity['hp'] -= damage
	
	#entities.delete_entity(entity)
