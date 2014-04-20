import display
import worlds
import events

import time


ENTITIES = {}
ENTITIES_TO_DELETE = set()
NEXT_ENTITY_ID = 1
GROUPS = {}
TICKS_PER_SECOND = 0
CURRENT_TICKS_PER_SECOND = 0
LAST_TICK_TIME = time.time()


def boot():
	events.register_event('tick', tick)
	events.register_event('loop', loop)
	events.register_event('cleanup', cleanup)

def create_entity():
	global NEXT_ENTITY_ID
	
	_entity = {'_id': str(NEXT_ENTITY_ID),
	           '_events': {},
	           '_groups': []}
	
	ENTITIES[_entity['_id']] = _entity
	
	worlds.register_entity(_entity)
	create_event(_entity, 'delete')
	create_event(_entity, 'create')
	create_event(_entity, 'loop')
	create_event(_entity, 'tick')
	
	NEXT_ENTITY_ID += 1
	
	return _entity

def delete_all():
	ENTITIES_TO_DELETE.update(ENTITIES.keys())

def delete_entity(entity):
	ENTITIES_TO_DELETE.add(entity['_id'])

def get_entity(entity_id):
	return ENTITIES[entity_id]

def create_entity_group(group_name):
	GROUPS[group_name] = []

def get_sprite_group(group_name):
	return GROUPS[group_name]

def get_sprite_groups(group_names):
	_entities = []
	
	for group_name in group_names:
		_entities.extend(GROUPS[group_name])
	
	return [entity_id for entity_id in _entities if entity_id in ENTITIES]

def add_entity_to_group(group_name, entity):
	entity['_groups'].append(group_name)
	GROUPS[group_name].append(entity['_id'])

def remove_entity_from_group(entity, group_name):
	if not entity['_id'] in GROUPS[group_name]:
		print('Trying to remove entity from a group it isn\'t in: %s (%s)' % (entity['_id'], group_name))
		
		return False
	
	GROUPS[group_name].remove(entity['_id'])
	entity['_groups'].remove(group_name)

def remove_entity_from_all_groups(entity):
	for group_name in entity['_groups']:
		remove_entity_from_group(entity, group_name)

def create_event(entity, event_name):
	entity['_events'][event_name] = []

def register_event(entity, event_name, callback):
	entity['_events'][event_name].append(callback)

def unregister_event(entity, event_name, callback):
	entity['_events'][event_name].remove(callback)

def trigger_event(entity, event_name, **kwargs):
	for event in entity['_events'][event_name]:
		event(entity, **kwargs)

def tick():
	global LAST_TICK_TIME, TICKS_PER_SECOND, CURRENT_TICKS_PER_SECOND
	
	for entity in ENTITIES.values():
		trigger_event(entity, 'tick')
	
	if time.time()-LAST_TICK_TIME>=1:
		LAST_TICK_TIME = time.time()
		TICKS_PER_SECOND = CURRENT_TICKS_PER_SECOND
		CURRENT_TICKS_PER_SECOND = 0
	else:
		CURRENT_TICKS_PER_SECOND += 1

def loop():
	for entity in ENTITIES.values():
		trigger_event(entity, 'loop')

def cleanup():
	global ENTITIES_TO_DELETE
	
	while ENTITIES_TO_DELETE:
		_entity_id = ENTITIES_TO_DELETE.pop()
		
		if not _entity_id in ENTITIES:
			continue
		
		_entity = ENTITIES[_entity_id]
		
		trigger_event(_entity, 'delete')
		remove_entity_from_all_groups(_entity)
		
		del ENTITIES[_entity_id]
	
	ENTITIES_TO_DELETE = set()