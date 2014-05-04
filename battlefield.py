import entities
import display
import player
import events
import worlds
import ships
import clock

import random


LEVEL = 1
NOTERIETY = 0
TRANSITION_PAUSE = 0
ANNOUNCE = True


def boot():
	display.create_sprite_group('effects_background')
	display.create_sprite_group('ships')
	display.create_sprite_group('effects_foreground')
	display.create_text_group('bot_center')
	
	entities.create_entity_group('players')
	entities.create_entity_group('enemies')
	entities.create_entity_group('hazards')
	entities.create_entity_group('effects')
	entities.create_entity_group('bullets')
	entities.create_entity_group('weapons')
	
	entities.create_entity_group('cursor')
	entities.create_entity_group('tiles_foreground')
	display.create_sprite_group('tiles_foreground')
	display.create_sprite_group('ui_foreground')

def clean():
	global LEVEL
	
	LEVEL = 1
	
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

def create(player=True):
	global LEVEL
	
	if player:
		create_player()
		LEVEL = 1
	else:
		LEVEL = 3
	
	spawn_enemies()
		
def create_player():
	_player = ships.create_energy_ship()
	_player['player'] = True
	
	player.register_entity(_player)
	events.register_event('input', player.handle_input, _player['_id'])
	events.register_event('camera', player.handle_camera, _player['_id'])
	entities.register_event(_player, 'score', player.score)
	entities.register_event(_player, 'delete', player.delete)

def spawn_enemies():
	global TRANSITION_PAUSE, ANNOUNCE, LEVEL
	
	if LEVEL == 5:
		_boss = ships.create_ivan(x=random.randint(0, worlds.get_size()[0]), y=random.randint(0, worlds.get_size()[1]))
		
		display.camera_zoom(1.5)
		display.camera_focus_on(_boss['position'])
		display.clear_text_group('bot_center')
		display.print_text(display.get_window_size()[0]/2, display.get_window_size()[1]*.75, 'CRAZY IVAN', font_size=42, text_group='bot_center', center=True, color=(0, 240, 0, 50), fade_in_speed=24, show_for=3)
		clock.hang_for(180)
		
		TRANSITION_PAUSE = 240
		ANNOUNCE = True
		LEVEL += 1
		
		return False
	
	if not LEVEL % 4:
		for i in range(1*(LEVEL-1)):
			ships.create_flea(x=random.randint(0, worlds.get_size()[0]), y=random.randint(0, worlds.get_size()[1]))
		
		TRANSITION_PAUSE = 120
		ANNOUNCE = True
		LEVEL += 1
		
		return False
	
	for i in range(1*(LEVEL-1)):
		ships.create_flea(x=random.randint(0, worlds.get_size()[0]), y=random.randint(0, worlds.get_size()[1]))
	
	_eyemine_spawn_point = (random.randint(worlds.get_size()[0]*.25, worlds.get_size()[0]*.75),
	                        random.randint(worlds.get_size()[1]*.25, worlds.get_size()[1]*.75))
	for i in range(random.randint(2, 4)*LEVEL):
		_rand_distance = 350+(120*LEVEL)
		_x_mod = random.randint(-_rand_distance, _rand_distance)
		_y_mod = random.randint(-_rand_distance, _rand_distance)
		ships.create_eyemine(x=_eyemine_spawn_point[0]+_x_mod, y=_eyemine_spawn_point[1]+_y_mod)
	
	_move = random.randint(0, 1)
	
	if _move:
		_move_direction = random.randint(0, 359)
	
	for i in range(random.randint(1, 2)*LEVEL):
		_x, _y = random.randint(worlds.get_size()[0]*.25, worlds.get_size()[0]*.75), random.randint(worlds.get_size()[1]*.25, worlds.get_size()[1]*.75)
		_turret = ships.create_missile_turret(x=_x, y=_y)
		
		if _move:
			entities.trigger_event(_turret, 'set_direction', direction=_move_direction)
			entities.trigger_event(_turret, 'set_minimum_velocity', velocity=[-5, -5])
			entities.trigger_event(_turret, 'set_maximum_velocity', velocity=[5, 5])
			entities.trigger_event(_turret, 'thrust')
	
	if LEVEL >= 3:
		for i in range(random.randint(1, 2)*(int(round(LEVEL*.25)))):
			_x, _y = random.randint(worlds.get_size()[0]*.25, worlds.get_size()[0]*.75), random.randint(worlds.get_size()[1]*.25, worlds.get_size()[1]*.75)
			_turret = ships.create_gun_turret(x=_x, y=_y)
			
			if _move:
				entities.trigger_event(_turret, 'set_direction', direction=_move_direction)
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

def loop():
	global TRANSITION_PAUSE, ANNOUNCE, NOTERIETY
	
	if entities.get_entity_group('players') and not entities.get_entity_group('enemies') and not entities.get_entity_group('hazards'):
		if TRANSITION_PAUSE:
			if ANNOUNCE:
				ANNOUNCE = False
				
				display.print_text(display.get_window_size()[0]/2,
				                   display.get_window_size()[1]*.95,
				                   'WAVE CLEARED',
				                   color=(200, 200, 200, 255),
				                   text_group='bot_center',
				                   show_for=2,
				                   center=True)
			
			TRANSITION_PAUSE -= 1
			
			return False
		
		NOTERIETY += LEVEL
		spawn_enemies()

def loop_attract():
	global TRANSITION_PAUSE, LEVEL
	
	if not entities.get_entity_group('enemies') or not entities.get_entity_group('hazards'):
		if TRANSITION_PAUSE:
			TRANSITION_PAUSE -= 1
		else:
			TRANSITION_PAUSE = 80
			clean()
			LEVEL = 3
			spawn_enemies()