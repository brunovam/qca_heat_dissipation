import sys


class QCADCell(object):
	def __init__(self, x, y, mode, function, clock):
 		self.x = x
 		self.y = y
 		self.mode = mode
 		self.function = function
 		self.clock = clock


# Transformar as coordenadas em espaciais em posicoes do grid

def read_qca_file ():
	block_tag = []
	cells = []
	inputs = []
	outputs = []
#	circuit_layout = ???

	if len(sys.argv) == 1:
		print "You have to add the qca file as a first argument to this script"
		exit(1)
	with open(sys.argv[1]) as f:
 		for line in f.readlines():
			if (line[0] == '['):
				if (line[1] != '#'):
					block_tag.append(line[0:-1])
				else:
					if (len(block_tag) >= 3):
						if (block_tag[-1] == '[TYPE:QCADCell]'):
							cells.append(QCADCell(x, y, mode, function, clock))
#							circuit_layout [x][y][clock] = len(cells) - 1
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
# 					print 'clock= ' + clock
 				if (line[0:14] == 'cell_function='):
 					function = line[14:-1]
# 					print 'function= ' + function
 				if (line[0:18] == 'cell_options.mode='):
 					mode = line[18:]
# 					print 'mode= ' + mode
                        elif (len(block_tag) >= 3):
				if ((block_tag[-2] == '[TYPE:QCADCell]') & (block_tag[-1] == '[TYPE:QCADDesignObject]')):
					if (line[0:2] == 'x='):
 						x = float(line[2:])
# 						print  'String ', line, '***|x = ', x
					if (line[0:2] == 'y='):
 						y = float(line[2:])
# 						print  'String ', line, '***|y = ',  y
#			print block_tag
#	return [cells, circuit_layout, inputs, outputs]
	return cells

cells = read_qca_file()
print len(cells)
