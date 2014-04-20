import entities

import numbers

def register_entity(entity):
	entity['current_target'] = None

def track_target(entity, target_id):
	register_entity(entity)
	entities.register_event(entity, 'tick', tick_track)
	
	entity['current_target'] = target_id

def guard(entity):
	register_entity(entity)
	entities.register_event(entity, 'tick', tick_guard)

def tick_track(entity):
	#_target_id = find_target(entity)
	_target_id = entity['current_target']
	
	if entity['hp']<=0 or not _target_id in entities.ENTITIES:
		entity['current_target'] = None
		entities.unregister_event(entity, 'tick', tick_track)
		
		return False
	
	if not _target_id:
		entities.trigger_event(entity, 'accelerate', velocity=(0, 0))
		
		return False
	
	_target = entities.get_entity(_target_id)
	_direction_to = numbers.direction_to(entity['position'], _target['position'])
	_degrees_to = abs(entity['direction']-_direction_to)
	
	if _degrees_to>=180:
		_direction_to += 360
	
	_new_direction = numbers.interp(entity['direction'], _direction_to, entity['turn_rate'])
	_direction_difference = abs(entity['direction']-_new_direction)
	entity['direction'] = _new_direction
	entities.trigger_event(entity, 'thrust')

def tick_guard(entity):
	if entity['hp']<=0:
		entities.unregister_event(entity, 'tick', tick_guard)
		
		return False
	
	if not entity['current_target']:
		_target_id = find_target(entity, max_distance=350)
		
		if _target_id:
			entities.trigger_event(entity, 'set_direction', direction=numbers.direction_to(entity['position'], entities.get_entity(_target_id)['position']))
			track_target(entity, _target_id)

def find_target(entity, max_distance=-1):
	_closest_target = {'enemy_id': None, 'distance': 0}
	_enemy_sprite_groups = [name for name in entities.GROUPS if not name in entity['_groups']]
	
	for soldier_id in entities.get_sprite_groups(_enemy_sprite_groups):
		if entity['_id'] == soldier_id:
			continue
		
		_distance = numbers.distance(entity['position'], entities.get_entity(soldier_id)['position'])
		
		if max_distance>-1 and _distance>max_distance:
			continue
		
		if not _closest_target['enemy_id'] or _distance<_closest_target['distance']:
			_closest_target['distance'] = _distance
			_closest_target['enemy_id'] = soldier_id
	
	return _closest_target['enemy_id']