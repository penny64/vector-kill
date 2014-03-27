EVENTS = {'BOOT': [],
          'LOAD': [],
          'LOOP': [],
          'TICK': [],
          'DRAW': []}


def register_event(event_name, callback, *args, **kargs):
	EVENTS[event_name.upper()].append({'callback': callback,
	                                   'args': args,
	                                   'kargs': kargs})

def trigger_event(event_name):
	for event in EVENTS[event_name.upper()]:
		event['callback'](*event['args'], **event['kargs'])
