from HexBoardKI import *
from EventManager import *
from PatternMatcher import PatternMatcher
from random import shuffle

class Size:
    def __init__(self, m = 0, n = 0):
        self.m = m
        self.n = n

    def getWidth(self):
        return self.n
    
    def getHeight(self):
        return self.m



class HexKI:
    
    def __init__(self, m, n):
        
        
        self._moveCounter = 1
        
        self._movesReceived = 0
        self._movesCalculated = 0
        
        self._myTurn = False
        
        self.Size = Size(m,n)
        
        self.HexBoard = HexBoardKI(self.Size.m, self.Size.n)
        
        
        self.PatternMatcher = None
        #self.MCTS = MCTS()
        
        self._player = 0
        
        # pattern, mcts, random
        self.modeCounter = [0,0,0]
        
    def getPlayer(self):
        return self._player
    
    def getEnemy(self):
        
        if self._player == 1:
            return 2
        else:
            return 1
    
    
    def receiveMove(self, move):
        
        self._movesReceived += 1
        
        # notify Model
        if self._myTurn:
            self.HexBoard.receiveMoveByPlayer([move[0], move[1]], "player")
        else:
            self.HexBoard.receiveMoveByPlayer([move[0], move[1]], "enemy")
        self._myTurn = False
        
        self._moveCounter = self._moveCounter + 1
        
        # finnaly it's possible to determine where we should play
        if self._moveCounter == 2:

            if self._movesCalculated != self._movesReceived:
                self._player = 2
            else:
                self._player = 1
            
            
            self.HexBoard.setPlayer(self._player)
            self.PatternMatcher = PatternMatcher(self.HexBoard, self)
            
        
        if sum(self.modeCounter) > 0:
            pass#print(round((self.modeCounter[0] * 100 / sum(self.modeCounter))),round((self.modeCounter[1] * 100 / sum(self.modeCounter))),round((self.modeCounter[2] * 100 / sum(self.modeCounter))))
        
            if self.modeCounter[0]/sum(self.modeCounter) < 0.8:
                pass#self.Game.pause()  
        
    def nextMove(self):
        
        self._movesCalculated += 1
        
        self._myTurn = True
        
        # get the next move
        return self.calculateMove()
    
    #chooseOrder(self, firstmove) soll basierend auf dem ersten Zug entscheiden, ob als zweiter Spieler weitergespielt wird oder stattdessen der Computergegner als erster Spieler spielt. Der Ru ̈ckgabewert soll 1 oder 2 sein; bei 1 soll der Computergegner als erster Spieler weiterspielen, bei 2 soll er zweiter Spieler bleiben.
    def chooseOrder(self, firstmove):
        pass
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
                    
                    move = self.PatternMatcher.getMove()
                
                    if move != False:
                        #print("MODE:", "Pattern")
                        self.modeCounter[0] += 1
                        return move
                
                
                # then check the mcts results
                #move = self.MCTS.getMove()
                
                #if move != False:
                #    #print("MODE:", "MCTS")
                #    self.modeCounter[1] += 1
                #    return move
                
                
                # finally pick random
                #print("MODE:", "random")
                self.modeCounter[2] += 1
                vertices = self.HexBoard.getVertices("unmarked")
                shuffle(vertices)
                vertex = vertices.pop()
                
                move = [vertex.i, vertex.j]
        
        
        return move
    
    
    # read the current board
    def readBoard(self):
        pass

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





