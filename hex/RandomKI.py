from EventManager import *
from HexBoard import *
from Size import *
from random import shuffle
from PlayerController import PlayerController
from PatternMatcher import *

class RandomKI(PlayerController):
    
    def __init__(self, m, n):
        
        super().__init__()
        
        self._moveCounter = 1
        
        self._movesReceived = 0
        self._movesCalculated = 0
        
        self.Size = Size(m,n)
        
        self.HexBoard = HexBoard(self.Size.m, self.Size.n)
        self.HexBoard.setReferenceToGame(self)
        self.HexBoard.suppressEvents()
        
        
        self.PatternMatcher = None
        #self.MCTS = MCTS()
        
        # pattern, mcts, random
        self.modeCounter = [0,0,0]
    
    
    def receiveMove(self, move):
        
        self._movesReceived += 1
        
        # notify Model
        self.HexBoard.receiveMove([move[0], move[1]])
        
        self._moveCounter = self._moveCounter + 1
        
        if self._moveCounter == 2:
            self.PatternMatcher = PatternMatcher(self.HexBoard, self)
        
        
        self.changePlayer()
        
        
    def nextMove(self):
        
        self._movesCalculated += 1
        
        # get the next move
        return self.calculateMove()
    
    #calculateMove(self) soll den na ̈chsten Zug berechnen und True zuru ̈ckgeben, wenn die Berechnung fertiggestellt ist. Beim Testen werden wir Ihre Prozesse nach einer gewissen Zeit abbrechen. Es sollte also immer eine Mo ̈glichkeit fu ̈r einen na ̈chsten Zug (in einer Instanzvariable) gespeichert sein.
    def calculateMove(self):
        
        vertices = self.HexBoard.getVertices("unmarked")
        
        shuffle(vertices)
        vertex = vertices.pop()
        print("Random")
        return [vertex.i, vertex.j]
    
    
    # read the current board
    def readBoard(self, board, myturn):
        
        self.HexBoard.readBoard(board, myturn)

    # get current state of the board
    def getBoard(self):
        
        Vertices = []
        
        for i in range(self.Size.m):
            VertexRow = []
            for j in range(self.Size.n):
                player = self.HexBoard.getVertex(i, j).player
                if player == None:
                    player = 0
                VertexRow.append(player)
            
            Vertices.append(VertexRow)
        
        return Vertices





