import entities
import controls
import display
import numbers


def handle_input(entity_id):
	_entity = entities.get_entity(entity_id)
	
	if controls.key_pressed('d') or controls.key_held('d'):
		entities.trigger_event(_entity, 'accelerate', velocity=[6, 0])
	
	if controls.key_pressed('a') or controls.key_held('a'):
		entities.trigger_event(_entity, 'accelerate', velocity=[-6, 0])
	
	if controls.key_pressed('a') or controls.key_held('w'):
		entities.trigger_event(_entity, 'accelerate', velocity=[0, -6])
	
	if controls.key_pressed('a') or controls.key_held('s'):
		entities.trigger_event(_entity, 'accelerate', velocity=[0, 6])
	
	if controls.key_pressed_ord(controls.NUM_2):
		entities.trigger_event(_entity, 'shoot', direction=270)
	
	if controls.key_pressed_ord(controls.NUM_4):
		entities.trigger_event(_entity, 'shoot', direction=180)
	
	if controls.key_pressed_ord(controls.NUM_6):
		entities.trigger_event(_entity, 'shoot', direction=0)
	
	if controls.key_pressed_ord(controls.NUM_8):
		entities.trigger_event(_entity, 'shoot', direction=90)

def handle_camera(entity_id):
	_player = entities.get_entity(entity_id)
	
	if '2' in entities.ENTITIES:
		_enemy = entities.get_entity('2')
	else:
		_enemy = _player
	
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

def score(entity, target_id):
	display.print_text(0, 10+(len(display.LABELS)*15), 'Kill (<b>+1XP</b>)', color=(0, 240, 0, 255), show_for=1.5)
	