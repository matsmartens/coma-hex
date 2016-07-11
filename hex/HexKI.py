from HexBoard import *
from EventManager import *

from PlayerController import *

from PatternMatcher import PatternMatcher
from Size import *

from random import shuffle
from DynamicPatterns import DynamicPatterns
from MCTS import *
from math import sqrt

class HexKI(PlayerController):
    
    def __init__(self, m, n):
        
        super().__init__()
        
        self._moveCounter = 1
        
        self._movesReceived = 0
        self._movesCalculated = 0
        
        self.Size = Size(m,n)
        
        self.HexBoard = HexBoard(self.Size.m, self.Size.n)
        self.HexBoard.suppressEvents()
        self.HexBoard.setReferenceToGame(self)
        
        self.DynamicPatternMatcher = None
        self.PatternMatcher = None
        self.MCTS = MCTS(self.HexBoard, self)
        
        # pattern, mcts, random
        self.modeCounter = [0,0,0]
    
    def receiveMove(self, move):
        
        self._movesReceived += 1
        
        # notify Model
        self.HexBoard.receiveMove([move[0], move[1]])
        
        
        # finnaly it's possible to determine where we should play
        if self._moveCounter == 1:

            if self._movesCalculated == 0:
                self.setPlayerIdentity(2)
            else:
                self.setPlayerIdentity(1)
        
        if self._moveCounter == 2:
            self.PatternMatcher = PatternMatcher(self.HexBoard, self)
            self.DynamicPatternMatcher = DynamicPatterns(self.HexBoard, self)
            
        self.changePlayer()
        self._moveCounter = self._moveCounter + 1
        
    def nextMove(self):
        
        self._movesCalculated += 1
        
        # get the next move
        return self.calculateMove()
    
    # decides whether to pick first player's move
    # builds a circle around center stone.. inner moves are swapped, outer left as started
    def chooseOrder(self, firstmove):
        
        threshold = self.HexBoard.size[0] // 4
        i = firstmove[1]
        j = firstmove[0]
        
        iCenter = self.Size.m // 2
        jCenter = self.Size.n // 2
        
        distance = sqrt(pow(i-iCenter, 2) + pow(j-jCenter, 2))
        
        if (distance < threshold):
            return 1
        else:
            return 0
    
    #calculateMove(self) soll den na ̈chsten Zug berechnen und True zuru ̈ckgeben, wenn die Berechnung fertiggestellt ist. Beim Testen werden wir Ihre Prozesse nach einer gewissen Zeit abbrechen. Es sollte also immer eine Mo ̈glichkeit fu ̈r einen na ̈chsten Zug (in einer Instanzvariable) gespeichert sein.
    def calculateMove(self):
        # asymmetric board
        if self.Size.m != self.Size.n:
            
            # set the result
            return [0,0]
        
        else:
            
            # if first move
            if self._moveCounter == 1:

                # calc first move 75% down right
                return [round(self.Size.m * 0.75), round(self.Size.n * 0.75)]
            
            
            else:
            
                # first check for patterns
                # but only when it's clear where to play to
                if self._moveCounter >= 3:
                    
                    # get Dynamic Patterns first
                    '''move = self.DynamicPatternMatcher.getMove()
                
                    if move != False:
                        print("MODE:", "Dynamic Pattern found")
                        self.modeCounter[0] += 1
                        return move'''
                    
                    
                    # then get rule network
                    move = self.PatternMatcher.getMove()
                
                    if move != False:
                        #print("MODE:", "Pattern")
                        self.modeCounter[0] += 1
                        return move
                
                
                # then check the mcts results
                move = self.MCTS.getMove()
                
                if move != False:
                    #print("MODE:", "MCTS")
                    self.modeCounter[1] += 1
                    return move
                
                
                # finally pick random
                self.modeCounter[2] += 1
                vertices = self.HexBoard.getVertices("unmarked")
                shuffle(vertices)
                vertex = vertices.pop()
                
                move = [vertex.i, vertex.j]
        
        
        return move
    
    
    # read the current board
    def readBoard(self, board, current = True):
        self.HexBoard.readBoard(board, current)






