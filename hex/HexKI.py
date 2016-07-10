from HexBoard import *
from EventManager import *

from PlayerController import *

from PatternMatcher import PatternMatcher
from Size import *

from random import shuffle

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
        
        self.PatternMatcher = None
        #self.MCTS = MCTS()
        
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
            
        self.changePlayer()
        self._moveCounter = self._moveCounter + 1
        
    def nextMove(self):
        
        self._movesCalculated += 1
        
        self._myTurn = True
        
        # get the next move
        return self.calculateMove()
    
    #chooseOrder(self, firstmove) soll basierend auf dem ersten Zug entscheiden, ob als zweiter Spieler weitergespielt wird oder stattdessen der Computergegner als erster Spieler spielt. Der Ru ̈ckgabewert soll 1 oder 2 sein; bei 1 soll der Computergegner als erster Spieler weiterspielen, bei 2 soll er zweiter Spieler bleiben.
    #def chooseOrder(self, firstmove):
    #   Schranke = ((self.Board.size[0] // 2) // 2)
     #   i = firstmove[1]
      #  j = firstmove[0]
       # if (i > Schranke and (j > Schranke or j < (self.Board.size[1] -1) - Schranke)) or ((i < ((self.Board.size[0] -1) - Schranke))and (j > Schranke or j < (self.Board.size[1] -1) - Schranke)):
        #DO SWAP PLAYER 

    #calculateMove(self) soll den na ̈chsten Zug berechnen und True zuru ̈ckgeben, wenn die Berechnung fertiggestellt ist. Beim Testen werden wir Ihre Prozesse nach einer gewissen Zeit abbrechen. Es sollte also immer eine Mo ̈glichkeit fu ̈r einen na ̈chsten Zug (in einer Instanzvariable) gespeichert sein.
    def calculateMove(self):
        # asymmetric board
        if self.Size.m != self.Size.n:
            if self._moveCounter == 1:
                # calc first move
                return [round(self.Size.m * 0.75), round(self.Size.n * 0.75)]
            
            else:
                Movege= self.HexBoard.getLastMove()
                i=Movege[0]
                j=Movege[1]
                
                if self.Size.m < self.Size.n:
                    unters=self.Size.n-self.Size.m 
                    maxi=self.Size.m -1 
                    maxj=self.Size.n -unters
                    if (i+j) < maxj:
                        gesj=maxj-i
                        gesi=maxi-j
                    else:
                        gesj=maxi-i
                        gesi=maxj-j
                        
                    #restspalten    
                    if unters/2!=1 and unters!=1 and j>maxj:
                        if j/2==1:
                            gesj= j+1
                            gesi= i
                        else:
                            gesj=j-1
                            gesi=i
                    if unters!=1 and j>maxj:
                        if j==self.Size.n-1 and i ==self.Size.m-1:
                            vertices = self.HexBoard.getVertices("unmarked")
                            shuffle(vertices)
                            vertex = vertices.pop()
                            move = [vertex.i, vertex.j]
                            return move
                            
                        if j!= self.Size.n-1:
                            if j%2==1 :
                                gesj= j-1
                                gesi= i
                            else:
                                gesj=j+1
                                gesi=i
                        else:
                            if i%2==1:
                                gesj=j
                                gesi=i-1
                            else:
                                gesj=j
                                gesi=i+1
                
                
                #länger als breiter                
                else:
                    unters=self.Size.m-self.Size.n 
                    maxj=self.Size.n -1 
                    maxi=self.Size.m -unters
                    if (i+j) < maxi:
                        gesi=maxi-j
                        gesj=maxj-i
                    else:
                        gesi=maxj-j
                        gesj=maxi-i
                    
                    if unters!=1 and j>maxj:
                        if j%2==1:
                            gesj= j+1
                            gesi= i
                        else:
                            gesj=j-1
                            gesi=i
                            
                    if unters!=1 and i>maxi:
                        if j==self.Size.n-1 and i ==self.Size.m-1:
                            vertices = self.HexBoard.getVertices("unmarked")
                            shuffle(vertices)
                            vertex = vertices.pop()
                            move = [vertex.i, vertex.j]
                            return move
                            
                        if i!= self.Size.m-1:
                            if i%2==1 :
                                gesi= i-1
                                gesj= j
                            else:
                                gesi=i+1
                                gesj=j
                        else:
                            if j%2==1:
                                gesi=i
                                gesj=j-1
                            else:
                                gesi=i
                                gesj=j+1
                                
                if self.HexBoard.isMarked(gesi,gesj)==True:
                    vertices = self.HexBoard.getVertices("unmarked")
                    shuffle(vertices)
                    vertex = vertices.pop()
                    move = [vertex.i, vertex.j]
                    return move
                    
                gesmove=[gesi,gesj]
                    
                return gesmove
        
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
                self.modeCounter[2] += 1
                vertices = self.HexBoard.getVertices("unmarked")
                shuffle(vertices)
                vertex = vertices.pop()
                
                move = [vertex.i, vertex.j]
        
        
        return move
    
    
    # read the current board
    def readBoard(self, board, current = True):
        self.HexBoard.readBoard(board, current)






