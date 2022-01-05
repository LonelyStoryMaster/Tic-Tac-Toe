from enum import Enum
from math import sqrt

class Winners(Enum):
	NONE = 0
	X = 1
	O = 2
	DRAW = 3

class Colors(Enum):
    BLUE  = (15, 2, 255)
    RED   = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREY = (73, 73, 73)
    WHITISH = (214, 214, 214)

class Next_Play(Enum):
    TOP_LEFT = (0,0)
    TOP_MIDDLE = (1,0)
    TOP_RIGHT = (2,0)
    MIDDLE_LEFT = (0,1)
    MIDDLE_MIDDLE = (1,1)
    MIDDLE_RIGHT = (2,1)
    BOTTOM_LEFT = (0,2)
    BOTOM_MIDDLE = (1,2)
    BOTTOM_RIGHT = (2,2)

def within_Range(val, start, stop):
	return start < val < stop

def dist_Between_Points(point1, point2):
    return sqrt( ( ( point2[0] - point1[0] ) ** 2 ) + (  (  point2[1] - point1[1] ) ** 2 ) )
