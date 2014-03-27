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
	
	WORLDS[world_name] = {'entities': [],
	                      'next_tick': time.time()}
	
	if not ACTIVE_WORLD:
		ACTIVE_WORLD = world_name
		
		#Dirty hack...
		events.register_event('draw', sprites.draw, WORLDS[world_name]['entities'])

def register_entity(entity):
	_check_active_world()
	
	WORLDS[ACTIVE_WORLD]['entities'].append(entity)

def loop():
	_time = time.time()
	
	if _time>=WORLDS[ACTIVE_WORLD]['next_tick']:
		WORLDS[ACTIVE_WORLD]['next_tick'] = _time+(1.0/display.get_max_fps())
		WORLDS[ACTIVE_WORLD]['delta'] = 1.0
		
		events.trigger('tick')
		events.trigger('draw')
	else:
		WORLDS[ACTIVE_WORLD]['delta'] = WORLDS[ACTIVE_WORLD]['next_tick']-_time
		
		events.trigger('draw')
