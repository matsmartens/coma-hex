class Hexagon:
    
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.player = None
        self.group = None
        self.victorypath = 0
        
    def mark(self, player):
        self.player = player