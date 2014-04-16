import entities
import controls
import display


def handle_input(entity_id):
	_entity = entities.get_entity(entity_id)
	
	if controls.key_pressed('d') or controls.key_held('d'):
		entities.trigger_event(_entity, 'accelerate', velocity=[3, 0])
	
	if controls.key_pressed('a') or controls.key_held('a'):
		entities.trigger_event(_entity, 'accelerate', velocity=[-3, 0])
	
	if controls.key_pressed('a') or controls.key_held('w'):
		entities.trigger_event(_entity, 'accelerate', velocity=[0, -3])
	
	if controls.key_pressed('a') or controls.key_held('s'):
		entities.trigger_event(_entity, 'accelerate', velocity=[0, 3])

def handle_camera(entity_id):
	display.CAMERA['next_center_on'] = entities.get_entity(entity_id)['position'][:]
	display.CAMERA['next_center_on'][0] += 50
	display.CAMERA['next_center_on'][1] += 50