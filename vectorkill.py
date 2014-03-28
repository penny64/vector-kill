import pyglet

import battlefield
import entities
import controls
import display
import events
import worlds


def loop(dt):
	display.set_clock_delta(dt)
	
	events.trigger_event('loop')

def window(dt):
	display.set_caption('%s - %ifps' % ('vector:KILL', round(display.get_fps())))

def main():
	events.register_event('boot', display.boot)
	events.register_event('boot', controls.boot, display.get_window())
	events.register_event('boot', worlds.create, world_name='game')
	events.register_event('load', battlefield.create)
	events.register_event('loop', controls.loop)
	
	events.trigger_event('boot')
	events.trigger_event('load')
	
	pyglet.clock.schedule(loop)
	pyglet.clock.schedule_interval(worlds.loop, 1/display.get_tps())
	pyglet.clock.schedule_interval(window, 1/10)
	pyglet.app.run()

if __name__ == '__main__':
	main()
