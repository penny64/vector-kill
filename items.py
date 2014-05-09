import entities
import numbers
import player


def create_gravity_well(x=0, y=0, kill_engines=True, strength=0.1, min_distance=3000):
	_entity = entities.create_entity(group='items')
	_entity['position'] = (x, y)
	_entity['min_distance'] = min_distance
	_entity['strength'] = strength
	_entity['kill_engines'] = kill_engines
	
	entities.register_event(_entity, 'tick', _gravity_well)

def _gravity_well(entity):
	_moving_groups = [name for name in entities.GROUPS if not name in entity['_groups'] and not name in entities.IGNORE_ENTITY_GROUPS]
	
	for entity_id in entities.get_sprite_groups(_moving_groups):
		_entity = entities.get_entity(entity_id)
		
		if numbers.distance(entity['position'], _entity['position'])<entity['min_distance']:
			_entity['in_space'] = False
			
			continue
		
		if entity['kill_engines']:
			_entity['in_space'] = True
		
		_velocity = numbers.velocity(numbers.direction_to(_entity['position'], entity['position']), entity['strength'])
		
		entities.trigger_event(_entity, 'push', velocity=_velocity)