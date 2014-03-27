import movement
import entities
import sprites


def create():
	_soldier = entities.create_entity()
	
	movement.register_entity(_soldier)
	sprites.register_entity(_soldier)