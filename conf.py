LISTBOX_MIMETYPE = "application/x-item"

VIDEO_NODE = 7
YOLO_V4_NODE = 9
MOTION_TRACK_NODE = 10
IS_HUMAN_NODE = 11
CHECK_SHIRT_NODE = 12
DATABASE_NODE = 13

NODES = {
}

class ConfException(Exception): pass
class InvalidNodeRegistration(ConfException): pass
class OpCodeNotRegistered(ConfException): pass

def register_node_now(op_code, class_reference):
    if op_code in NODES:
        raise InvalidNodeRegistration("Duplicate node registration of '%s'. There is already %s" %(
            op_code, NODES[op_code]
        ))
    NODES[op_code] = class_reference


def register_node(op_code):
    def decorator(original_class):
        register_node_now(op_code, original_class)
        return original_class
    return decorator

def get_class_from_opcode(op_code):
    if op_code not in NODES: raise OpCodeNotRegistered("OpCode '%d' is not registered" % op_code)
    return NODES[op_code]

# import all nodes and register them
from nodes import *