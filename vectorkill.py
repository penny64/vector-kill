import pyglet

import battlefield
import entities
import display
import events
import worlds


def loop():
	display.set_caption('%s - %ifps' % ('vector:KILL', round(display.get_fps())))

def main():
	events.register_event('boot', display.boot)
	events.register_event('boot', worlds.create, world_name='game')
	events.register_event('load', battlefield.create)
	events.register_event('loop', loop)
	
	events.trigger_event('boot')
	events.trigger_event('load')
	
	pyglet.clock.schedule_interval(worlds.loop, 1/60.0)
	pyglet.app.run()

if __name__ == '__main__':
	main()
