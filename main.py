import sys
import graph
import e
import c
import qca
    
# Transformar as coordenadas em espaciais em posicoes do grid

def read_qca_file ():
    block_tag = []
    cells = []
    inputs = []
    outputs = []
#    circuit_layout = ???

    if len(sys.argv) == 1:
        print("You have to add the qca file as a first argument to this script")
        exit(1)
    with open(sys.argv[1]) as f:
         value = 0
         for line in f.readlines():
            line = line.replace("\r\n","").replace("\n","").replace("\r","")

            if (line[0] == '['):
                if (line[1] != '#'):
                    block_tag.append(line)
                else:
                    if (len(block_tag) >= 3):
                        if (block_tag[-1] == '[TYPE:QCADCell]'):
                            cell = qca.QCADCell(x, y, mode, function, clock, value)
                            cells.append(cell)
#                            circuit_layout [x][y][clock] = len(cells) - 1
                            if (function ==  'QCAD_CELL_INPUT'):
                                inputs.append(len(cells) - 1)
                            if (function ==  'QCAD_CELL_OUTPUT'):
                                outputs.append(len(cells) - 1)
                            del clock
                            del function
                            del mode
                            del x
                            del y
                    del block_tag[-1]
            elif (block_tag[-1] == '[TYPE:QCADCell]'):
                if (line[0:19] == 'cell_options.clock='):
                    clock = line[19:]
#                     print 'clock= ' + clock
                if (line[0:14] == 'cell_function='):
                    function = line[14:]#-1
                if (line[0:18] == 'cell_options.mode='):
                     mode = line[18:]
#                    print 'mode= ' + mode
            elif (len(block_tag) >= 3):
                #print(block_tag[2])
                #[TYPE:CELL_DOT]
                if ((block_tag[-2] == '[TYPE:QCADCell]') & (block_tag[-1] == '[TYPE:QCADDesignObject]')):
                    if (line[0:2] == 'x='):

                         x = float(line[2:].replace(",","."))
#                         print  'String ', line, '***|x = ', x
                    if (line[0:2] == 'y='):
                         y = float(line[2:].replace(",","."))
                         #print('String ', line, '***|y = ',  y)
            
#            print block_tag
#    return [cells, circuit_layout, inputs, outputs]
    return cells

cells = read_qca_file()

#for cell in cells:
#    print("X: %d" % cell.x)
#    print("Y: %d" % cell.y)
#    print("Mode: %s" % cell.mode)
#    print("Function: %s" % cell.function)
#    print("Clock: %s" % cell.clock)
#    print("\n")

g = graph.Graph()
count = 0
for cell in cells:
    n = graph.Node(count, cell)
    g.insert_node(n, cell.function == "QCAD_CELL_INPUT" or cell.function == "QCAD_CELL_FIXED")
    count += 1

z = 20
cell_number = 0

for cell in cells:
    node1 = g.get_node(cell_number)
    cell2_number = 0
    for cell2 in cells:
        if cell_number == cell2_number:
            continue
        node2 = g.get_node(cell2_number)
        if node1.cell.x == node2.cell.x or abs(node1.cell.x - node2.cell.x) == z / 2:
            if abs(node1.cell.y - node2.cell.y) == z:
#                print("\tNode %d %d %d %s" % (node1.number, node1.cell.x, node1.cell.y, node1.cell.function))
#                print("\t\tNode %d %d %d %s" % (node2.number, node2.cell.x, node2.cell.y, node2.cell.function))
#                print("%d\t%d " % (node1.number, node2.number))
                g.insert_edge(node1, node2)
                g.insert_edge(node2, node1)
        elif node1.cell.y == node2.cell.y or abs(node1.cell.y - node2.cell.y) == z / 2:
            if abs(node1.cell.x - node2.cell.x) == z:
#                print("\tNode %d %d %d %s" % (node1.number, node1.cell.x, node1.cell.y, node1.cell.function))
#                print("\t\tNode %d %d %d %s" % (node2.number, node2.cell.x, node2.cell.y, node2.cell.function))
#                print("%d\t%d " % (node1.number, node2.number))
                g.insert_edge(node1, node2)
                g.insert_edge(node2, node1)
        cell2_number += 1
    cell_number += 1
#g.print_graph()
c.convert(g)
