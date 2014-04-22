import movement
import entities
import weapons
import numbers
import sprites
import effects
import bullet
import events
import ai

import random


def create(sprite_name, x=0, y=0, group=None, speed=10, turn_rate=0.1, acceleration=0.5, max_velocity=15):
	_soldier = entities.create_entity()
	_soldier['hp'] = 10
	_soldier['death_timer'] = -1
	_soldier['speed'] = speed
	_soldier['turn_rate'] = turn_rate
	
	entities.add_entity_to_group('soldiers', _soldier)
	
	if group:
		entities.add_entity_to_group(group, _soldier)
	
	movement.register_entity(_soldier, x=x, y=y)
	sprites.register_entity(_soldier, 'soldiers', sprite_name)
	entities.create_event(_soldier, 'shoot')
	entities.create_event(_soldier, 'hit')
	entities.create_event(_soldier, 'kill')
	entities.create_event(_soldier, 'score')
	entities.create_event(_soldier, 'explode')
	entities.register_event(_soldier, 'tick', tick)
	entities.register_event(_soldier, 'kill', destroy)
	entities.register_event(_soldier, 'explode', explode)
	entities.register_event(_soldier, 'hit', damage)
	entities.register_event(_soldier, 'moved', set_direction)
	entities.trigger_event(_soldier, 'set_minimum_velocity', velocity=[-max_velocity, -max_velocity])
	entities.trigger_event(_soldier, 'set_maximum_velocity', velocity=[max_velocity, max_velocity])
	entities.trigger_event(_soldier, 'set_acceleration', acceleration=acceleration)
	entities.trigger_event(_soldier, 'set_friction', friction=0)
	
	return _soldier

def create_energy_ship():
	_entity = create(sprite_name='ball.png', acceleration=.05, turn_rate=0.3)
	_entity['weapon_id'] = weapons.create(_entity['_id'], rounds=6, recoil_time=5, tracking=True)['_id']
	
	entities.register_event(_entity, 'tick', tick_energy_ship)
	entities.register_event(_entity, 'shoot', lambda entity: entities.trigger_event(entities.get_entity(_entity['weapon_id']), 'shoot'))
	
	return _entity

def create_flea(x=0, y=0):
	_entity = create(sprite_name='ball.png', group='enemies', x=x, y=y, acceleration=.2, speed=5, turn_rate=0.8)
	_entity['current_target'] = None
	_entity['fire_rate'] = 0
	_entity['fire_rate_max'] = 20
	_entity['weapon_id'] = weapons.create(_entity['_id'], rounds=3, recoil_time=15, tracking=False)['_id']
	
	entities.register_event(_entity, 'tick', tick_energy_ship)
	entities.register_event(_entity, 'tick', tick_flea)
	entities.register_event(_entity, 'tick', tick_turret)
	entities.register_event(_entity, 'shoot', lambda entity: entities.trigger_event(entities.get_entity(_entity['weapon_id']), 'shoot'))
	#entities.register_event(_entity, 'shoot', shoot_turret)
	
	return _entity

def create_eyemine(x=0, y=0):
	_entity = create(x=x, y=y, group='hazards', sprite_name='eyemine_body.png', speed=25, acceleration=0.1, max_velocity=25)
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
	entities.register_event(_entity, 'hit_edge', lambda entity: entities.trigger_event(entity, 'kill'))
	ai.guard(_entity)
	
	return _entity

def create_missile_turret(x=0, y=0):
	_entity = create(x=x, y=y, sprite_name='eyemine_body.png', speed=5, acceleration=1, max_velocity=0)
	_entity['weapon_id'] = weapons.create(_entity['_id'], rounds=3, recoil_time=20, tracking=True, turn_rate=.02)['_id']
	
	entities.register_event(_entity, 'shoot', lambda entity: entities.trigger_event(entities.get_entity(_entity['weapon_id']), 'shoot'))
	entities.register_event(_entity, 'tick', tick_turret)
	
	entities.add_entity_to_group('hazards', _entity)
	
	return _entity

def tick(entity):
	if entity['hp']<=0:
		entities.trigger_event(entity, 'kill')

