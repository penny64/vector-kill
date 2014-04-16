import movement
import entities
import numbers
import sprites
import events


def create():
	_soldier = entities.create_entity()
	
	movement.register_entity(_soldier)
	sprites.register_entity(_soldier, 'soldiers')
	events.register_event('tick', tick, _soldier)
	entities.register_event(_soldier, 'moved', set_direction)
	entities.trigger_event(_soldier, 'set_minimum_velocity', velocity=[-15, -15])
	entities.trigger_event(_soldier, 'set_maximum_velocity', velocity=[15, 15])
	entities.trigger_event(_soldier, 'set_acceleration', acceleration=.05)
	entities.trigger_event(_soldier, 'set_friction', friction=0)
	
	return _soldier

def set_direction(entity, **kwargs):
	_direction = numbers.distance([0, 0], kwargs['position_change'])*numbers.clip(kwargs['position_change'][0], -1, 1)
	entities.trigger_event(entity, 'rotate_by', degrees=_direction*.5)

def tick(entity):
	return False
