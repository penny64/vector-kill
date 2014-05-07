import entities


def register_entity(entity):
	entity['timers'] = []
	
	entities.create_event(entity, 'create_timer')
	entities.register_event(entity, 'create_timer', create_timer)
	entities.register_event(entity, 'tick', tick)

#TODO: Timer names
def create_timer(entity, time, repeat=0, callback=None, enter_callback=None, exit_callback=None, repeat_callback=None):
	entity['timers'].append({'callback': callback,
						'enter_callback': enter_callback,
						'exit_callback': exit_callback,
	                         'repeat_callback': repeat_callback,
	                         'time': time,
	                         'time_max': time,
	                         'repeat': repeat,
	                         'entered': False})

def tick(entity):
	_remove_timers = []
	
	for timer in entity['timers']:
		if not timer['entered']:
			if timer['enter_callback']:
				timer['enter_callback'](entity)
			
			timer['entered'] = True
		
		if timer['time']:
			timer['time'] -= 1
			
			if timer['callback']:
				timer['callback'](entity)
		elif timer['repeat']:
			timer['time'] = timer['time_max']
			timer['repeat'] -= 1
			
			if timer['repeat_callback']:
				timer['repeat_callback'](entity)
		else:
			if timer['exit_callback']:
				timer['exit_callback'](entity)
			
			_remove_timers.append(timer)
	
	for timer in _remove_timers:
		entity['timers'].remove(timer)