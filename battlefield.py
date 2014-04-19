import entities
import display
import player
import events
import ships

import random


def boot():
	display.create_sprite_group('effects_background')
	display.create_sprite_group('effects_foreground')

def clean():
	for ship_id in entities.get_sprite_group('soldiers'):
		entities.delete_entity(entities.ENTITIES[ship_id])

def create():
	display.create_sprite_group('soldiers')
	entities.create_entity_group('soldiers')
	
	_player = ships.create_energy_ship()
	_player['player'] = True

	events.register_event('input', player.handle_input, _player['_id'])
	events.register_event('camera', player.handle_camera, _player['_id'])
	entities.register_event(_player, 'score', player.score)
	entities.register_event(_player, 'delete', player.delete)
	
	spawn_enemies()

def spawn_enemies():
	for i in range(3):
		ships.create_eyemine(x=random.randint(0, 1000), y=random.randint(0, 1000))
	
	for i in range(3):
		ships.create_missile_turret(x=random.randint(0, 1000), y=random.randint(0, 1000))

def loop():
	if len(entities.get_sprite_group('soldiers')) == 1:
		spawn_enemies()
		