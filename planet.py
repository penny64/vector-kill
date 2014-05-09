import movement
import entities
import display
import sprites
import numbers
import effects
import player
import events
import worlds
import ships
import clock
import items
import maps

import random


LEVEL = 1
WAVE = 1
NOTERIETY = 0
TRANSITION_PAUSE = 0
CHANGE_WAVE = False
CHANGE_WAVE_FIRE = False
ANNOUNCE = True
WAVE_TIMER_MAX = 30*45
WAVE_TIMER = 240


def create():
	global WAVE_TIMER_MAX, WAVE_TIMER, WAVE
	
	WAVE = 1
	WAVE_TIMER = 240
	WAVE_TIMER_MAX = 30*45
	
	worlds.create('planet', width=12000, height=12000)
	_planet = entities.create_entity(group='planets')
	sprites.register_entity(_planet, 'effects_foreground', 'planet.png', scale=1.0)
	movement.register_entity(_planet, x=worlds.get_size()[0]/2, y=worlds.get_size()[0]/2, speed=0)
	effects.create_image(_planet['position'][0], _planet['position'][1], 'ring.png', background=2, scale=2)
	events.register_event('tick', tick)
	create_player()
	display.clear_grid()
	items.create_gravity_well(x=worlds.get_size()[0]/2, y=worlds.get_size()[0]/2, strength=0.25)

def clean():
	for ship_id in entities.get_entity_group('players'):
		entities.delete_entity(entities.ENTITIES[ship_id])
	
	for ship_id in entities.get_entity_group('enemies'):
		entities.delete_entity(entities.ENTITIES[ship_id])	
	
	for ship_id in entities.get_entity_group('hazards'):
		entities.delete_entity(entities.ENTITIES[ship_id])
	
	for ship_id in entities.get_entity_group('effects'):
		entities.delete_entity(entities.ENTITIES[ship_id])
	
	for ship_id in entities.get_entity_group('bullets'):
		entities.delete_entity(entities.ENTITIES[ship_id])
	
	for ship_id in entities.get_entity_group('weapons'):
		entities.delete_entity(entities.ENTITIES[ship_id])
	
	entities.reset()
		
def create_player(x=0, y=0):
	_player = ships.create_energy_ship(x=x, y=y)
	_player['player'] = True
	
	player.register_entity(_player)
	events.register_event('input', player.handle_input, _player['_id'])
	events.register_event('camera', player.handle_camera, _player['_id'], min_zoom=5, max_zoom=14, max_enemy_distance=10000, center_distance=5000)
	entities.register_event(_player, 'delete', player.delete)
	entities.register_event(_player, 'hit_edge', lambda entity: entities.trigger_event(entity, 'hit', damage=100))
	entities.trigger_event(_player, 'push', velocity=(30, 30))

