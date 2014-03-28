import events


def register_entity(entity):
	entity['position'] = [100, 100]
	entity['last_position'] = [100, 100]
	entity['velocity'] = [5, 0]
	entity['gravity'] = [.5, .8]
	
	events.register_event('tick', tick, entity)

def tick(entity):
	entity['last_position'] = entity['position'][:]
	
	entity['velocity'][1] += entity['gravity'][0]*entity['gravity'][1]
	entity['position'][0] += (entity['velocity'][0])
	entity['position'][1] += (entity['velocity'][1])