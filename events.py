EVENTS = {'BOOT': {'events': {}, 'id': 1, 'banned': set()},
          'LOAD': {'events': {}, 'id': 1, 'banned': set()},
          'INPUT': {'events': {}, 'id': 1, 'banned': set()},
          'CAMERA': {'events': {}, 'id': 1, 'banned': set()},
          'LOOP': {'events': {}, 'id': 1, 'banned': set()},
          'TICK': {'events': {}, 'id': 1, 'banned': set()},
          'DRAW': {'events': {}, 'id': 1, 'banned': set()},
          'CLEANUP': {'events': {}, 'id': 1, 'banned': set()},
          'SHUTDOWN': {'events': {}, 'id': 1, 'banned': set()},
          'FRAME': {'events': {}, 'id': 1, 'banned': set()}}


def register_event(event_name, callback, *args, **kargs):
	_event = {'callback': callback,
	          'args': args,
	          'kargs': kargs,
	          'id': str(EVENTS[event_name.upper()]['id'])}
	
	for arg in args:
		if isinstance(arg, dict) and '_id' in arg:
			_event['_world_events'] = arg['_id']
	
	_event_structure = EVENTS[event_name.upper()]
	_event_structure['events'][str(_event_structure['id'])] = _event
	_event_structure['id'] += 1

def unregister_event(event_name, callback, *args, **kargs):
	for event in EVENTS[event_name.upper()]['events'].values():
		if event['callback'] == callback:
			EVENTS[event_name.upper()]['banned'].add(event['id'])
			
			del EVENTS[event_name.upper()]['events'][event['id']]
			return True
	
	raise Exception('Event not registered.')

def trigger_event(event_name):
	for event in EVENTS[event_name.upper()]['events'].values():
		if event['id'] in EVENTS[event_name.upper()]['banned']:
			EVENTS[event_name.upper()]['banned'].remove(event['id'])
			
			continue
		
		event['callback'](*event['args'], **event['kargs'])
