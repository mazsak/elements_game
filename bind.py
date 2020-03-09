from enum import Enum


class Bind(Enum):
    FWD = 'forward'
    BWD = 'backward'
    RIGHT = 'right'
    LEFT = 'left'
    UP = 'up'
    DOWN = 'down'
    EQ = 'equipment'
    EXIT = 'exit'
