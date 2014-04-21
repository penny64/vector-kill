import battlefield
import entities
import controls
import display
import numbers
import bullet
import ai


def register_entity(entity):
	entities.add_entity_to_group('players', entity)
	return entity

def handle_input(entity_id):
	if not entity_id in entities.ENTITIES or not 'player' in entities.ENTITIES[entity_id]:
		if controls.key_pressed(' '):
			battlefield.clean()
			battlefield.create_player()
			battlefield.spawn_enemies()
		
		return False
	
	_entity = entities.get_entity(entity_id)
	
	if controls.key_pressed_ord(controls.NUM_1) or controls.key_held_ord(controls.NUM_1):
		entities.trigger_event(_entity, 'accelerate', velocity=[-6, 6])
	
	if controls.key_pressed_ord(controls.NUM_2) or controls.key_held_ord(controls.NUM_2):
		entities.trigger_event(_entity, 'accelerate', velocity=[0, 6])
	
	if controls.key_pressed_ord(controls.NUM_3) or controls.key_held_ord(controls.NUM_3):
		entities.trigger_event(_entity, 'accelerate', velocity=[6, 6])
	
	if controls.key_pressed_ord(controls.NUM_4) or controls.key_held_ord(controls.NUM_4):
		entities.trigger_event(_entity, 'accelerate', velocity=[-6, 0])
	
	if controls.key_pressed_ord(controls.NUM_6) or controls.key_held_ord(controls.NUM_6):
		entities.trigger_event(_entity, 'accelerate', velocity=[6, 0])
	
	if controls.key_pressed_ord(controls.NUM_7) or controls.key_held_ord(controls.NUM_7):
		entities.trigger_event(_entity, 'accelerate', velocity=[-6, -6])
	
	if controls.key_pressed_ord(controls.NUM_8) or controls.key_held_ord(controls.NUM_8):
		entities.trigger_event(_entity, 'accelerate', velocity=[0, -6])
	
	if controls.key_pressed_ord(controls.NUM_9) or controls.key_held_ord(controls.NUM_9):
		entities.trigger_event(_entity, 'accelerate', velocity=[6, -6])
	
	if controls.key_held('q'):
		entities.trigger_event(_entity, 'shoot')
	
	if controls.key_pressed('w'):
		bullet.create_laser(_entity['position'][0], _entity['position'][1], _entity['shoot_direction'], _entity['_id'])
	
	if controls.key_held('x'):
		battlefield.clean()
	
	if controls.key_held('z'):
		display.screenshot()

def handle_camera(entity_id):
	if not entity_id in entities.ENTITIES:
		display.CAMERA['zoom_speed'] = .005
		display.CAMERA['next_zoom'] = 4.5
		
		return False
	
	_player = entities.get_entity(entity_id)
	_center_pos = _player['position'][:]
	
	for enemy_id in entities.get_sprite_group('soldiers'):
		_enemy = entities.get_entity(enemy_id)
		
		if 'player' in _enemy:
			continue
		
		if numbers.distance(_player['position'], _enemy['position'])>=1200:
			continue
		
		_center_pos = numbers.interp_velocity(_center_pos, _enemy['position'], 0.5)
	
	_enemy_id = ai.find_target(_player)
	
	if _enemy_id:
		_enemy = entities.get_entity(_enemy_id)
	else:
		_enemy = _player
	
	_distance_to_nearest_enemy = numbers.distance(_player['position'], _enemy['position'], old=True)
	_min_zoom = 3.0
	_max_zoom = 4.5
	display.CAMERA['next_zoom'] = numbers.clip(_distance_to_nearest_enemy/400.0, _min_zoom, _max_zoom)
	
	if display.CAMERA['next_zoom'] < 5:
		display.CAMERA['next_center_on'] = numbers.interp_velocity(_player['position'][:],
		                                                           _center_pos,
		                                                           1-(display.CAMERA['next_zoom']/_max_zoom))
	else:
		display.CAMERA['next_center_on'] = _player['position'][:]	

def score(entity, target_id):
	display.print_text(0, 10+(len(display.LABELS)*15), 'Kill (<b>+1XP</b>)', color=(0, 240, 0, 255), show_for=1.5)
	display.print_text(display.get_window_size()[0]/2, display.get_window_size()[1]*.85, 'Fragged <b>%s</b>' % target_id, color=(0, 240, 0, 255), text_group='top_center', show_for=1.5, center=True)

def delete(entity):
	display.clear_text_group('top_center')
	display.print_text(display.get_window_size()[0]/2, display.get_window_size()[1]*.85, 'GAME OVER', text_group='top_center', color=(255, 0, 0, 255), show_for=5, center=True)
