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


def create(sprite_name, x=0, y=0, group=None, speed=10, turn_rate=0.1, acceleration=0.5, max_velocity=15, death_time=10, hp=10):
	_soldier = entities.create_entity()
	_soldier['hp'] = hp
	_soldier['death_timer'] = -1
	_soldier['death_timer_max'] = death_time
	_soldier['speed'] = speed
	_soldier['turn_rate'] = turn_rate
	
	if group:
		entities.add_entity_to_group(group, _soldier)
	else:
		print 'WARNING: Entity has no group!'
	
	movement.register_entity(_soldier, x=x, y=y)
	sprites.register_entity(_soldier, 'ships', sprite_name)
	entities.create_event(_soldier, 'shoot')
	entities.create_event(_soldier, 'hit')
	entities.create_event(_soldier, 'kill')
	entities.create_event(_soldier, 'score')
	entities.create_event(_soldier, 'explode')
	entities.register_event(_soldier, 'tick', tick)
	entities.register_event(_soldier, 'kill', destroy)
	entities.register_event(_soldier, 'explode', explode)
	entities.register_event(_soldier, 'hit', damage)
	entities.trigger_event(_soldier, 'set_minimum_velocity', velocity=[-max_velocity, -max_velocity])
	entities.trigger_event(_soldier, 'set_maximum_velocity', velocity=[max_velocity, max_velocity])
	entities.trigger_event(_soldier, 'set_acceleration', acceleration=acceleration)
	entities.trigger_event(_soldier, 'set_friction', friction=0)
	
	return _soldier

def create_energy_ship():
	_entity = create(group='players', sprite_name='ball.png', acceleration=.05, max_velocity=30, turn_rate=0.3, death_time=35, hp=30)
	_entity['weapon_id'] = weapons.create(_entity['_id'], rounds=6, recoil_time=5, tracking=True)['_id']
	#_entity['weapon_id'] = weapons.create(_entity['_id'], rounds=2, recoil_time=0, reload_time=1, speed=125, missile=False, bullet=True, damage_radius=150)['_id']
	
	entities.register_event(_entity, 'tick', tick_energy_ship)
	entities.register_event(_entity, 'shoot', lambda entity: entities.trigger_event(entities.get_entity(_entity['weapon_id']), 'shoot'))
	
	return _entity

def create_flea(x=0, y=0):
	_entity = create(sprite_name='diamond_body.png', group='enemies', x=x, y=y, acceleration=.4, speed=30, max_velocity=30, turn_rate=0.8)
	_entity['current_target'] = None
	_entity['fire_rate'] = 0
	_entity['fire_rate_max'] = 20
	_entity['weapon_id'] = weapons.create(_entity['_id'], rounds=3, recoil_time=15, tracking=False)['_id']
	
	effects.create_image(_entity['position'][0],
	                     _entity['position'][1],
	                     'diamond_turret.png',
	                     parent_entity=_entity)
	effects.create_image(_entity['position'][0],
	                     _entity['position'][1],
	                     'diamond_drive.png',
	                     parent_entity=_entity,
	                     rotate_by=3)
	
	entities.register_event(_entity, 'moved', set_direction)
	entities.register_event(_entity, 'tick', tick_energy_ship)
	entities.register_event(_entity, 'tick', tick_flea)
	entities.register_event(_entity, 'tick', tick_turret)
	entities.register_event(_entity, 'shoot', lambda entity: entities.trigger_event(entities.get_entity(_entity['weapon_id']), 'shoot'))
	
	return _entity

def create_eyemine(x=0, y=0):
	_entity = create(x=x, y=y, group='hazards', sprite_name='eyemine_body.png', speed=35, acceleration=0.1, max_velocity=35)
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
	_entity = create(x=x, y=y, group='hazards', sprite_name='eyemine_body.png', speed=5, acceleration=1, max_velocity=0)
	_entity['weapon_id'] = weapons.create(_entity['_id'], rounds=3, recoil_time=20, tracking=True, turn_rate=.02)['_id']
	
	entities.register_event(_entity, 'shoot', lambda entity: entities.trigger_event(entities.get_entity(_entity['weapon_id']), 'shoot'))
	entities.register_event(_entity, 'tick', tick_turret)
	
	return _entity

def create_gun_turret(x=0, y=0):
	_entity = create(x=x, y=y, group='hazards', sprite_name='eyemine_body.png', speed=5, acceleration=1, max_velocity=0)
	_entity['weapon_id'] = weapons.create(_entity['_id'],
	                                      rounds=10,
	                                      recoil_time=2,
	                                      reload_time=40,
	                                      damage_radius=40,
	                                      speed=140,
	                                      missile=False,
	                                      bullet=True)['_id']
	
	entities.register_event(_entity, 'shoot', lambda entity: entities.trigger_event(entities.get_entity(_entity['weapon_id']), 'shoot'))
	entities.register_event(_entity, 'tick', tick_turret)
	
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
	entity['shoot_direction'] = numbers.direction_to(entity['last_position'], entity['position'])
	
	if random.randint(0, 1):
		_displace = (random.uniform(-entity['velocity'][0], entity['velocity'][0]),
		             random.uniform(-entity['velocity'][1], entity['velocity'][1]))
		_effect_direction = numbers.direction_to(entity['position'],
		                                         (entity['position'][0]+(entity['velocity'][0]*6),
		                                          entity['position'][1]+(entity['velocity'][1]*6)))
		_effect_direction += (abs(entity['shoot_direction']-_effect_direction)*numbers.clip(_effect_direction, -1, 1))*5
		
		effects.create_particle(entity['position'][0]+_displace[0],
		                        entity['position'][1]+_displace[1],
		                        'streamer.png',
		                        scale_rate=.75,
		                        speed=-entity['current_speed'],
		                        friction=0.1,
		                        direction=_effect_direction+random.randint(-5, 5),
		                        rotation=_effect_direction)

