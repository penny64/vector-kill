import display
import worlds
import events


ENTITIES = {}
NEXT_ENTITY_ID = 1


def create_entity():
	global NEXT_ENTITY_ID
	
	_entity = {'_id': str(NEXT_ENTITY_ID),
	           '_events': {}}
	
	ENTITIES[_entity['_id']] = _entity
	
	worlds.register_entity(_entity)
	events.register_event('tick', tick, _entity)
	
	NEXT_ENTITY_ID += 1
	
	return _entity

def get_entity(entity_id):
	return ENTITIES[entity_id]

def create_event(entity, event_name):
	entity['_events'][event_name] = []

def register_event(entity, event_name, callback):
	entity['_events'][event_name].append(callback)

def trigger_event(entity, event_name, **kwargs):
	for event in entity['_events'][event_name]:
		event(entity, **kwargs)

def tick(entity):
	pass
