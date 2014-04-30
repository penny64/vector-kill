import display
import numbers
import worlds
import events


CURRENT_TIME = 0.0
T = 0.0
DT = .025#1/60.0
ACCU = 0.0


def boot():
	global CURRENT_TIME
	
	CURRENT_TIME = worlds.get_time()

def tick():
	global CURRENT_TIME, ACCU, T
	
	_new_time = worlds.get_time()
	_frame_time = _new_time-CURRENT_TIME
	CURRENT_TIME = _new_time	
	ACCU = numbers.clip(ACCU+_frame_time, 0, DT)
	
	while ACCU >= DT:
		events.trigger_event('logic')
		
		ACCU -= DT
		T += DT
	
	display.set_clock_delta(_frame_time)
	events.trigger_event('frame')