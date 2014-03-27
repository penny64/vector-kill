import pyglet

import battlefield
import entities
import display
import events
import worlds


def main():
	events.register_event('boot', display.boot)
	events.register_event('boot', worlds.create, world_name='game')
	events.register_event('load', battlefield.create)
	events.register_event('loop', worlds.loop)
	
	events.trigger('boot')
	events.trigger('load')
	
	pyglet.clock.schedule(lambda _: None)
	pyglet.app.run()

if __name__ == '__main__':
	main()
	loop()