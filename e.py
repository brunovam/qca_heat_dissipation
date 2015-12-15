from enum import Enum
class ElementType(Enum):
    Fixed = 0
    Input = 1
    Line = 2
    PortAnd = 3
    PortOr = 4
    NotAnd = 5
    NotOr = 6   
    Inverter = 7
    MajorGate = 8
    Output = 9
    Trifurcation = 10
    
class Element(object):
    values = []

    def __init__(self, type, function, clock, cell):
        self.type = type
        self.function = function
        self.clock = clock
        self.cell = cell
    def __str__(self):        
        return "type: %s function: %s clock: %s cell: %s" % (self.type, self.function, self.clock, self.cell)
    
    def get_saida(self, graph, node):
        if len(self.values) == 0:
            self.values = self.__get_saida(graph, node)
        return self.values
    
    def __get_saida(self, graph, node):
        if self.type == ElementType.Fixed:
            return [self.cell.value];
        elif self.type == ElementType.Input:
            return [0, 1]
        elif self.type == ElementType.OutPut:
            return []
        elif self.type == ElementType.Inverter:
            for nodeNeigbor in graph.get_neighbors(node.number):
                if nodeNeigbor != node:
                    value = nodeNeigbor.get_saida(graph, nodeNeigbor)
                    if len(value) != 0:
                        for v in value:
                            self.values.append(v)
            return self.values;
        elif self.type == ElementType.PortAnd:
            # Busca os elementos vizinhas.
            self.values = []
            for nodeNeigbor in graph.get_neighbors(node.number):
                if nodeNeigbor != node:
                    value = nodeNeigbor.get_saida(graph, nodeNeigbor)
                    if value != None:
                        self.values.append(value)
            return values;
        elif self.type == ElementType.PortOr:
            return [0, 1]
        elif self.type == ElementType.Inverter:
            return [0, 1]
        else:
            print("Nao implementado.")
