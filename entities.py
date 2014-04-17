import display
import worlds
import events


ENTITIES = {}
ENTITIES_TO_DELETE = set()
NEXT_ENTITY_ID = 1
GROUPS = {}


def boot():
	events.register_event('tick', tick)
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
	register_event(_entity, 'delete', remove_entity_from_all_groups)
	
	NEXT_ENTITY_ID += 1
	
	return _entity

def delete_entity(entity):
	ENTITIES_TO_DELETE.add(entity['_id'])

def get_entity(entity_id):
	return ENTITIES[entity_id]

def create_entity_group(group_name):
	GROUPS[group_name] = []

def get_sprite_group(group_name):
	return GROUPS[group_name]

def add_entity_to_group(group_name, entity):
	entity['_groups'].append(group_name)
	GROUPS[group_name].append(entity['_id'])

def remove_entity_from_group(entity, group_name):
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
	for entity in ENTITIES.values():
		trigger_event(entity, 'tick')

def cleanup():
	global ENTITIES_TO_DELETE
	
	for entity_id in ENTITIES_TO_DELETE:
		trigger_event(ENTITIES[entity_id], 'delete')
		
		del ENTITIES[entity_id]
	
	ENTITIES_TO_DELETE = set()