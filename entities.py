import display
import worlds
import events

import time


ENTITIES = {}
ENTITIES_TO_DELETE = set()
NEXT_ENTITY_ID = 1
REVOKED_ENTITY_IDS_HOLDING = set()
REVOKED_ENTITY_IDS = set()
CLEANING = False
GROUPS = {}
TICKS_PER_SECOND = 0
CURRENT_TICKS_PER_SECOND = 0
LAST_TICK_TIME = time.time()


def boot():
	events.register_event('tick', tick)
	events.register_event('loop', loop)
	events.register_event('cleanup', cleanup)

def create_entity(group=None):
	global NEXT_ENTITY_ID
	
	if REVOKED_ENTITY_IDS:
		_entity_id = REVOKED_ENTITY_IDS.pop()
	else:
		_entity_id = str(NEXT_ENTITY_ID)
		NEXT_ENTITY_ID += 1
	
	_entity = {'_id': _entity_id,
	           '_events': {},
	           '_groups': [],
	           '_groups_orig': []}
	
	ENTITIES[_entity['_id']] = _entity
	
	worlds.register_entity(_entity)
	create_event(_entity, 'delete')
	create_event(_entity, 'create')
	create_event(_entity, 'loop')
	create_event(_entity, 'tick')
	
	if group:
		add_entity_to_group(group, _entity)
	
	return _entity

def delete_all():
	ENTITIES_TO_DELETE.update(ENTITIES.keys())

def delete_entity(entity):
	if not entity['_id'] in ENTITIES:
		
		return False
	
	ENTITIES_TO_DELETE.add(entity['_id'])

def delete_entity_via_id(entity_id):
	if not entity_id in ENTITIES:
		
		return False
	
	ENTITIES_TO_DELETE.add(entity_id)

def get_entity(entity_id):
	return ENTITIES[entity_id]

def create_entity_group(group_name):
	if group_name in GROUPS:
		raise Exception('Trying to create duplicate entity group:' % group_name)
	
	GROUPS[group_name] = []

def get_entity_group(group_name):
	return GROUPS[group_name]

def get_sprite_groups(group_names):
	_entities = []
	
	for group_name in group_names:
		_entities.extend(GROUPS[group_name])
	
	return [entity_id for entity_id in _entities if entity_id in ENTITIES]

def add_entity_to_group(group_name, entity):
	entity['_groups'].append(group_name)
	entity['_groups_orig'].append(group_name)
	GROUPS[group_name].append(entity['_id'])

def remove_entity_from_group(entity, group_name):
	if not entity['_id'] in GROUPS[group_name]:
		print('Trying to remove entity from a group it isn\'t in: %s (%s)' % (entity['_id'], group_name))
		entity['_groups'].remove(group_name)
		
		return False
	
	GROUPS[group_name].remove(entity['_id'])
	entity['_groups'].remove(group_name)

def remove_entity_from_all_groups(entity):
	for group_name in entity['_groups'][:]:
		remove_entity_from_group(entity, group_name)

def create_event(entity, event_name):
	entity['_events'][event_name] = {'events': {}, 'id': 1, 'banned': set()}

def register_event(entity, event_name, callback):
	_event_structure = entity['_events'][event_name]
	_event = {'callback': callback,
	          'id': str(_event_structure['id'])}
	_event_structure['events'][str(_event_structure['id'])] = _event
	_event_structure['id'] += 1

def unregister_event(entity, event_name, callback):
	_event_structure = entity['_events'][event_name]
	
	for event in _event_structure['events'].values():
		if event['callback'] == callback:
			_event_structure['banned'].add(event['id'])
			
			del _event_structure['events'][event['id']]
			return True

def trigger_event(entity, event_name, **kwargs):
	_event_structure = entity['_events'][event_name]
	for event in _event_structure['events'].values():
		if event['id'] in _event_structure['banned']:
			_event_structure['banned'].remove(event['id'])
			
			continue
		
		event['callback'](entity, **kwargs)

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

def reset():
	global REVOKED_ENTITY_IDS_HOLDING, REVOKED_ENTITY_IDS
	
	REVOKED_ENTITY_IDS.update(REVOKED_ENTITY_IDS_HOLDING)
	REVOKED_ENTITY_IDS_HOLDING = set()

def cleanup():
	global ENTITIES_TO_DELETE, CLEANING
	
	CLEANING = True
	
	while ENTITIES_TO_DELETE:
		_entity_id = ENTITIES_TO_DELETE.pop()
		
		if not _entity_id in ENTITIES:
			remove_entity_from_all_groups(_entity)
			
			continue
		
		_entity = ENTITIES[_entity_id]
		
		trigger_event(_entity, 'delete')
		remove_entity_from_all_groups(_entity)
		REVOKED_ENTITY_IDS_HOLDING.add(_entity_id)
		
		del ENTITIES[_entity_id]
	
	ENTITIES_TO_DELETE = set()
	CLEANING = False