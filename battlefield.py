import entities
import display
import player
import events
import worlds
import ships

import random


LEVEL = 1


def boot():
	display.create_sprite_group('effects_background')
	display.create_sprite_group('effects_foreground')
	display.create_text_group('top_center')

def clean():
	global LEVEL
	
	LEVEL = 1
	
	for ship_id in entities.get_sprite_group('soldiers'):
		entities.delete_entity(entities.ENTITIES[ship_id])

def create():
	display.create_sprite_group('soldiers')
	entities.create_entity_group('soldiers')
	entities.create_entity_group('players')
	entities.create_entity_group('enemies')
	entities.create_entity_group('hazards')
	
	_player = ships.create_energy_ship()
	_player['player'] = True
	
	player.register_entity(_player)

	events.register_event('input', player.handle_input, _player['_id'])
	events.register_event('camera', player.handle_camera, _player['_id'])
	entities.register_event(_player, 'score', player.score)
	entities.register_event(_player, 'delete', player.delete)
	
	spawn_enemies()

def spawn_enemies():
	global LEVEL
	
	display.clear_text_group('top_center')
	display.print_text(display.get_window_size()[0]/2,
	                   display.get_window_size()[1]*.85,
	                   'ENEMY FIGHTERS INBOUND', color=(0, 240, 0, 255), text_group='top_center', show_for=1.5, center=True)
	
	_eyemine_spawn_point = (random.randint(0, worlds.get_size()[0]), random.randint(0, worlds.get_size()[1]))
	for i in range(random.randint(2, 4)*LEVEL):
		_rand_distance = 350+(120*LEVEL)
		_x_mod = random.randint(-_rand_distance, _rand_distance)
		_y_mod = random.randint(-_rand_distance, _rand_distance)
		ships.create_eyemine(x=_eyemine_spawn_point[0]+_x_mod, y=_eyemine_spawn_point[1]+_y_mod)
	
	_move = random.randint(0, 1)
	
	if _move:
		_move_direction = random.randint(0, 359)
	
	for i in range(random.randint(1, 2)*LEVEL):
		_turret = ships.create_missile_turret(x=random.randint(0, worlds.get_size()[0]), y=random.randint(0, worlds.get_size()[1]))
		
		if _move:
			entities.trigger_event(_turret, 'set_direction', direction=_move_direction)
			entities.trigger_event(_turret, 'set_minimum_velocity', velocity=[-5, 5])
			entities.trigger_event(_turret, 'set_maximum_velocity', velocity=[-5, 5])
			entities.trigger_event(_turret, 'thrust')
	
	for i in range(1*(LEVEL-1)):
		ships.create_flea(x=random.randint(0, worlds.get_size()[0]), y=random.randint(0, worlds.get_size()[1]))
	
	LEVEL += 1

def loop():
	if len(entities.get_sprite_group('soldiers')) == 1:
		spawn_enemies()
		