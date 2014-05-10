import movement
import entities
import display
import weapons
import numbers
import sprites
import effects
import bullet
import timers
import events
import ai

import random


def create(sprite_name, x=0, y=0, group=None, speed=10, scale=1, turn_rate=0.1, acceleration=0.5, max_velocity=15, death_time=10, hp=10):
	_soldier = entities.create_entity()
	_soldier['hp'] = hp
	_soldier['death_timer'] = -1
	_soldier['death_timer_max'] = death_time
	_soldier['speed'] = speed
	_soldier['turn_rate'] = turn_rate
	_soldier['collision_radius'] = 0
	
	if group:
		entities.add_entity_to_group(group, _soldier)
	else:
		print 'WARNING: Entity has no group!'
	
	movement.register_entity(_soldier, x=x, y=y)
	sprites.register_entity(_soldier, 'ships', sprite_name, scale=scale)
	entities.create_event(_soldier, 'shoot')
	entities.create_event(_soldier, 'shoot_alt')
	entities.create_event(_soldier, 'hit')
	entities.create_event(_soldier, 'kill')
	entities.create_event(_soldier, 'score')
	entities.create_event(_soldier, 'dying')
	entities.create_event(_soldier, 'explode')
	entities.register_event(_soldier, 'tick', tick)
	entities.register_event(_soldier, 'dying', destroy)
	entities.register_event(_soldier, 'explode', explode)
	entities.register_event(_soldier, 'hit', damage)
	entities.trigger_event(_soldier, 'set_minimum_velocity', velocity=[-max_velocity, -max_velocity])
	entities.trigger_event(_soldier, 'set_maximum_velocity', velocity=[max_velocity, max_velocity])
	entities.trigger_event(_soldier, 'set_acceleration', acceleration=acceleration)
	entities.trigger_event(_soldier, 'set_friction', friction=0)
	
	return _soldier

def create_energy_ship(x=0, y=0):
	_entity = create(x=x, y=y, group='players', sprite_name='ball.png', speed=19, acceleration=.3, max_velocity=30, turn_rate=0.5, death_time=35, hp=60)
	_entity['weapon_id'] = weapons.create(_entity['_id'],
	                                      rounds=35,
	                                      recoil_time=0,
	                                      reload_time=48,
	                                      kickback=3,
	                                      damage_radius=65,
	                                      spray=3,
	                                      speed=200,
	                                      missile=False,
	                                      bullet=True)['_id']
	_entity['alt_weapon_id'] = weapons.create(_entity['_id'], rounds=6, recoil_time=5, reload_time=28, speed=60, tracking=True)['_id']
	
	timers.register_entity(_entity)
	entities.register_event(_entity, 'tick', tick_energy_ship)
	entities.register_event(_entity, 'shoot', lambda entity, direction=0: entities.trigger_event(entities.get_entity(_entity['weapon_id']), 'shoot', direction=direction))
	entities.register_event(_entity, 'shoot_alt', lambda entity: entities.trigger_event(entities.get_entity(_entity['alt_weapon_id']), 'shoot'))
	
	return _entity

def create_flea(x=0, y=0, hazard=False):
	if hazard:
		_group = 'hazards'
	else:
		_group = 'enemies'
	
	_entity = create(sprite_name='diamond_body.png', group=_group, x=x, y=y, acceleration=.4, speed=30, max_velocity=30, turn_rate=0.8)
	_entity['current_target'] = None
	_entity['fire_rate'] = 0
	_entity['fire_rate_max'] = 20
	_entity['weapon_id'] = weapons.create(_entity['_id'], rounds=3, recoil_time=15, speed=30, tracking=False)['_id']
	
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

def create_eyemine(x=0, y=0, max_explode_velocity=40):
	_entity = create(x=x, y=y, group='hazards', sprite_name='eyemine_body.png', speed=35, acceleration=0.1, max_velocity=35)
	_entity['max_explode_velocity'] = max_explode_velocity
	
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
	_entity = create(x=x, y=y, group='hazards', sprite_name='eyemine_body.png', speed=5, acceleration=1, max_velocity=5)
	_entity['weapon_id'] = weapons.create(_entity['_id'], rounds=3, recoil_time=20, tracking=True, turn_rate=.02)['_id']
	
	entities.register_event(_entity, 'shoot', lambda entity: entities.trigger_event(entities.get_entity(_entity['weapon_id']), 'shoot'))
	entities.register_event(_entity, 'tick', tick_turret)
	
	return _entity

