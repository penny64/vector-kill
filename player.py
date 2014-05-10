import battlefield
import entities
import controls
import display
import numbers
import bullet
import worlds
import events
import clock
import menu
import ai

import time


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
	
	if not clock.is_ticking() and controls.key_pressed(' '):
		clock.hang_for(0)
	
	_entity = entities.get_entity(entity_id)
	_move_speed = _entity['speed']
	
	if controls.key_held('s'):
		#entities.trigger_event(_entity, 'accelerate', velocity=[0, _move_speed])
		entities.trigger_event(_entity, 'set_direction', direction=270)
		entities.trigger_event(_entity, 'thrust')
	
	if controls.key_held('a'):
		#entities.trigger_event(_entity, 'accelerate', velocity=[-_move_speed, 0])
		entities.trigger_event(_entity, 'set_direction', direction=180)
		entities.trigger_event(_entity, 'thrust')
	
	if controls.key_held('d'):
		#entities.trigger_event(_entity, 'accelerate', velocity=[_move_speed, 0])
		entities.trigger_event(_entity, 'set_direction', direction=0)
		entities.trigger_event(_entity, 'thrust')
	
	if controls.key_held('w'):
		#entities.trigger_event(_entity, 'accelerate', velocity=[0, -_move_speed])
		entities.trigger_event(_entity, 'set_direction', direction=90)
		entities.trigger_event(_entity, 'thrust')
	
	if controls.key_pressed('q'):
		entities.trigger_event(_entity,
		                       'create_timer',
		                       time=120,
		                       enter_callback=lambda entity: entities.trigger_event(_entity, 'set_maximum_velocity', velocity=[80, 80]) and entities.trigger_event(_entity, 'set_speed', speed=80),
		                       exit_callback=lambda entity: entities.trigger_event(_entity, 'set_maximum_velocity', velocity=[30, 30]))
	
	if controls.key_pressed('v'):
		for entity_id in entities.get_sprite_groups(['hazards', 'enemies']):
			entities.delete_entity_via_id(entity_id)
	
	if controls.key_held_ord(controls.NUM_1):
		entities.trigger_event(_entity, 'shoot', direction=225)
	
	if controls.key_held_ord(controls.NUM_2):
		entities.trigger_event(_entity, 'shoot', direction=270)
	
	if controls.key_held_ord(controls.NUM_3):
		entities.trigger_event(_entity, 'shoot', direction=315)
	
	if controls.key_held_ord(controls.NUM_4):
		entities.trigger_event(_entity, 'shoot', direction=180)
	
	if controls.key_held_ord(controls.NUM_6):
		entities.trigger_event(_entity, 'shoot', direction=0)
	
	if controls.key_held_ord(controls.NUM_7):
		entities.trigger_event(_entity, 'shoot', direction=135)
	
	if controls.key_held_ord(controls.NUM_8):
		entities.trigger_event(_entity, 'shoot', direction=90)
	
	if controls.key_held_ord(controls.NUM_9):
		entities.trigger_event(_entity, 'shoot', direction=45)
	
	if controls.key_held_ord(controls.NUM_5):
		entities.trigger_event(_entity, 'shoot_alt')
	
	if controls.key_held('x'):
		battlefield.clean()

def handle_camera(entity_id, min_zoom=3.5, max_zoom=14.5, max_enemy_distance=2400, center_distance=600.0):
	if not entity_id in entities.ENTITIES:
		display.CAMERA['zoom_speed'] = .005
		display.CAMERA['next_zoom'] = 4.5
		
		return False
	
	if not clock.is_ticking():
		return False
	
	_player = entities.get_entity(entity_id)
	_center_pos = _player['position'].copy()
	_median_distance = []
	
	if 'in_space' in _player and _player['in_space']:
		_distance_to_center = numbers.distance(_player['position'], (worlds.get_size()[0]/2, worlds.get_size()[1]/2))
		
		_min_zoom = 2.0
		_max_zoom = max_zoom
		display.CAMERA['next_zoom'] = numbers.clip(_max_zoom*((_distance_to_center/3000.0)-1), _min_zoom, _max_zoom)
	
	elif _player['death_timer'] == -1:
		for enemy_id in entities.get_sprite_groups(['enemies', 'hazards']):
			_enemy = entities.get_entity(enemy_id)
			
			if 'player' in _enemy:
				continue
			
			_dist = numbers.distance(_player['position'], _enemy['position'])
			if _dist>=max_enemy_distance:
				continue
			
			_median_distance.append(_dist)
			_center_pos = numbers.interp_velocity(_center_pos, _enemy['position'], 0.5)
		
		if not _median_distance:
			_median_distance = [0]
		
		_distance_to_nearest_enemy = sum(_median_distance)/len(_median_distance)
		_min_zoom = min_zoom
		_max_zoom = max_zoom
		display.CAMERA['next_zoom'] = numbers.clip(_max_zoom*(_distance_to_nearest_enemy/float(center_distance)), _min_zoom, _max_zoom)
	else:
		display.CAMERA['zoom_speed'] = .05
		display.CAMERA['next_zoom'] = 1.5
	
	if display.CAMERA['next_zoom'] < 5:
		display.CAMERA['next_center_on'] = _center_pos
	else:
		display.CAMERA['next_center_on'] = _player['position'].copy()

def score(entity, target_id, amount=0, text=''):
	display.print_text(0, 10+(len(display.LABELS)*15), '%s (<b>+%s</b>)' % (text, amount), color=(0, 240, 0, 255), show_for=1.5)
	
	if target_id in entities.ENTITIES and abs(entity['shoot_direction']-numbers.direction_to(entity['position'], entities.get_entity(target_id)['position']))<45:
		display.print_text(0, 10+(len(display.LABELS)*15), 'FRENZY!!!', color=(0, 240, 0, 255), show_for=1.5)

def delete(entity):
	time.sleep(.75)
	display.clear_text_group('bot_center')
	
	#TODO: Let menu take over
	display.CAMERA['zoom_speed'] = .09
	display.CAMERA['next_zoom'] = 4.5
	display.CAMERA['camera_move_speed'] = 0.02
	
	#NOTERIETY -= entities.get_entity_group('enemies')
	
	events.unregister_event('camera', handle_camera)
	menu.setup_main_menu()
	
	_enemy_amount = len(entities.get_entity_group('enemies'))
	
	if _enemy_amount>=3:
		_loss_string = 'Pirates spread the news of your death...'
	elif _enemy_amount:
		_loss_string = 'People think a little less of you now...'
	else:
		_loss_string = 'Only the machines saw your death...'
	
	display.print_text(display.get_window_size()[0]/2,
	                   display.get_window_size()[1]*.25,
	                   _loss_string,
	                   text_group='bot_center',
	                   color=(255, 0, 0, 0),
	                   show_for=6,
	                   fade_in_speed=4,
	                   center=True)
