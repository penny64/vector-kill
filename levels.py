import entities
import display
import player
import events
import worlds
import ships
import maps

import random


MAP = {}

def load():
	global MAP
	
	for x in range(10000/100):
		for y in range(10000/100):
			MAP['%s,%s' % (x*100, y*100)] = {'solid': False}

def clean():
	for ship_id in entities.get_entity_group('players'):
		entities.delete_entity(entities.ENTITIES[ship_id])
	
	for ship_id in entities.get_entity_group('enemies'):
		entities.delete_entity(entities.ENTITIES[ship_id])	
	
	for ship_id in entities.get_entity_group('hazards'):
		entities.delete_entity(entities.ENTITIES[ship_id])
	
	for ship_id in entities.get_entity_group('effects'):
		entities.delete_entity(entities.ENTITIES[ship_id])
	
	for ship_id in entities.get_entity_group('bullets'):
		entities.delete_entity(entities.ENTITIES[ship_id])
	
	for ship_id in entities.get_entity_group('weapons'):
		entities.delete_entity(entities.ENTITIES[ship_id])
	
	entities.reset()

def load_level():
	global MAP
	
	MAP = maps.load_map('test')
	create_player()

def create(player=True):
	pass
		
def create_player():
	_player = ships.create_energy_ship()
	_player['player'] = True
	
	player.register_entity(_player)
	events.register_event('input', player.handle_input, _player['_id'])
	events.register_event('camera', player.handle_camera, _player['_id'])
	entities.register_event(_player, 'delete', player.delete)

def loop():
	pass


def is_solid(x, y):
	_key = '%s,%s' % ((x/100)*100, (y/100)*100)
	
	try:
		return MAP[_key]['solid']
	except:
		return False
