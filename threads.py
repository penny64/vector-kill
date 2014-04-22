#Careful now...
from multiprocessing import Process, Lock
from multiprocessing.sharedctypes import Value, Array
from ctypes import Structure, c_double, c_int


SHARED_ENTITIES = []


class Movement(Structure):
    _fields_ = [('entity_id', c_int),
                 ('x', c_double),
                 ('y', c_double),
                 ('v_x', c_double),
                 ('v_y', c_double),
                 ('f', c_double),
                 ('a', c_double)]


def register_entity(entity):
    SHARED_ENTITIES.append((int(entity['_id']),
                            entity['position'][0],
                            entity['position'][1],
                            entity['velocity'][0],
                            entity['velocity'][1],
                            entity['friction'],
                            entity['acceleration']))

def movement(entities):
    print 'Made it...'

def tick():
    if not SHARED_ENTITIES:
        return False
    
    _entities = Array(Movement, SHARED_ENTITIES)

    p = Process(target=movement, args=(_entities,))
    p.start()
    p.join()