def create_gun_turret(x=0, y=0):
	_entity = create(x=x, y=y, group='hazards', sprite_name='eyemine_body.png', speed=5, acceleration=1, max_velocity=5)
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

def create_ivan(x=0, y=0):
	_entity = create(sprite_name='boss1.png', group='enemies', x=x, y=y, acceleration=.4, speed=3, max_velocity=3, turn_rate=0.8, death_time=40, hp=100)
	_entity['current_target'] = None
	_entity['fire_rate'] = 0
	_entity['fire_rate_max'] = 20
	_entity['weapon_id'] = weapons.create(_entity['_id'],
	                                      rounds=25,
	                                      recoil_time=1,
	                                      reload_time=30,
	                                      damage_radius=40,
	                                      speed=140,
	                                      missile=False,
	                                      bullet=True)['_id']
	
	entities.register_event(_entity, 'moved', set_direction)
	entities.register_event(_entity, 'tick', tick_energy_ship)
	entities.register_event(_entity, 'tick', tick_flea)
	entities.register_event(_entity, 'tick', tick_turret)
	entities.register_event(_entity, 'kill', boss_victory)
	entities.register_event(_entity, 'dying', boss_dying)
	entities.register_event(_entity, 'explode', boss_explode)
	entities.register_event(_entity, 'shoot', lambda entity: entities.trigger_event(entities.get_entity(_entity['weapon_id']), 'shoot'))
	
	return _entity

def create_ivan_large(x=0, y=0):
	_entity = create(sprite_name='boss3.png', group='hazards', scale=2.0, x=x, y=y, acceleration=.4, speed=0, max_velocity=0, turn_rate=0.8, death_time=40, hp=1000)
	_entity['current_target'] = None
	_entity['fire_rate'] = 0
	_entity['fire_rate_max'] = 20
	_entity['collision_radius'] = 1000
	_entity['cycle'] = 'shoot'
	_entity['shoot_cycle_max'] = 3
	_entity['shoot_cycle'] = 3
	_entity['spawn_cycle_max'] = 5
	_entity['spawn_cycle'] = 5
	_entity['warmup_cycles'] = 1
	
	_entity['weapon_id'] = weapons.create(_entity['_id'],
	                                      rounds=25,
	                                      recoil_time=1,
	                                      reload_time=30,
	                                      damage_radius=40,
	                                      speed=140,
	                                      missile=False,
	                                      bullet=True)['_id']
	timers.register_entity(_entity)
	effects.create_image(_entity['position'][0],
	                     _entity['position'][1],
	                     'boss3_core.png',
	                     scale=2.0,
	                     parent_entity=_entity,
	                     background=False)
	effects.create_image(_entity['position'][0],
	                     _entity['position'][1],
	                     'boss3_shield1.png',
	                     scale=2.0,
	                     rotate_by=-1,
	                     parent_entity=_entity,
	                     background=False)
	effects.create_image(_entity['position'][0],
	                     _entity['position'][1],
	                     'boss3_shield2.png',
	                     scale=2.0,
	                     rotate_by=0.5,
	                     parent_entity=_entity,
	                     background=False)
	entities.trigger_event(_entity,
	                       'create_timer',
	                       repeat=-1,
	                       time=100,
	                       repeat_callback=lambda entity: entities.trigger_event(_entity, 'shoot'))
	entities.register_event(_entity, 'moved', set_direction)
	entities.register_event(_entity, 'kill', boss_victory)
	entities.register_event(_entity, 'dying', boss_dying)
	entities.register_event(_entity, 'explode', boss_explode)
	entities.register_event(_entity, 'shoot', ivan_cycles)
	
	return _entity

