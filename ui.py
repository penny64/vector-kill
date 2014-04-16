import display
import events


def boot():
	events.register_event('tick', tick)

def tick():
	display.print_text(0, 0, '<b>Ladies and gentlemen we are floating in space</b>')
