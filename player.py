import entities
import controls
import display
import numbers


def handle_input(entity_id):
	_entity = entities.get_entity(entity_id)
	
	if controls.key_pressed('d') or controls.key_held('d'):
		entities.trigger_event(_entity, 'accelerate', velocity=[3, 0])
	
	if controls.key_pressed('a') or controls.key_held('a'):
		entities.trigger_event(_entity, 'accelerate', velocity=[-3, 0])
	
	if controls.key_pressed('a') or controls.key_held('w'):
		entities.trigger_event(_entity, 'accelerate', velocity=[0, -3])
	
	if controls.key_pressed('a') or controls.key_held('s'):
		entities.trigger_event(_entity, 'accelerate', velocity=[0, 3])
	
	if controls.key_pressed_ord(controls.NUM_4) or controls.key_held_ord(controls.NUM_4):
		print 'dero'

def handle_camera(entity_id):
	_player = entities.get_entity(entity_id)
	_enemy = entities.get_entity('2')
	_distance_to_nearest_enemy = numbers.distance(_player['position'], _enemy['position'], old=True)
	_min_zoom = 1.5
	_max_zoom = 3.0
	
	display.CAMERA['next_zoom'] = numbers.clip(_distance_to_nearest_enemy/400.0, _min_zoom, _max_zoom)
	
	if display.CAMERA['next_zoom'] < 5:
		display.CAMERA['next_center_on'] = numbers.interp_velocity(_player['position'][:],
		                                                           _enemy['position'],
		                                                           1-(display.CAMERA['next_zoom']/_max_zoom))
	else:
		display.CAMERA['next_center_on'] = _player['position'][:]	
