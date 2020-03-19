from enum import Enum


class Bind(Enum):
    FWD = 'forward'
    BWD = 'backward'
    RIGHT = 'right'
    LEFT = 'left'
    UP = 'up'
    DOWN = 'down'
    SPACE = 'space'
    EQ = 'equipment'
    DEBUG = 'debug'
    EXIT = 'exit'
