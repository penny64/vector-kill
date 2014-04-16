import movement
import entities
import sprites
import events


def create():
	_soldier = entities.create_entity()
	
	movement.register_entity(_soldier)
	sprites.register_entity(_soldier, 'soldiers')
	events.register_event('tick', tick, _soldier)
	entities.trigger_event(_soldier, 'set_minimum_velocity', velocity=[-15, -15])
	entities.trigger_event(_soldier, 'set_maximum_velocity', velocity=[15, 15])
	entities.trigger_event(_soldier, 'set_acceleration', acceleration=.8)
	
	return _soldier

def tick(entity):
	entities.trigger_event(entity, 'rotate_by', degrees=2)