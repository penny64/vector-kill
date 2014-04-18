import entities
import soldier
import display
import player
import events
import ai


def create():
	display.create_sprite_group('effects_background')
	display.create_sprite_group('effects_foreground')
	display.create_sprite_group('soldiers')
	entities.create_entity_group('soldiers')
	
	_player = soldier.create_energy_ship()

	events.register_event('input', player.handle_input, _player['_id'])
	events.register_event('camera', player.handle_camera, _player['_id'])
	entities.register_event(_player, 'score', player.score)
	entities.trigger_event(_player, 'accelerate', velocity=[45, 3])
	
	for i in range(1):
		_enemy = soldier.create_eyemine()
		
		ai.register_entity(_enemy)
		entities.trigger_event(_enemy, 'accelerate', velocity=[45, 45])
