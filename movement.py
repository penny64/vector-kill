import display
import events


def register_entity(entity):
	entity['position'] = [100, 100]
	entity['velocity'] = [5, 0]
	
	events.register_event('tick', tick, entity)

def tick(entity):
	_dt = display.get_clock_delta()
	
	entity['position'][0] += (entity['velocity'][0] * _dt)
	entity['position'][1] += (entity['velocity'][1] * _dt)