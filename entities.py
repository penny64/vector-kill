import worlds


ENTITIES = {}
NEXT_ENTITY_ID = 1


def create_entity():
	_entity = {'_id': str(NEXT_ENTITY_ID)}
	
	ENTITIES[_entity['_id']] = _entity
	
	worlds.register_entity(_entity)
	
	return _entity

		
		