import display
import numbers
import worlds
import events


CLOCKS = {}
CURRENT_TIME = 0.0
T = 0.0
DT = .025#1/60.0
ACCU = 0.0


def boot():
	global CURRENT_TIME
	
	CURRENT_TIME = worlds.get_time()

def create_scheduled_event(name, callback, interval):
	if name in CLOCKS:
		raise Exception('Clock already exists: %s' % name)
	
	_ts = worlds.get_time()
	
	CLOCKS[name] = {'name': name,
	                'callback': callback,
	                'last_ts': _ts,
	                'next_ts': _ts+interval,
	                'dt': 0,
	                'interval': interval}


def tick():
	global CURRENT_TIME, ACCU, T
	
	_new_time = worlds.get_time()
	_frame_time = _new_time-CURRENT_TIME
	CURRENT_TIME = _new_time	
	ACCU = numbers.clip(ACCU+_frame_time, 0, DT)
	
	while ACCU >= DT:
		CLOCKS['world_loop']['callback'](_frame_time)
		ACCU -= DT
		T += DT
	
	display.set_clock_delta(_frame_time)
	events.trigger_event('frame')