def spawn_enemies():
	global TRANSITION_PAUSE, CHANGE_WAVE_FIRE, CHANGE_WAVE, ANNOUNCE, WAVE
	
	_i = random.choice([0, 1, 2, 3])
	
	if WAVE == 3:
		TRANSITION_PAUSE = 30*30
		CHANGE_WAVE = True
		CHANGE_WAVE_FIRE = False
		
		return False
	
	if _i == 1:
		_xrange = random.choice([(100, worlds.get_size()[0]*.25),
		                         (worlds.get_size()[0]*.25, worlds.get_size()[0]*.5),
		                         (worlds.get_size()[0]*.5, worlds.get_size()[0]*.75),
		                         (worlds.get_size()[0]*.75, worlds.get_size()[0]-100)])
		_y = 100
	elif _i == 2:
		_x = worlds.get_size()[0]-100
		_y = random.choice([(100, worlds.get_size()[1]*.25),
		                         (worlds.get_size()[1]*.25, worlds.get_size()[1]*.5),
		                         (worlds.get_size()[1]*.5, worlds.get_size()[1]*.75),
		                         (worlds.get_size()[1]*.75, worlds.get_size()[1]-100)])
	elif _i == 3:
		_x = 100
		_y = random.randint(100, worlds.get_size()[1]-100)
	else:
		_x = random.randint(100, worlds.get_size()[0]-100)
		_y = worlds.get_size()[1]-100
	
	_missile_turrets = int(round(10*((WAVE+1)/5.0)))
	_gun_turrets = int(round(10*(WAVE/5.0)))
	_fleas = int(round(5*(WAVE/5.0)))
	
	for i in range(_fleas):
		if _i == 1:
			_x = random.randint(100, worlds.get_size()[0]-100)
			_y = 100
		elif _i == 2:
			_x = worlds.get_size()[0]-100
			_y = random.randint(100, worlds.get_size()[1]-100)
		elif _i == 3:
			_x = 100
			_y = random.randint(100, worlds.get_size()[1]-100)
		else:
			_x = random.randint(100, worlds.get_size()[0]-100)
			_y = worlds.get_size()[1]-100
		
		_entity = ships.create_flea(x=_x, y=_y, hazard=True)
		_move_direction = numbers.direction_to((_x, _y,), (worlds.get_size()[0]/2, worlds.get_size()[1]/2))
		
		entities.trigger_event(_entity, 'push', velocity=numbers.velocity(_move_direction, 20))
	
	for i in range(_gun_turrets):
		if _i == 1:
			_x = random.randint(200, worlds.get_size()[0]-200)
			_y = 200
		elif _i == 2:
			_x = worlds.get_size()[0]-200
			_y = random.randint(200, worlds.get_size()[1]-200)
		elif _i == 3:
			_x = 200
			_y = random.randint(200, worlds.get_size()[1]-200)
		else:
			_x = random.randint(200, worlds.get_size()[0]-200)
			_y = worlds.get_size()[1]-200
		
		_entity = ships.create_gun_turret(x=_x, y=_y)
		_move_direction = numbers.direction_to((_x, _y,), (worlds.get_size()[0]/2, worlds.get_size()[1]/2))
		
		entities.trigger_event(_entity, 'push', velocity=numbers.velocity(_move_direction, 20))
	
	for i in range(_missile_turrets):
		if _i == 1:
			_x = random.randint(100, worlds.get_size()[0]-100)
			_y = 100
		elif _i == 2:
			_x = worlds.get_size()[0]-100
			_y = random.randint(100, worlds.get_size()[1]-100)
		elif _i == 3:
			_x = 100
			_y = random.randint(100, worlds.get_size()[1]-100)
		else:
			_x = random.randint(100, worlds.get_size()[0]-100)
			_y = worlds.get_size()[1]-100
		
		_entity = ships.create_missile_turret(x=_x, y=_y)
		_move_direction = numbers.direction_to((_x, _y,), (worlds.get_size()[0]/2, worlds.get_size()[1]/2))
		
		entities.trigger_event(_entity, 'push', velocity=numbers.velocity(_move_direction, 20))
	
	WAVE += 1
	ANNOUNCE = True

def tick():
	global WAVE_TIMER
	
	if WAVE_TIMER:
		WAVE_TIMER -= 1

def loop():
	global CHANGE_WAVE_FIRE, TRANSITION_PAUSE, CHANGE_WAVE, WAVE_TIMER, LEVEL, WAVE
	
	if TRANSITION_PAUSE and CHANGE_WAVE:
		_player = entities.get_entity(entities.get_entity_group('players')[0])
		
		if not CHANGE_WAVE_FIRE:
			entities.trigger_event(_player,
			                       'create_timer',
			                       time=120,
			                       enter_callback=lambda entity: events.unregister_event('input', player.handle_input),
			                       callback=lambda entity: entities.trigger_event(entity, 'push', velocity=(6, 6)),
			                       exit_callback=lambda entity: display.camera_snap((-4000, -4000)) and entities.trigger_event(entity, 'set_position', x=-4000, y=-4000) and events.register_event('input', player.handle_input, _player['_id']))
			
			LEVEL += 1
			_player['NO_BOUNCE'] = True
			CHANGE_WAVE_FIRE = True
		
		if TRANSITION_PAUSE:
			TRANSITION_PAUSE -= 1
		
		return False
	
	if CHANGE_WAVE:
		WAVE = 1
		CHANGE_WAVE = False
	
	if not entities.get_entity_group('enemies') and not entities.get_entity_group('hazards') and WAVE_TIMER:
		WAVE_TIMER -= 4
	
	if entities.get_entity_group('players') and WAVE_TIMER<=0:
		spawn_enemies()
		WAVE_TIMER = WAVE_TIMER_MAX+(60*WAVE)
