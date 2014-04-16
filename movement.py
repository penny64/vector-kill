import entities
import numbers
import events


def register_entity(entity):
	entity['position'] = [40, 0]
	entity['last_position'] = [100, 100]
	entity['velocity'] = [0, 0]
	entity['acceleration'] = 0.5
	entity['friction'] = 0.5
	entity['direction'] = 0
	entity['min_velocity'] = [-1000, -1000]
	entity['max_velocity'] = [1000, 1000]
	entity['gravity'] = [0, .8]
	
	events.register_event('tick', tick, entity)
	entities.create_event(entity, 'moved')
	entities.create_event(entity, 'accelerate')
	entities.create_event(entity, 'set_minimum_velocity')
	entities.create_event(entity, 'set_maximum_velocity')
	entities.create_event(entity, 'set_acceleration')
	entities.create_event(entity, 'set_friction')
	entities.create_event(entity, 'set_direction')
	entities.register_event(entity, 'set_minimum_velocity', set_minimum_velocity)
	entities.register_event(entity, 'set_maximum_velocity', set_maximum_velocity)
	entities.register_event(entity, 'set_acceleration', set_acceleration)
	entities.register_event(entity, 'set_friction', set_friction)
	entities.register_event(entity, 'set_direction', set_direction)
	entities.register_event(entity, 'accelerate', accelerate)

def set_acceleration(entity, acceleration):
	entity['acceleration'] = acceleration

def set_friction(entity, friction):
	entity['friction'] = friction

def set_direction(entity, direction):
	entity['direction'] = direction

def set_minimum_velocity(entity, velocity):
	entity['min_velocity'] = list(velocity)
	
def set_maximum_velocity(entity, velocity):
	entity['max_velocity'] = list(velocity)

def accelerate(entity, velocity):
	_n_vol = numbers.interp_velocity((0, 0), velocity, entity['acceleration'])
	
	entity['velocity'][0] = numbers.clip(entity['velocity'][0]+_n_vol[0], entity['min_velocity'][0], entity['max_velocity'][0])
	entity['velocity'][1] = numbers.clip(entity['velocity'][1]+_n_vol[1], entity['min_velocity'][1], entity['max_velocity'][1])

def tick(entity):
	entity['last_position'] = entity['position'][:]
	entity['velocity'][1] += entity['gravity'][0]*entity['gravity'][1]
	entity['position'][0] += entity['velocity'][0]
	entity['position'][1] += entity['velocity'][1]
	entity['velocity'][0] *= 1-entity['friction']
	entity['velocity'][1] *= 1-entity['friction']
	_position_change = [entity['position'][0]-entity['last_position'][0],
	                    entity['position'][1]-entity['last_position'][1]]
	
	entities.trigger_event(entity,
	                       'moved',
	                       last_position=entity['last_position'],
	                       position_change=_position_change,
					   velocity=entity['velocity'])