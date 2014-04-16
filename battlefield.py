import soldier
import display
import player
import events


def create():
	display.create_sprite_group('soldiers')
	
	_player_id = soldier.create()

	events.register_event('input', player.handle_input, _player_id['_id'])
	events.register_event('camera', player.handle_camera, _player_id['_id'])
	
	for i in range(2):
		soldier.create()
