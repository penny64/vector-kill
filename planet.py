import movement
import entities
import display
import sprites
import numbers
import player
import events
import worlds
import ships
import clock
import maps

import random

LEVEL = 1
NOTERIETY = 0
TRANSITION_PAUSE = 0
ANNOUNCE = True
WAVE_TIMER_MAX = 30*15
WAVE_TIMER = 0

def create():
	global LEVEL
	
	LEVEL = 1
	
	worlds.create('planet', width=9000, height=9000)
	_planet = entities.create_entity(group='planets')
	sprites.register_entity(_planet, 'effects_foreground', 'planet.png', scale=1.8)
	movement.register_entity(_planet, x=worlds.get_size()[0]/2, y=worlds.get_size()[0]/2, speed=0)
	events.register_event('tick', tick)
	
	create_player()
	display.create_grid()

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
		
def create_player():
	_player = ships.create_energy_ship()
	_player['player'] = True
	
	player.register_entity(_player)
	events.register_event('input', player.handle_input, _player['_id'])
	events.register_event('camera', player.handle_camera, _player['_id'], min_zoom=5, max_zoom=14, max_enemy_distance=10000, center_distance=5000)
	entities.register_event(_player, 'delete', player.delete)
	entities.register_event(_player, 'hit_edge', lambda entity: entity['current_speed']>40 and entities.trigger_event(entity, 'hit', damage=entity['current_speed']-40))

def spawn_enemies():
	global TRANSITION_PAUSE, ANNOUNCE, LEVEL
	
	_i = random.choice([0, 1, 2, 3])
	
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
	
	if LEVEL == 5:
		_boss = ships.create_ivan(x=random.randint(0, worlds.get_size()[0]), y=random.randint(0, worlds.get_size()[1]))
		_details = ['<b>Stolovitzky, Ivan</b>',
		            '<i>Suicidal maniac</i>',
		            'Wanted for: <b>Intergalactic Manslaughter</b>']
		
		display.camera_zoom(1.5)
		display.camera_focus_on(_boss['position'])
		display.clear_text_group('bot_center')
		display.print_text(display.get_window_size()[0]/2,
		                   display.get_window_size()[1]*.75,
		                   'CRAZY IVAN',
		                   font_size=42,
		                   text_group='bot_center',
		                   center=True,
		                   color=(0, 240, 0, 50),
		                   fade_in_speed=24,
		                   show_for=3)
		
		_i = 0
		for detail_text in _details:
			display.print_text(display.get_window_size()[0]*.6,
			                   display.get_window_size()[1]*.65-(24*_i),
			                   detail_text,
			                   font_size=20,
			                   text_group='bot_center',
			                   color=(240, 240, 240, 0),
			                   fade_in_speed=(len(_details)-_i)*2,
			                   show_for=3)
			_i += 1
		
		clock.hang_for(180)
		#entities.register_event(_boss, 'kill', lambda entity: progress.unlock_chaingun())
		
		TRANSITION_PAUSE = 240
		ANNOUNCE = True
		LEVEL += 1
		
		return False
	
	if not LEVEL % 4:
		for i in range(1*(LEVEL-1)):
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
			
			ships.create_flea(x=_x, y=_y)
		
		TRANSITION_PAUSE = 120
		ANNOUNCE = True
		LEVEL += 1
		
		return False
	
	for i in range(1*(LEVEL-1)):
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
		
		ships.create_flea(x=_x, y=_y, hazard=True)
	
	#_eyemine_spawn_point = (random.randint(worlds.get_size()[0]*.25, worlds.get_size()[0]*.75),
	#                        random.randint(worlds.get_size()[1]*.25, worlds.get_size()[1]*.75))
	#for i in range(random.randint(2, 4)*LEVEL):
	#	_rand_distance = 350+(120*LEVEL)
	#	_x_mod = random.randint(-_rand_distance, _rand_distance)
	#	_y_mod = random.randint(-_rand_distance, _rand_distance)
	#	ships.create_eyemine(x=_eyemine_spawn_point[0]+_x_mod, y=_eyemine_spawn_point[1]+_y_mod)
	#
	
	for i in range(random.randint(1, 2)*LEVEL):
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
		
		_move_direction = numbers.direction_to((_x, _y,), (worlds.get_size()[0]/2, worlds.get_size()[1]/2))
		_turret = ships.create_missile_turret(x=_x, y=_y)
		
		entities.trigger_event(_turret, 'set_direction', direction=_move_direction)
		entities.trigger_event(_turret, 'set_speed', speed=2)
		entities.trigger_event(_turret, 'set_minimum_velocity', velocity=[-5, -5])
		entities.trigger_event(_turret, 'set_maximum_velocity', velocity=[5, 5])
		entities.trigger_event(_turret, 'thrust')

	if LEVEL >= 3:
		for i in range(random.randint(1, 2)*(int(round(LEVEL*.25)))):
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
			
			_turret = ships.create_gun_turret(x=_x, y=_y)
			_move_direction = numbers.direction_to((_x, _y,), (worlds.get_size()[0]/2, worlds.get_size()[1]/2))
			
			entities.trigger_event(_turret, 'set_direction', direction=_move_direction)
			entities.trigger_event(_turret, 'set_speed', speed=2)
			entities.trigger_event(_turret, 'set_minimum_velocity', velocity=[-5, -5])
			entities.trigger_event(_turret, 'set_maximum_velocity', velocity=[5, 5])
			entities.trigger_event(_turret, 'thrust')
	
	if 1*(LEVEL-1):
		display.clear_text_group('bot_center')
		display.print_text(display.get_window_size()[0]/2,
		                   display.get_window_size()[1]*.95,
		                   'ENEMY FIGHTERS INBOUND',
		                   color=(0, 240, 0, 255),
		                   text_group='bot_center',
		                   show_for=1.5,
		                   center=True)
	
	LEVEL += 1
	ANNOUNCE = True
	TRANSITION_PAUSE = 120


def tick():
	global WAVE_TIMER
	
	if WAVE_TIMER:
		WAVE_TIMER -= 1

def loop():
	global WAVE_TIMER
	
	if entities.get_entity_group('players') and not WAVE_TIMER:
		spawn_enemies()
		WAVE_TIMER = WAVE_TIMER_MAX+(10*LEVEL)
