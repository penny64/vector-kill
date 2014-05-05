import display


def unlock_chaingun():
	display.print_text(display.get_window_size()[0]/2,
					   display.get_window_size()[1]*.30,
					   'Unlocked: Ivan\'s Chaingun',
	                   color=(255, 255, 255, 150),
	                   font_size=18,
					   center=True)