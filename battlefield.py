import entities
import soldier
import display
import player
import events


def create():
	display.create_sprite_group('soldiers')
	
	_player = soldier.create()

	events.register_event('input', player.handle_input, _player['_id'])
	events.register_event('camera', player.handle_camera, _player['_id'])
	entities.trigger_event(_player, 'accelerate', velocity=[45, 3])
	
	for i in range(2):
		soldier.create()
