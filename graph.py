class Node:
    number = None
    cell = None
    def __init__(self, number, cell):
        self.number = number
        self.cell = cell

class Graph:
    graph = None
    def __init__(self):
        self.graph = {}

    def insert_node(self, node):
        if not node.number in self.graph.keys():
            self.graph[node.number] = [node]

    def insert_edge(self, node1, node2):
        if not node1.number in self.graph.keys():
            return False
        if not node2.number in self.graph.keys():
            return False
        self.graph[node1.number].append(node2)

    def print_graph(self):
        for n in self.graph:
            print "\n%d" % n
            for node in self.graph[n]:
                print "\t%d" % node.number

    def get_node(self, number):
        if number in self.graph:
            return self.graph[number][0]