def ivan_cycles(entity):
	if entity['warmup_cycles']:
		entity['warmup_cycles'] -= 1
		
		return False
	
	if entity['cycle'] == 'shoot':
		#if entity['shoot_cycle'] == entity['shoot_cycle_max']:
		#	for i in range(8):
		#		bullet.create_laser(entity['position'][0], entity['position'][0], 45*(i+1), entity['_id'], damage=30, length=90)
		
		entity['shoot_cycle'] -= 1
		
		if not entity['shoot_cycle']:
			entity['shoot_cycle'] = entity['shoot_cycle_max']
			entity['cycle'] = 'spawn'
		
		for direction in range(0, 360, 15):
			for i in range(4):
				bullet.create_bullet(entity['position'][0],
					                entity['position'][1],
					                direction+4*i,
					                60+(i*10),
					                'boss3_core.png',
					                entity['_id'],
					                damage=15)
	else:
		entity['spawn_cycle'] -= 1
		
		if not entity['spawn_cycle']:
			entity['spawn_cycle'] = entity['shoot_cycle_max']
			entity['cycle'] = 'shoot'
		
		for i in range(5):
			_mine = create_eyemine(x=entity['position'][0], y=entity['position'][1], max_explode_velocity=90)
			entities.trigger_event(_mine, 'push', velocity=numbers.velocity(random.randint(0, 359), 65))

def tick(entity):
	if entity['hp']<=0:
		if not '_dead' in entity:
			entities.trigger_event(entity, 'kill')
			
			entity['_dead'] = True
		
		entities.trigger_event(entity, 'dying')

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
	if 'max_explode_velocity' in entity and entity['current_speed']>=entity['max_explode_velocity']:
		entities.trigger_event(entity, 'kill')
		entities.trigger_event(entity, 'explode')
		
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

def boss_dying(entity):
	if random.randint(0, 3):
		_effect = effects.create_particle(entity['position'][0]+random.randint(-190, 190),
			                              entity['position'][1]+random.randint(-190, 190),
			                              'explosion.png',
			                              background=False,
			                              scale=random.uniform(.5, 1.3),
			                              flashes=random.randint(10, 15),
			                              flash_chance=0.85,
			                              direction=entity['direction']+random.randint(-90, 90),
			                              speed=entity['current_speed']*.9)
	
	if not random.randint(0, 5):
		_effect = effects.create_particle(entity['position'][0]+random.randint(-50, 50),
		                                  entity['position'][1]+random.randint(-50, 50),
		                                  'explosion.png',
		                                  background=True,
		                                  scale=random.uniform(1.0, 1.3),
		                                  scale_min=0.05,
		                                  scale_rate=.91,
		                                  friction=0,
		                                  speed=80,
		                                  direction=random.randint(0, 359),
		                                  streamer=True,
		                                  streamer_chance=.8,
		                                  swerve_rate=15)

def boss_explode(entity):
	for i in range(random.randint(3, 6)):
		_effect = effects.create_particle(entity['position'][0]+random.randint(-20, 20),
		                                  entity['position'][1]+random.randint(-20, 20),
		                                  'explosion.png',
		                                  background=False,
		                                  scale=random.uniform(.5, 1.3),
		                                  flashes=random.randint(10, 15),
		                                  flash_chance=0.85,
		                                  direction=entity['direction']+random.randint(-90, 90),
		                                  speed=entity['current_speed']*.9)
	
	for i in range(random.randint(6, 8)):
		_effect = effects.create_particle(entity['position'][0]+random.randint(-20, 20),
		                                  entity['position'][1]+random.randint(-20, 20),
		                                  'explosion.png',
		                                  background=True,
		                                  scale=random.uniform(1.0, 1.3),
		                                  scale_min=0.05,
		                                  scale_rate=.91,
		                                  friction=0,
		                                  speed=80,
		                                  direction=random.randint(0, 359),
		                                  streamer=True,
		                                  streamer_chance=.8,
		                                  swerve_rate=15)

def boss_victory(entity, victory_text='Boss Defeated'):
	display.print_text(display.get_window_size()[0]/2,
	                   display.get_window_size()[1]*.6,
	                   victory_text,
	                   color=(255, 255, 255, 255),
	                   show_for=1.5,
	                   font_size=42,
	                   center=True)

def damage(entity, damage, target_id=None):
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
