import entities
#import threads
import numbers
import events
import worlds
import levels

import numpy


def register_entity(entity, x=0, y=0, acceleration=.5, direction=0, speed=10, turn_rate=0.1, offload=False, no_tick=False):
	entity['position'] = numpy.zeros(2)
	entity['position'] += (x, y)
	entity['last_position'] = [x, y]
	entity['velocity'] = numpy.zeros(2)
	entity['acceleration'] = acceleration
	entity['friction'] = 0.5
	entity['turn_rate'] = turn_rate
	entity['direction'] = direction
	entity['speed'] = speed
	entity['current_speed'] = 0
	entity['min_velocity'] = [-1000, -1000]
	entity['max_velocity'] = [1000, 1000]
	entity['gravity'] = [0, .8]
	
	entities.create_event(entity, 'moved')
	entities.create_event(entity, 'accelerate')
	entities.create_event(entity, 'push')
	entities.create_event(entity, 'turn')
	entities.create_event(entity, 'thrust')
	entities.create_event(entity, 'hit_edge')
	entities.create_event(entity, 'set_position')
	entities.create_event(entity, 'set_minimum_velocity')
	entities.create_event(entity, 'set_maximum_velocity')
	entities.create_event(entity, 'set_acceleration')
	entities.create_event(entity, 'set_friction')
	entities.create_event(entity, 'set_direction')
	entities.create_event(entity, 'set_speed')
	entities.create_event(entity, 'set_turn_rate')
	entities.register_event(entity, 'turn', turn)
	entities.register_event(entity, 'thrust', thrust)
	entities.register_event(entity, 'accelerate', accelerate)
	entities.register_event(entity, 'push', push)
	entities.register_event(entity, 'set_position', set_position)
	entities.register_event(entity, 'set_minimum_velocity', set_minimum_velocity)
	entities.register_event(entity, 'set_maximum_velocity', set_maximum_velocity)
	entities.register_event(entity, 'set_acceleration', set_acceleration)
	entities.register_event(entity, 'set_friction', set_friction)
	entities.register_event(entity, 'set_direction', set_direction)
	entities.register_event(entity, 'set_speed', set_speed)
	entities.register_event(entity, 'set_turn_rate', set_turn_rate)

	if offload:
		threads.register_entity(entity)
	elif not no_tick:
		entities.register_event(entity, 'tick', tick)

def set_acceleration(entity, acceleration):
	entity['acceleration'] = acceleration

def set_friction(entity, friction):
	entity['friction'] = friction

def set_direction(entity, direction):
	entity['direction'] = direction

def set_speed(entity, speed):
	entity['speed'] = speed
	
	return True

def set_turn_rate(entity, rate):
	entity['turn_rate'] = rate
	
	return True

def set_position(entity, x, y):
	entity['last_position'][0] = x
	entity['last_position'][1] = y
	entity['position'][0] = x
	entity['position'][1] = y

def set_minimum_velocity(entity, velocity):
	entity['min_velocity'] = list(velocity)
	
	return True
	
def set_maximum_velocity(entity, velocity):
	entity['max_velocity'] = list(velocity)
	
	return True

def accelerate(entity, velocity):
	_n_vol = numbers.interp_velocity((0, 0), velocity, entity['acceleration'])
	
	entity['velocity'][0] = numbers.clip(entity['velocity'][0]+_n_vol[0], entity['min_velocity'][0], entity['max_velocity'][0])
	entity['velocity'][1] = numbers.clip(entity['velocity'][1]+_n_vol[1], entity['min_velocity'][1], entity['max_velocity'][1])

def push(entity, velocity):
	entity['velocity'][0] = entity['velocity'][0]+velocity[0]
	entity['velocity'][1] = entity['velocity'][1]+velocity[1]

def turn(entity, degrees):
	entity['direction'] += degrees

def thrust(entity):
	if 'in_space' in entity and entity['in_space']:
		return False
	
	_thrust_velocity = numbers.velocity(entity['direction'], entity['speed'])
	_next_xv = entity['velocity'][0] + numbers.interp(0, _thrust_velocity[0], entity['acceleration'])
	_next_yv = entity['velocity'][1] + numbers.interp(0, _thrust_velocity[1], entity['acceleration'])
	
	if _next_xv > entity['max_velocity'][0]:
		entity['velocity'][0] += numbers.clip(entity['max_velocity'][0]-entity['velocity'][0], 0, 1000)
	elif _next_xv < entity['min_velocity'][0]:
		entity['velocity'][0] -= numbers.clip(entity['min_velocity'][0]+entity['velocity'][0], 0, 1000)
	else:
		entity['velocity'][0] = _next_xv
	
	if _next_yv > entity['max_velocity'][1]:
		entity['velocity'][1] += numbers.clip(entity['max_velocity'][1]-entity['velocity'][1], 0, 1000)
	elif _next_yv < entity['min_velocity'][1]:
		entity['velocity'][1] -= numbers.clip(entity['min_velocity'][1]+entity['velocity'][1], 0, 1000)
	else:
		entity['velocity'][1] = _next_yv

