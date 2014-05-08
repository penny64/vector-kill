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
NOTERIETY = 0
TRANSITION_PAUSE = 0
CHANGE_LEVEL = False
CHANGE_LEVEL_FIRE = False
ANNOUNCE = True
WAVE_TIMER_MAX = 30*45
WAVE_TIMER = 240


def create():
	global WAVE_TIMER_MAX, WAVE_TIMER, LEVEL
	
	LEVEL = 1
	WAVE_TIMER = 240
	WAVE_TIMER_MAX = 30*45
	
	worlds.create('planet', width=12000, height=12000)
	_planet = entities.create_entity(group='planets')
	sprites.register_entity(_planet, 'effects_foreground', 'planet.png', scale=1.8)
	movement.register_entity(_planet, x=worlds.get_size()[0]/2, y=worlds.get_size()[0]/2, speed=0)
	effects.create_image(_planet['position'][0], _planet['position'][1], 'ring.png', background=2, scale=2)
	events.register_event('tick', tick)
	create_player(x=2000, y=2000)
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

def spawn_enemies():
	global TRANSITION_PAUSE, CHANGE_LEVEL_FIRE, CHANGE_LEVEL, ANNOUNCE, LEVEL
	
	_i = random.choice([0, 1, 2, 3])
	
	if LEVEL == 3:
		TRANSITION_PAUSE = 30*30
		CHANGE_LEVEL = True
		CHANGE_LEVEL_FIRE = False
		
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
	
	_missile_turrets = numbers.clip(LEVEL, 1, 5)
	_gun_turrets = numbers.clip(LEVEL, 1, 3)
	
	for i in range(_gun_turrets):
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
		
		_entity = ships.create_gun_turret(x=_x, y=_y)
		_move_direction = numbers.direction_to((_x, _y,), (worlds.get_size()[0]/2, worlds.get_size()[1]/2))
		
		entities.trigger_event(_entity, 'set_direction', direction=_move_direction)
		entities.trigger_event(_entity, 'set_speed', speed=2)
		entities.trigger_event(_entity, 'set_minimum_velocity', velocity=[-5, -5])
		entities.trigger_event(_entity, 'set_maximum_velocity', velocity=[5, 5])
		entities.trigger_event(_entity, 'thrust')
	
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
		entities.trigger_event(_entity, 'set_direction', direction=_move_direction)
		entities.trigger_event(_entity, 'set_speed', speed=2)
		entities.trigger_event(_entity, 'set_minimum_velocity', velocity=[-5, -5])
		entities.trigger_event(_entity, 'set_maximum_velocity', velocity=[5, 5])
		entities.trigger_event(_entity, 'thrust')
	
	LEVEL += 1
	ANNOUNCE = True

def tick():
	global WAVE_TIMER
	
	if WAVE_TIMER:
		WAVE_TIMER -= 1

def loop():
	global CHANGE_LEVEL_FIRE, TRANSITION_PAUSE, CHANGE_LEVEL, WAVE_TIMER, LEVEL
	
	print TRANSITION_PAUSE, CHANGE_LEVEL
	
	if TRANSITION_PAUSE and CHANGE_LEVEL:
		_player = entities.get_entity(entities.get_entity_group('players')[0])
		
		if not CHANGE_LEVEL_FIRE:
			events.unregister_event('input', player.handle_input)
			entities.trigger_event(_player,
			                       'create_timer',
			                       time=240,
			                       callback=lambda entity: entities.trigger_event(entity, 'push', velocity=(5, 5)),
			                       exit_callback=lambda entity: events.register_event('input', player.handle_input, _player['_id']))
			
			_player['NO_BOUNCE'] = True
			CHANGE_LEVEL_FIRE = True
		
		return False
	
	if TRANSITION_PAUSE:
		TRANSITION_PAUSE -= 1
		
		return False
	else:
		if CHANGE_LEVEL:
			LEVEL = 1
		
		CHANGE_LEVEL = False
	
	if not entities.get_entity_group('enemies') and not entities.get_entity_group('hazards'):
		WAVE_TIMER = 0
	
	if entities.get_entity_group('players') and not WAVE_TIMER:
		spawn_enemies()
		WAVE_TIMER = WAVE_TIMER_MAX+(60*LEVEL)
