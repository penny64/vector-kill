import entities
import display
import bullet


def create(owner_id, rounds=1, recoil_time=16, reload_time=35, missile=True, hitscan=False, tracking=False):
	_entity = entities.create_entity()
	_entity['owner_id'] = owner_id
	_entity['rounds'] = rounds
	_entity['max_rounds'] = rounds
	_entity['recoil_time'] = 1
	_entity['recoil_time_max'] = recoil_time
	_entity['reload_time'] = reload_time
	_entity['reload_time_max'] = reload_time
	_entity['missile'] = missile
	_entity['hitscan'] = hitscan
	_entity['tracking'] = tracking
	_entity['firing'] = False
	_entity['speed'] = 30
	
	entities.create_event(_entity, 'shoot')
	entities.register_event(_entity, 'shoot', shoot)
	entities.register_event(entities.get_entity(owner_id), 'delete', lambda owner_entity: entities.delete_entity(_entity))
	
	return _entity

def shoot(entity):
	if entity['firing']:
		return False
	
	entities.register_event(entity, 'tick', tick)
	entity['firing'] = True

def tick(entity):
	entity['recoil_time'] -= 1
	
	if not entity['owner_id'] in entities.ENTITIES:
		entities.unregister_event(entity, 'tick', tick)
		
		return False
	
	if entity['recoil_time']>0:
		return False
	elif not entity['rounds']:
		if entity['reload_time']:
			if entity['owner_id'] in entities.ENTITIES and 'player' in entities.get_entity(entity['owner_id']) and entity['reload_time'] == entity['reload_time_max']:
				display.print_text(0, 0, 'RELOADING', show_for=(entity['reload_time']/display.get_tps())*2, fade_out_speed=255)
				
			entity['reload_time'] -= 1
		else:
			entity['reload_time'] = entity['reload_time_max']
			entity['recoil_time'] = 1
			entity['rounds'] = entity['max_rounds']
			entity['firing'] = False
			entities.unregister_event(entity, 'tick', tick)
		
		return False
	
	_owner = entities.get_entity(entity['owner_id'])
	
	if entity['missile']:
		bullet.create_missile(_owner['position'][0],
		                      _owner['position'][1],
		                      _owner['shoot_direction'],
		                      entity['speed'],
		                      'bullet.png',
		                      entity['owner_id'],
		                      tracking=entity['tracking'])
	
	entity['recoil_time'] = entity['recoil_time_max']
	entity['rounds'] -= 1