def tick(entity):
	entity['last_position'] = entity['position'].copy()
	entity['velocity'][1] += entity['gravity'][0]*entity['gravity'][1]
	entity['position'] += entity['velocity']
	entity['velocity'] *= 1-entity['friction']
	_x = entity['position'][0]-entity['last_position'][0]
	_y = entity['position'][1]-entity['last_position'][1]
	
	if entity['velocity'][0] > entity['max_velocity'][0]:
		entity['velocity'][0] = numbers.clip(entity['velocity'][0]*.95, entity['max_velocity'][0], 1000)
	elif entity['velocity'][0] < entity['min_velocity'][0]:
		entity['velocity'][0] = numbers.clip(entity['velocity'][0]*.95, -1000, -entity['min_velocity'][0])
	
	if entity['velocity'][1] > entity['max_velocity'][1]:
		entity['velocity'][1] = numbers.clip(entity['velocity'][1]*.95, entity['max_velocity'][1], 1000)
	elif entity['velocity'][1] < entity['min_velocity'][1]:
		entity['velocity'][1] = numbers.clip(entity['velocity'][1]*.95, -1000, -entity['min_velocity'][1])
	
	entity['current_speed'] = numbers.distance(entity['last_position'], entity['position'])
	
	if not 'NO_BOUNCE' in entity or not entity['NO_BOUNCE']:
		if entity['position'][0] > worlds.get_size()[0]:
			entity['position'][0] = worlds.get_size()[0]
			entity['velocity'][0] = -entity['velocity'][0]
			
			entities.trigger_event(entity, 'hit_edge')
		elif entity['position'][0] < 0:
			entity['position'][0] = 0
			entity['velocity'][0] = -entity['velocity'][0]
			
			entities.trigger_event(entity, 'hit_edge')
		
		if entity['position'][1] > worlds.get_size()[1]:
			entity['position'][1] = worlds.get_size()[1]
			entity['velocity'][1] = -entity['velocity'][1]
			
			entities.trigger_event(entity, 'hit_edge')
		elif entity['position'][1] < 0:
			entity['position'][1] = 0
			entity['velocity'][1] = -entity['velocity'][1]
			
			entities.trigger_event(entity, 'hit_edge')
	
	#_hit = False
	#if levels.is_solid(int(round(entity['position'][0]))+50, int(round(entity['position'][1]))):
	#	entity['velocity'][0] = -entity['velocity'][0]
	#	entities.trigger_event(entity, 'set_position', x=(((entity['position'][0]+50)/100)*100)-52, y=entity['position'][1])
	#	entities.trigger_event(entity, 'hit_edge')
	#	_hit = True
	#elif levels.is_solid(int(round(entity['position'][0]-50)), int(round(entity['position'][1]))):
	#	entity['velocity'][0] = -entity['velocity'][0]
	#	entities.trigger_event(entity, 'set_position', x=(((entity['position'][0]-50)/100)*100)+52, y=entity['position'][1])
	#	entities.trigger_event(entity, 'hit_edge')
	#	_hit = True
	
	#if levels.is_solid(int(round(entity['position'][0])), int(round(entity['position'][1]))+50):
	#	entity['velocity'][1] = -entity['velocity'][1]
	#	entities.trigger_event(entity, 'set_position', x=entity['position'][0], y=(((entity['position'][1]+50)/100)*100)-54)
	#	entities.trigger_event(entity, 'hit_edge')
	#	_hit = True
	#elif levels.is_solid(int(round(entity['position'][0])), int(round(entity['position'][1]))-50):
	#	entity['velocity'][1] = -entity['velocity'][1]
	#	entities.trigger_event(entity, 'set_position', x=entity['position'][0], y=(((entity['position'][1]-50)/100)*100)+52)
	#	entities.trigger_event(entity, 'hit_edge')
	#	_hit = True
	
	#if not 'NO_BOUNCE' in entity or not entity['NO_BOUNCE']:
	#	if levels.is_solid(int(round(entity['position'][0]))+50, int(round(entity['position'][1]))+50):
	#		entity['velocity'][0] = -entity['velocity'][0]
	#		entity['velocity'][1] = -entity['velocity'][1]
	#		entities.trigger_event(entity, 'set_position', x=(((entity['position'][0]+50)/100)*100)-52, y=(((entity['position'][1]+50)/100)*100)-54)
	#		entities.trigger_event(entity, 'hit_edge')
	#	elif levels.is_solid(int(round(entity['position'][0]))-50, int(round(entity['position'][1]))+50):
	#		entity['velocity'][0] = -entity['velocity'][0]
	#		entity['velocity'][1] = -entity['velocity'][1]
	#		entities.trigger_event(entity, 'set_position', x=(((entity['position'][0]-50)/100)*100)+52, y=(((entity['position'][1]+50)/100)*100)-54)
	#		entities.trigger_event(entity, 'hit_edge')
	#	elif levels.is_solid(int(round(entity['position'][0]))-50, int(round(entity['position'][1]))-50):
	#		entity['velocity'][0] = -entity['velocity'][0]
	#		entity['velocity'][1] = -entity['velocity'][1]
	#		entities.trigger_event(entity, 'set_position', x=(((entity['position'][0]-50)/100)*100)+52, y=(((entity['position'][1]-50)/100)*100)+52)
	#		entities.trigger_event(entity, 'hit_edge')
	#	elif levels.is_solid(int(round(entity['position'][0]))+50, int(round(entity['position'][1]))-50):
	#		entity['velocity'][0] = -entity['velocity'][0]
	#		entity['velocity'][1] = -entity['velocity'][1]
	#		entities.trigger_event(entity, 'set_position', x=(((entity['position'][0]+50)/100)*100)-52, y=(((entity['position'][1]-50)/100)*100)+52)
	#		entities.trigger_event(entity, 'hit_edge')
	
	_position_change = [entity['position'][0]-entity['last_position'][0],
	                    entity['position'][1]-entity['last_position'][1]]
	
	if not (entity['position']==entity['last_position']).all():
		entities.trigger_event(entity,
			                  'moved',
			                  last_position=entity['last_position'],
			                  position_change=_position_change,
		                       velocity=entity['velocity'])