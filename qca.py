class QCADCell(object):
    segmento = 0
    def __init__(self, x, y, mode, function, clock, value):
        self.x = x
        self.y = y
        self.mode = mode
        self.function = function
        self.clock = clock
        self.value = value
