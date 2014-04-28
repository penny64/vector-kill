import entities
import movement
import sprites
import effects


def save_map(name, map_dict):
	with open('%s.dat' % name, 'w') as _file:
		for x in range(10000/100):
			for y in range(10000/100):
				if map_dict['%s,%s' % (x*100, y*100)]['solid']:
					_file.write('1')
				else:
					_file.write('0')
			
			_file.write('\n')
	
	return _map

def load_map(name):
	_map = {}
	
	with open('%s.dat' % name, 'r') as _file:
		_x = 0
		_y = 0
		
		for line in _file.readlines():
			_x = 0
			
			for tile in [int(c) for c in line if not c == '\n']:
				_map['%s,%s' % (_x*100, _y*100)] = {'solid': False}
				
				if tile == 1:
					_map['%s,%s' % (_x*100, _y*100)]['solid'] = True
					_tile = entities.create_entity('tiles_foreground')
					_map['%s,%s' % (_x*100, _y*100)]['tile'] = _tile['_id']
					_sprite = effects.create_image(_y*100, _x*100, 'wall_full.png')
					_id = _sprite['_id']
					
					print _id
					entities.register_event(_tile, 'delete', lambda _entity: entities.delete_entity_via_id(_id))
					
					_sprite['sprite'].image.anchor_x = 0
					_sprite['sprite'].image.anchor_y = 0
				
				_x += 1
			_y += 1
	
	return _map