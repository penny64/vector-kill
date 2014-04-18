import entities
import display
import player
import events
import ships

import random


def create():
	display.create_sprite_group('effects_background')
	display.create_sprite_group('effects_foreground')
	display.create_sprite_group('soldiers')
	entities.create_entity_group('soldiers')
	
	_player = ships.create_energy_ship()
	_player['player'] = True

	events.register_event('input', player.handle_input, _player['_id'])
	events.register_event('camera', player.handle_camera, _player['_id'])
	entities.register_event(_player, 'score', player.score)
	entities.trigger_event(_player, 'accelerate', velocity=[45, 3])
	
	for i in range(5):
		_enemy = ships.create_eyemine(x=random.randint(0, 1000), y=random.randint(0, 1000))
