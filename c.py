import graph
import qca
import e

# Converte para um grafo de portas e elementos, seguindo a regra que mudanca de clocks, birfucacoes e celulas que forma portas
# Sao vertices aresta do grafo.

def process_nodes(graphElements, graphCells, nodeCell, nodeElement):
    nodeCell.color = "c"
    previousCell = nodeCell.cell
    found = 0

    # Busca as celulas vizinhas.
    for nodeNeigborCell in graphCells.get_neighbors(nodeCell.number):
        cellNeigbor = nodeNeigborCell.cell
        
        if nodeNeigborCell != nodeCell:
            print("node inicial %d (%s) vizinho %d .." % (nodeCell.number, nodeCell.cell.function, nodeNeigborCell.number))
            
            # Verifica se o vertice ja foi visitado
            if nodeNeigborCell.color == "b":
                found = 1
                newNodeElement = None
                
                # Verifica se houve mudanca de clock, isso significa um novo vertice
                if previousCell.clock != cellNeigbor.clock:
                    newNodeElement = graphElements.create_next_node(nodeElement, e.Element(e.ElementType.Line, previousCell.function, previousCell.clock))
                    cellNeigbor.segmento = newNodeElement.number
                    print("\t\tVertice %d..." % newNodeElement.number)
                else:
                    # Apartir do numero de conexoes podemos deduzir os tipos de porta
                    conections = len(graphCells.get_neighbors(nodeNeigborCell.number)) - 2
                    type = None
                    
                    # Iniciamente pode ser: trifurcacao, MajorGate, And ou Or
                    if conections == 3:
                        type = e.ElementType.Trifurcation
                    
                    # Iniciamente pode ser uma bifurcacao
                    elif conections == 2:
                        type = e.ElementType.Bifurcation

                    # Verifica o tipo de elemento
                    if type == None:
                        
                        # Verifica se é uma célula fixa, isso pode mudar o tipo do elemento anterior.
                        if cellNeigbor.function == "QCAD_CELL_FIXED":
                            print("Fixa %d %s %s" % (cellNeigbor.value, cellNeigbor.value == -1.0, nodeElement.cell.type))
                            if nodeElement.cell.type == e.ElementType.Trifurcation:
                                if cellNeigbor.value == 1.0:
                                    print("PortaOR")
                                    nodeElement.cell.type = e.ElementType.PortOr
                                elif cellNeigbor.value == -1.0:
                                    print("PortaAND")
                                    nodeElement.cell.type = e.ElementType.PortAnd
                    else:
                        newNodeElement = graphElements.create_next_node(nodeElement, e.Element(type, previousCell.function, previousCell.clock, previousCell))
                        cellNeigbor.segmento = newNodeElement.number
                        print("\t\tVertice doido %d %d .." % (cellNeigbor.segmento, newNodeElement.number))
                
                if newNodeElement == None:
                    newNodeElement = nodeElement
                process_nodes(graphElements, graphCells, nodeNeigborCell, newNodeElement)
            else:
                # Se ja foi visitado, entao, somente, cria uma aresta.
                node1 = graphElements.get_node(cellNeigbor.segmento)
                if not graphElements.check_edge(node1, nodeElement):
                    print("\t\tligacao seguimento... number %d celula %d node %d" % (nodeNeigborCell.number, cellNeigbor.segmento, node1.number))
                    #node2 = graphFinal.get_node(node.cell.segmento)
                    graphElements.insert_edge(node1, nodeElement)
                    graphElements.insert_edge(nodeElement, node1)
                
    # Verifica se nao e um fim de percurso.
    print("Found %d" % found)
    if found == 0:
        print("\t\tfim do seguimento...fim")
        if previousCell.function == "QCAD_CELL_FIXED":
            type = e.ElementType.Fixed
        elif previousCell.function == "QCAD_CELL_OUTPUT":
            type = e.ElementType.Output
        elif previousCell.function == "QCAD_CELL_INPUT":
            type = e.ElementType.Input
        graphElements.create_next_node(nodeElement, e.Element(type, previousCell.function, previousCell.clock, previousCell))

def convert(cells):
    graphFinal = graph.Graph()
    for node in cells.starts:
        cell = node.cell
        print("\tNode %d %d %s" % (cell.x, cell.y, cell.function))
        newNode = graph.Node(graphFinal.get_length(), e.Element(e.ElementType.Input, cell.function, cell.clock, cell))
        cell.segmento = newNode.number
        print("\t\tVertice %d %d .." % (cell.segmento, newNode.number))
        print("Node celular %d segmento %d" % (cell.segmento, newNode.number))
        graphFinal.insert_node(newNode, True)
        process_nodes(graphFinal, cells, node, newNode)

    for n in graphFinal.graph:
        print("\n%d" % (n) )
        for node in graphFinal.graph[n]:
            print("\t(node %d type %s x %d y %d)" % (node.number, node.cell.type, node.cell.cell.x, node.cell.cell.y))
            
    return graphFinal