def tick_eyemine(entity):
	if entity['current_speed']>=35:
		entities.trigger_event(entity, 'kill')
		
		return entities.delete_entity(entity)
	
	if entity['current_target'] and entity['current_target'] in entities.ENTITIES:
		_target_object = entities.get_entity(entity['current_target'])
	else:
		_target_object = None
	
	for soldier_id in entities.get_sprite_groups(['enemies', 'players']):
		if entity['_id'] == soldier_id:
			continue
		
		if numbers.distance(entity['position'], entities.get_entity(soldier_id)['position'], old=True)>50:
			continue
		
		if _target_object and not entity['current_target'] == soldier_id and 'player' in _target_object:
			entities.trigger_event(_target_object,
			                       'score',
			                       target_id=entity['_id'],
			                       amount=10,
			                       text='Creative Escape')
		
		entities.trigger_event(entities.get_entity(soldier_id), 'hit', damage=6, target_id=entity['_id'])
		entities.trigger_event(entity, 'kill')
		entities.trigger_event(entity, 'explode')
		entities.delete_entity(entity)
		
		break

def tick_turret(entity):
	_target_id = ai.find_target(entity, max_distance=1600)
	
	if _target_id:
		entity['shoot_direction'] = numbers.direction_to(entity['position'], entities.get_entity(_target_id)['position'])
		entities.trigger_event(entity, 'shoot')

def set_direction(entity, **kwargs):
	entities.trigger_event(entity, 'set_rotation', degrees=entity['direction'])

def destroy(entity):
	entity['hp'] = 0
	
	if entity['death_timer'] == -1:
		entity['death_timer'] = entity['death_timer_max']
	
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
	
	#if not random.randint(0, 7):
	#	_effect = effects.create_particle(entity['position'][0]+random.randint(-50, 50),
	#	                                  entity['position'][1]+random.randint(-50, 50),
	#	                                  'smoke.png',
	#	                                  background=True,
	#	                                  scale=random.uniform(.5, 1.1),
	#	                                  scale_min=0.05,
	#	                                  scale_rate=.9,
	#	                                  friction=0.3)
	
	if random.randint(0, 3):
		_effect = effects.create_particle(entity['position'][0]+random.randint(-20, 20),
		                                  entity['position'][1]+random.randint(-20, 20),
		                                  'explosion.png',
		                                  background=False,
		                                  scale=random.uniform(.5, 1.3),
		                                  flashes=random.randint(10, 15),
		                                  flash_chance=0.85,
		                                  direction=entity['direction']+random.randint(-90, 90),
		                                  speed=entity['current_speed']*.9)

def explode(entity):
	#if not random.randint(0, 3):
	#	_effect = effects.create_particle(entity['position'][0]+random.randint(-50, 50),
	#	                                  entity['position'][1]+random.randint(-50, 50),
	#	                                  'smoke.png',
	#	                                  background=True,
	#	                                  scale=random.uniform(.5, 1.3),
	#	                                  scale_min=0.1,
	#	                                  scale_rate=.9,
	#	                                  fade_rate=.9,
	#	                                  friction=0.1,
	#	                                  streamer=True)
	
	for i in range(random.randint(0, 3)+('player' in entity)*2):
		_effect = effects.create_particle(entity['position'][0]+random.randint(-20, 20),
		                                  entity['position'][1]+random.randint(-20, 20),
		                                  'explosion.png',
		                                  background=True,
		                                  scale=random.uniform(1.0, 1.3),
		                                  scale_min=0.05,
		                                  scale_rate=.91,
		                                  friction=0,
		                                  speed=40,
		                                  direction=random.randint(0, 359),
		                                  streamer=True,
		                                  streamer_chance=.8,
		                                  swerve_rate=15)

def damage(entity, damage, target_id):
	entity['hp'] -= damage
	
	if entity['hp']<=0 and entity['death_timer'] == -1:
		entities.trigger_event(entity, 'set_friction', friction=0.05)
		
		if target_id in entities.ENTITIES:
			entities.trigger_event(entities.get_entity(target_id),
			                       'score',
			                       target_id=entity['_id'],
			                       amount=5,
			                       text='Kill')
	elif entity['hp']<0:
		_text = 'Overkill'
		
		if target_id in entities.ENTITIES:
			entities.trigger_event(entities.get_entity(target_id),
			                       'score',
			                       target_id=entity['_id'],
			                       amount=2*abs(entity['hp']),
			                       text=_text)
