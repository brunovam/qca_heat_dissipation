import graph
import qca
import e

# Converte para um grafo de portas e elementos, seguindo a regra que mudanca de clocks, birfucacoes e celulas que forma portas
# Sao vertices aresta do grafo.

def process_nodes(graphElements, graphCells, nodeCell, nodeElement):
    #print("node cell %d node element %d %s" % (nodeCell.number, nodeElement.number, nodeCell))
    z = 20
    nodeCell.color = "c"
    previousCell = nodeCell.cell
    found = 0

    # Busca as celulas vizinhas.
    for nodeNeigborCell in graphCells.get_neighbors(nodeCell.number):
        cellNeigbor = nodeNeigborCell.cell
        
        if nodeNeigborCell != nodeCell:
            
            # Verifica se o vertice ja foi visitado
            if nodeNeigborCell.color == "b":
                found = 1
                newNodeElement = None
                
                # Verifica se houve mudanca de clock, isso significa um novo vertice
                if previousCell.clock != cellNeigbor.clock:
                    newNodeElement = graphElements.create_next_node(nodeElement, e.Element(e.ElementType.Line, previousCell.function, previousCell.clock, previousCell))
                    cellNeigbor.segmento = newNodeElement.number
                else:
                    # Apartir do numero de conexoes podemos deduzir os tipos de porta
                    conections = len(graphCells.get_neighbors(nodeNeigborCell.number)) - 2
                    type = None
                    
                    # Iniciamente pode ser: MajorGate, And ou Or
                    if conections == 3:
                        type = e.ElementType.MajorGate
                    
                    # Iniciamente pode ser uma bifurcacao
                    #elif conections == 2:
                    #    type = e.ElementType.Bifurcation

                    #inveror na horizontal ou inversor na vertical
                    if (abs(cellNeigbor.x - previousCell.x) == z and abs(cellNeigbor.y - previousCell.y) == z / 2) or (abs(cellNeigbor.y - previousCell.y) == z and abs(cellNeigbor.x - previousCell.y) == z / 2):
                        type = e.ElementType.Inverter

                    # Verifica o tipo de elemento
                    if type == None:
                        
                        # Verifica se é uma célula fixa, isso pode mudar o tipo do elemento anterior para Porta OR ou AND
                        if cellNeigbor.function == "QCAD_CELL_FIXED":
                            if nodeElement.cell.type == e.ElementType.Trifurcation:
                                if cellNeigbor.value == 1.0:
                                    nodeElement.cell.type = e.ElementType.PortOr
                                elif cellNeigbor.value == -1.0:
                                    nodeElement.cell.type = e.ElementType.PortAnd
                        
                        # Verifica se é uma entrada, com isso o tipo será um MajorGate, pois contém mais de uma entrada.
                        elif cellNeigbor.function == "QCAD_CELL_INPUT":
                            if nodeElement.cell.type == e.ElementType.Trifurcation:
                                nodeElement.cell.type = e.ElementType.MajorGate
                    else:
                        newNodeElement = graphElements.create_next_node(nodeElement, e.Element(type, previousCell.function, previousCell.clock, previousCell))
                        cellNeigbor.segmento = newNodeElement.number
                
                if newNodeElement == None:
                    newNodeElement = nodeElement
                process_nodes(graphElements, graphCells, nodeNeigborCell, newNodeElement)
            else:
                # Se ja foi visitado, entao, somente, cria uma aresta, se a mesma já não existe.
                node1 = graphElements.get_node(cellNeigbor.segmento)
                if not graphElements.check_edge(node1, nodeElement):
                    #node2 = graphFinal.get_node(node.cell.segmento)
                    graphElements.insert_edge(node1, nodeElement)
                    graphElements.insert_edge(nodeElement, node1)
                
    # Verifica se eh o fim de percurso.
    if found == 0:
        if previousCell.function == "QCAD_CELL_FIXED":
            type = e.ElementType.Fixed
        elif previousCell.function == "QCAD_CELL_OUTPUT":
            type = e.ElementType.Output
        elif previousCell.function == "QCAD_CELL_INPUT":
            type = e.ElementType.Input
        else:
            type = None
            print("Fim de percurso sem porta de saida... %s" % previousCell.function)
        if type != None:
            graphElements.create_next_node(nodeElement, e.Element(type, previousCell.function, previousCell.clock, previousCell))

def convert(graphCells):
    graphFinal = graph.Graph()
    for node in graphCells.starts:
        if node.color == "b":
            cell = node.cell
            if cell.function == "QCAD_CELL_INPUT":
                type = e.ElementType.Input
            elif cell.function == "QCAD_CELL_FIXED":
                type = e.ElementType.Fixed
            newNode = graph.Node(graphFinal.get_length(), e.Element(type, cell.function, cell.clock, cell))
            cell.segmento = newNode.number
            graphFinal.insert_node(newNode, True)
            process_nodes(graphFinal, graphCells, node, newNode)

#    for n in graphFinal.graph:
#        print("\n%d" % (n) )
#        for node in graphFinal.graph[n]:
#            #print("\t %" % node)
#            print("\t(node %d type %s x %d y %d)" % (node.number, node.cell.type, node.cell.cell.x, node.cell.cell.y))
            
    return graphFinal
