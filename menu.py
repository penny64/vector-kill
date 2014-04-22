import battlefield
import controls
import entities
import display
import events
import worlds


MENU_INDEX = 0
MENU = None


def boot():
	global MENU
	
	events.register_event('tick', tick)
	events.register_event('input', control)
	events.register_event('loop', battlefield.loop_attract)
	events.register_event('camera', action_camera)
	battlefield.create(no_player=True)
	display.create_text_group('logo')
	display.create_text_group('menu')
	
	MENU = [{'text': 'Career', 'callback': start_career},
	        {'text': 'Quit', 'callback': shutdown}]
	
	_title_text = 'VECTOR:KILL'
	display.print_text(display.get_window_size()[0]/2,
	                   display.get_window_size()[1]*.8,
	                   _title_text,
	                   color=(0, 255, 0, 100),
	                   font_name='Thin Design',
	                   font_size=42,
	                   center=True,
	                   show_for=-1,
	                   text_group='logo')
	
	draw_menu()

def control():
	global MENU_INDEX
	
	if controls.key_pressed_ord(controls.ARROW_DOWN):
		if MENU_INDEX+1<len(MENU):
			MENU_INDEX += 1
		
		draw_menu()
	elif controls.key_pressed_ord(controls.ARROW_UP):
		if MENU_INDEX:
			MENU_INDEX -= 1
		
		draw_menu()
	elif controls.key_pressed_ord(controls.ENTER):
		MENU[MENU_INDEX]['callback']()

def tick():
	pass

def action_camera():
	_focus_on = entities.get_entity_group('enemies')
	
	if not _focus_on:
		_focus_on = entities.get_entity_group('soldiers')
		
	display.CAMERA['next_center_on'] = entities.get_entity(_focus_on[0])['position']

def draw_menu():
	_i = 0
	
	display.clear_text_group('menu')
	
	for menu_item in MENU:
		_text = menu_item['text']
		
		if _i == MENU_INDEX:
			_text = '> '+_text+' <'
		
		display.print_text(display.get_window_size()[0]/2,
		                   (display.get_window_size()[1]*.65)-(_i*24),
		                   _text,
		                   show_for=-1,
		                   center=True,
		                   text_group='menu')
		_i += 1

def start_career():
	display.clear_text_group('menu')
	display.clear_text_group('logo')
	events.unregister_event('input', control)
	events.unregister_event('loop', battlefield.loop_attract)
	events.register_event('loop', battlefield.loop)
	battlefield.clean()
	battlefield.create()

def shutdown():
	events.trigger_event('shutdown')