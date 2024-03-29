import pyglet

import battlefield
import entities
import controls
import display
#import threads
import events
import worlds
import levels
import clock
import menu
import ui

import cProfile
import sys


def window():
	display.set_caption('%s - %ifps - %stps - %s' % ('vector:kill: SUICIDE SHIPS',
	                                                 round(display.get_fps()),
	                                                 entities.TICKS_PER_SECOND,
	                                                 len(entities.ENTITIES)))

def main():
	events.register_event('boot', display.boot)
	events.register_event('boot', entities.boot)
	events.register_event('boot', controls.boot, display.get_window())
	events.register_event('boot', worlds.create, world_name='game')
	events.register_event('boot', ui.boot)
	events.register_event('boot', menu.boot)
	events.register_event('boot', battlefield.boot)
	events.register_event('boot', clock.boot)
	events.register_event('load', display.load)
	events.register_event('load', display.load)
	events.register_event('load', levels.load)
	events.register_event('loop', clock.tick)
	events.register_event('loop', controls.loop)
	events.register_event('logic', worlds.logic)
	events.register_event('frame', window)
	events.register_event('shutdown', display.shutdown)
	
	events.trigger_event('boot')
	events.trigger_event('load')
	
	#clock.create_scheduled_event('world_loop', worlds.loop, 1/display.get_tps())
	#clock.create_scheduled_event('window_loop', window, 1/10.0)
	#pyglet.clock.schedule_interval(window, 1/10.0)
	#pyglet.clock.schedule_interval(worlds.loop, 1/display.get_tps())
	
	if display.RABBYT:
		while not display.WINDOW.has_exit:
			display.lib2d.step(pyglet.clock.tick())
			display.WINDOW.dispatch_events()
			display.WINDOW.dispatch_event('on_draw')
			display.WINDOW.flip()
	else:
		#pyglet.app.run()
		while not display.WINDOW.has_exit:
			events.trigger_event('loop')
			display.WINDOW.dispatch_events()
			display.WINDOW.dispatch_event('on_draw')
			display.WINDOW.flip()

if __name__ == '__main__':
	if '--profile' in sys.argv:
		cProfile.run('main()','profile.dat')
	else:
		main()
