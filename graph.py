class Node:
    number = None
    color = "b"
    cell = None
    def __init__(self, number, cell):
        self.number = number
        self.cell = cell

    def __str__(self):
        return "number: %d \n  cell: %s" % (self.number, self.cell)
        
class Graph:
    graph = None
    inputs = None
    def __init__(self):
        self.graph = {}
        self.starts = [] # para determinar os inícios do grafo.

    def get_length(self): 
        return len(self.graph)
    
    def insert_node(self, node, start):
        if not node.number in self.graph.keys():
            self.graph[node.number] = [node]
            if start:
                self.starts.append(node)

    def create_next_node(self, node, item):
        newNode = Node(self.get_length(), item)
        self.insert_node(newNode, False)
        self.insert_edge(node, newNode)
        self.insert_edge(newNode, node)
        return newNode

    def insert_edge(self, node1, node2):
        if not node1.number in self.graph.keys():
            return False
        if not node2.number in self.graph.keys():
            return False
        self.graph[node1.number].append(node2)

    def check_edge(self, node1, node2):
        return node2 in self.graph[node1.number]

    def print_graph(self):
        for n in self.graph:
            print("\n%d" % n)
            for node in self.graph[n]:
                print("\t%d" % node.number)

    def get_node(self, number):
        return self.get_neighbors(number)[0]
        
    def get_neighbors(self, number):
        if number in self.graph:
            return self.graph[number]
