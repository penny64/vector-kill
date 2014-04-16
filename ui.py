import display
import events


def boot():
	events.register_event('tick', tick)
	display.print_text(5,
	                   10,
	                   'flagsdev, 2014',
	                   fade_in_speed=2,
	                   show_for=4)
	display.print_text(5,
	                   24,
	                   '<b>Vector:Kill: Suicide Ships (Prototype)</b>',
	                   color=(200, 200, 200, 0),
	                   fade_in_speed=4,
	                   show_for=5)

def tick():
	pass
