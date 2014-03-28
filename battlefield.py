import soldier
import display


def create():
	display.create_sprite_group('soldiers')
	
	for i in range(50):
		soldier.create()
