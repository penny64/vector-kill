import entities

import numbers

def track_target(entity, target_id):
	entity['current_target'] = target_id

	entities.register_event(entity, 'tick', tick_track)

def guard(entity):
	entities.register_event(entity, 'tick', tick_guard)

def tick_track(entity):
	#_target_id = find_target(entity)
	_target_id = entity['current_target']
	
	if entity['hp']<=0:
		entities.unregister_event(entity, 'tick', tick)
		
		return False
	
	if not _target_id:
		entities.trigger_event(entity, 'accelerate', velocity=(0, 0))
		
		return False
	
	_target = entities.get_entity(_target_id)
	_direction_to = numbers.direction_to(entity['position'], _target['position'])
	_degrees_to = abs(entity['direction']-_direction_to)
	
	if _degrees_to>=180:
		_direction_to += 360
	
	_new_direction = numbers.interp(entity['direction'], _direction_to, 0.1)
	_direction_difference = abs(entity['direction']-_new_direction)
	entity['direction'] = _new_direction
	entity['velocity'] = numbers.velocity(entity['direction'], 10)

def tick_guard(entity):
	_target_id = find_target(entity, max_distance=500)


def find_target(entity, max_distance=-1):
	_closest_target = {'enemy_id': None, 'distance': 0}
	
	for soldier_id in entities.get_sprite_group('soldiers'):
		if entity['_id'] == soldier_id or not 'player' in entities.get_entity(soldier_id):
			continue
		
		_distance = numbers.distance(entity['position'], entities.get_entity(soldier_id)['position'])
		
		if max_distance>-1 and _distance>max_distance:
			continue
		
		if not _closest_target['enemy_id'] or _distance<_closest_target['distance']:
			_closest_target['distance'] = _distance
			_closest_target['enemy_id'] = soldier_id
	
	return _closest_target['enemy_id']