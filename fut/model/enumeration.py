from enum import Enum

class State(Enum):
    """Creates enum for service"""
    pending         = 0
    search          = 1
    chooseTrades    = 2
    watchTrades     = 3
    wait            = 4
    saveTrades      = 5
    delete          = 6