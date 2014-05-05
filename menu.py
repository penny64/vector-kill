import battlefield
import controls
import entities
import display
import events
import worlds
import levels

import random


MENU_INDEX = 0
MENU = None
CAMERA_TIME = 30
CAMERA_MODES = ['hover', 'follow']
CAMERA_MODE = random.choice(CAMERA_MODES)


def boot():
	setup_main_menu()

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


def setup_main_menu():
	global MENU
	
	events.register_event('input', control)
	events.register_event('loop', battlefield.loop_attract)
	events.register_event('camera', action_camera)
	battlefield.create(player=False)
	display.create_text_group('logo')
	display.create_text_group('menu')
	
	MENU = [{'text': 'Career', 'callback': start_career},
	        {'text': 'Arena', 'callback': weapon_selection},
	        {'text': 'Quit', 'callback': shutdown}]
	
	display.print_text(display.get_window_size()[0]/2,
	                   display.get_window_size()[1]*.8,
	                   'VECTOR:KILL',
	                   color=(0, 255, 0, 100),
	                   font_name='Thin Design',
	                   font_size=42,
	                   center=True,
	                   show_for=-1,
	                   text_group='logo')
	
	display.print_text(display.get_window_size()[0]/2,
	                   display.get_window_size()[1]*.20,
	                   'Next unlock:',
	                   text_group='bot_center',
	                   color=(238, 221, 130, 255),
	                   show_for=-1,
	                   center=True)
	
	display.print_text(display.get_window_size()[0]/2,
	                   display.get_window_size()[1]*.15,
	                   'Ivan\'s Chaingun',
	                   text_group='bot_center',
	                   color=(255, 215, 0, 255),
	                   show_for=-1,
	                   center=True)
	
	draw_menu()

def weapon_selection():
	global MENU_INDEX, MENU
	
	MENU_INDEX = 0
	MENU = [{'text': 'None', 'callback': start_arena},
	        {'text': 'Chaingun', 'callback': lambda: start_arena(weapon='chaingun')},
	        {'text': 'Back', 'callback': setup_main_menu}]
	
	display.print_text(display.get_window_size()[0]/2,
	                   display.get_window_size()[1]*.8,
	                   'VECTOR:KILL',
	                   color=(0, 255, 0, 100),
	                   font_name='Thin Design',
	                   font_size=42,
	                   center=True,
	                   show_for=-1,
	                   text_group='logo')
	
	display.print_text(display.get_window_size()[0]/2,
	                   display.get_window_size()[1]*.20,
	                   'Next unlock:',
	                   text_group='bot_center',
	                   color=(238, 221, 130, 255),
	                   show_for=-1,
	                   center=True)
	
	display.print_text(display.get_window_size()[0]/2,
	                   display.get_window_size()[1]*.15,
	                   'Ivan\'s Chaingun',
	                   text_group='bot_center',
	                   color=(255, 215, 0, 255),
	                   show_for=-1,
	                   center=True)
	
	draw_menu()

def action_camera():
	global CAMERA_TIME, CAMERA_MODE
	
	if CAMERA_MODE == 'hover':
		display.CAMERA['next_center_on'] = [worlds.get_size()[0]/2, worlds.get_size()[1]/2]
		display.CAMERA['next_zoom'] = 5.0
	
	elif CAMERA_MODE == 'follow':
		_focus_on = entities.get_entity_group('enemies')
		
		if not _focus_on:
			_focus_on = entities.get_entity_group('hazards')
		
		display.CAMERA['next_center_on'] = entities.get_entity(_focus_on[0])['position'][:]
		display.CAMERA['next_zoom'] = 2.5
	
	CAMERA_TIME -= 1
	
	if not CAMERA_TIME:
		CAMERA_MODE = random.choice(CAMERA_MODES)
		CAMERA_TIME = random.randint(120, 200)

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
	display.clear_text_group('bot_center')
	events.unregister_event('input', control)
	events.unregister_event('loop', battlefield.loop_attract)
	events.unregister_event('camera', action_camera)
	events.register_event('loop', levels.loop)
	battlefield.clean()
	levels.load_level()
	display.CAMERA['camera_move_speed'] = 0.05

def start_arena(weapon=None):
	display.clear_text_group('menu')
	display.clear_text_group('logo')
	display.clear_text_group('bot_center')
	events.unregister_event('input', control)
	events.unregister_event('loop', battlefield.loop_attract)
	events.unregister_event('camera', action_camera)
	events.register_event('loop', battlefield.loop)
	battlefield.clean()
	battlefield.create()
	display.CAMERA['camera_move_speed'] = 0.05

def shutdown():
	events.trigger_event('shutdown')