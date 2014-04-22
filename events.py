EVENTS = {'BOOT': {'events': {}, 'id': 1},
          'LOAD': {'events': {}, 'id': 1},
          'INPUT': {'events': {}, 'id': 1},
          'CAMERA': {'events': {}, 'id': 1},
          'LOOP': {'events': {}, 'id': 1},
          'TICK': {'events': {}, 'id': 1},
          'DRAW': {'events': {}, 'id': 1},
          'CLEANUP': {'events': {}, 'id': 1},
          'SHUTDOWN': {'events': {}, 'id': 1}}


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
			del EVENTS[event_name.upper()]['events'][event['id']]
			
			return True

def trigger_event(event_name):
	for event in EVENTS[event_name.upper()]['events'].values():
		event['callback'](*event['args'], **event['kargs'])
