from enum import Enum
class ElementType(Enum):
    Fixed = 0
    Input = 1
    Line = 2
    PortAnd = 3
    PortOr = 4
    Bifurcation = 5
    Trifurcation = 6
    Inverter = 7
    MajorGate = 8
    Output = 9
    
class Element(object):
    def __init__(self, type, function, clock, cell):
        self.type = type
        self.function = function
        self.clock = clock
        self.cell = cell
