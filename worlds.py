import display
import sprites
import events
import time


WORLDS = {}
ACTIVE_WORLD = None


def _check_active_world():
	if not ACTIVE_WORLD:
		raise Exception('ACTIVE_WORLD not set.')


def create(world_name):
	global ACTIVE_WORLD
	
	WORLDS[world_name] = {'size': (1000, 1000),
	                      'entities': [],
	                      'next_tick': time.time()}
	
	if not ACTIVE_WORLD:
		ACTIVE_WORLD = world_name
		
		#Dirty hack...
		events.register_event('draw', sprites.draw)

def get_size():
	return WORLDS[ACTIVE_WORLD]['size']

def register_entity(entity):
	_check_active_world()
	
	WORLDS[ACTIVE_WORLD]['entities'].append(entity)

def loop(dt):
	_time = time.time()
	_world = WORLDS[ACTIVE_WORLD]
	
	display.set_clock_delta(dt)
	
	events.trigger_event('loop')
	
	if _time>=_world['next_tick']:
		WORLDS[ACTIVE_WORLD]['next_tick'] = _time+(1.0/display.get_tps())
		display.set_clock_delta(0)
		
		events.trigger_event('tick')
	else:
		display.set_clock_delta(WORLDS[ACTIVE_WORLD]['next_tick']-_time)