def tick_flea(entity):
	if not entity['current_target']:
		entity['current_target'] = ai.find_target(entity)
	
		if entity['current_target']:
			ai.track_target(entity, entity['current_target'])

def tick_energy_ship(entity):
	if random.randint(0, 1):
		_displace = (random.uniform(-entity['velocity'][0], entity['velocity'][0]),
		             random.uniform(-entity['velocity'][1], entity['velocity'][1]))
		
		effects.create_particle(entity['position'][0]+_displace[0], entity['position'][1]+_displace[1], 'ball_shadow.png', scale_rate=.9)
	
	entity['shoot_direction'] = numbers.direction_to(entity['last_position'], entity['position'])

def tick_eyemine(entity):
	if entity['current_speed']>=35:
		entities.trigger_event(entity, 'kill')
		return entities.delete_entity(entity)
	
	for soldier_id in entities.get_sprite_groups(['enemies', 'players']):
		if entity['_id'] == soldier_id:
			continue
		
		if numbers.distance(entity['position'], entities.get_entity(soldier_id)['position'], old=True)>50:
			continue
		
		entities.trigger_event(entities.get_entity(soldier_id), 'hit', damage=6, target_id=entity['_id'])
		entities.trigger_event(entity, 'kill')
		entities.delete_entity(entity)
		
		break

def tick_turret(entity):
	_target_id = ai.find_target(entity, max_distance=1600)
	
	if _target_id:
		entity['shoot_direction'] = numbers.direction_to(entity['position'], entities.get_entity(_target_id)['position'])
		entities.trigger_event(entity, 'shoot')

def set_direction(entity, **kwargs):
	_direction = numbers.distance([0, 0], kwargs['position_change'])*numbers.clip(kwargs['position_change'][0], -1, 1)
	entities.trigger_event(entity, 'rotate_by', degrees=_direction*.5)

def destroy(entity):
	entity['hp'] = 0
	
	if entity['death_timer'] == -1:
		entity['death_timer'] = 10
	
	if entity['death_timer']:
		entity['death_timer'] -= 1
	else:
		entities.trigger_event(entity, 'explode')
		_effect = effects.create_particle(entity['position'][0]+random.randint(-20, 20),
		                                  entity['position'][1]+random.randint(-20, 20),
		                                  'shockwave.png',
		                                  background=True,
		                                  scale=0,
		                                  scale_min=-.1,
		                                  scale_max=8,
		                                  scale_rate=1.1)
		entities.delete_entity(entity)
	
	if not random.randint(0, 7):
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
	
	if random.randint(0, 3):
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
	if not random.randint(0, 3):
		_effect = effects.create_particle(entity['position'][0]+random.randint(-20, 20),
		                                  entity['position'][1]+random.randint(-20, 20),
		                                  'smoke.png',
		                                  background=True,
		                                  scale=random.uniform(.5, 1.3),
		                                  scale_min=0.1,
		                                  scale_rate=.9,
		                                  fade_rate=.9,
		                                  friction=0.1,
		                                  streamer=True,
		                                  direction=entity['direction']+random.randint(-90, 90),
		                                  speed=entity['current_speed']*.7)
	
	for i in range(random.randint(0, 3)):
		_effect = effects.create_particle(entity['position'][0]+random.randint(-20, 20),
		                                  entity['position'][1]+random.randint(-20, 20),
		                                  'explosion.png',
		                                  background=True,
		                                  scale=random.uniform(1.0, 1.3),
		                                  scale_min=0.05,
		                                  scale_rate=.91,
		                                  friction=0,
		                                  streamer=True,
		                                  streamer_chance=.8,
		                                  swerve_rate=15)
		_effect['direction'] = random.randint(0, 359)
		_effect['velocity'] = numbers.velocity(_effect['direction'], 40)

def damage(entity, damage, target_id):
	entity['hp'] -= damage
	
	if entity['hp']<=0 and entity['death_timer'] == -1:
		entities.trigger_event(entity, 'set_friction', friction=0.05)
		
		if target_id in entities.ENTITIES:
			entities.trigger_event(entities.get_entity(target_id), 'score', target_id=entity['_id'])
	
	#entities.delete_entity(entity)
