import display
import numbers
import sprites
import events
import time
import os


WORLDS = {}
ACTIVE_WORLD = None


def get_time():
	if os.sep == '/':
		return time.time()
	
	return time.clock()

def _check_active_world():
	if not ACTIVE_WORLD:
		raise Exception('ACTIVE_WORLD not set.')

def create(world_name):
	global ACTIVE_WORLD
	
	WORLDS[world_name] = {'size': (1000, 1000),
	                      'entities': [],
	                      'last_tick': get_time(),
	                      'next_tick': get_time()+.000001}
	
	if not ACTIVE_WORLD:
		ACTIVE_WORLD = world_name
		
		#Dirty hack...
		events.register_event('draw', sprites.draw)

def get_interp():
	_world = WORLDS[ACTIVE_WORLD]
	
	return numbers.clip((get_time()-_world['last_tick'])/(_world['next_tick']-_world['last_tick']), 0, 1.0)

def get_size():
	return WORLDS[ACTIVE_WORLD]['size']

def register_entity(entity):
	_check_active_world()
	
	#WORLDS[ACTIVE_WORLD]['entities'].append(entity['_id'])

def loop(dt):
	#TODO: time.time() on Linux!
	_time = get_time()
	_world = WORLDS[ACTIVE_WORLD]
	_world['last_tick'] = _time
	
	if _time>=_world['next_tick']:
		_world['next_tick'] = _time+(1.0/display.get_tps())
		
		events.trigger_event('tick')
	
	events.trigger_event('cleanup')
