from tkinter import *
import random
import collections
from EventManager import EventManager
from random import shuffle
from HexKI import HexKI
from HexBoard import HexBoard
from RandomKI import RandomKI


class MachineGUI:
    
    def __init__(self, m, n, game):
        self.size = [m,n]
        self.Game = game
        
        EventManager.subscribe("GameFinished", self.onGameFinished)
        
        self._finished = False
        
        self.targetIterations = 200
        self.q = 0 
        
        self.start()
        
        
        print("MachineGUI loaded")
    
    def start(self):
        
        self.KI = []
        self.KI.append(RandomKI(self.size[0], self.size[1]))
        self.KI.append(HexKI(self.size[0], self.size[1]))
        
        self.Game.HexBoard = HexBoard(self.size[0], self.size[1])
        self.Game.HexBoard.setReferenceToGame(self.Game)
    
    WonVertices = []
    IterationCounter = 0
    
        
    def gameLoop(self):
        
        print("Entering Game Loop")
        player = 1
        Q = []
        Winners = []
        while self.IterationCounter < self.targetIterations:
            
            q= 0
            while not self._finished:

                q += 1
                if player == 0:
                    player = 1
                else:
                    player = 0
                
                move = self.KI[player].nextMove()
                
                
                self.KI[0].receiveMove(move)
                self.KI[1].receiveMove(move)
                self.Game.makeMove(move)
                
                #if self.KI[1]._moveCounter > 3:
                #    #print("------")
                #    #print(self.KI[0].PatternMatcher.mapGameState())
                #    #print(self.KI[1].PatternMatcher.mapGameState())
                
            Winners.append(self.Game.HexBoard.winner())
            Q.append([self.Game.HexBoard.winner(), q, self.KI[0].getBoard()])
            
            self.IterationCounter = self.IterationCounter + 1
            
            
            
            for key, value in self.Game.HexBoard.Vertices.items():
                if value.player == self.Game.HexBoard.winner():
                    self.WonVertices.append(str(value.i) + ";" + str(value.j))
            
            if self.IterationCounter // (self.targetIterations / 20) != self.q:
                self.q = self.IterationCounter // (self.targetIterations / 20)
                print(round(self.IterationCounter/self.targetIterations * 100,1), "%", self.IterationCounter)
            
            self.Game.HexBoard = HexBoard(self.size[0], self.size[1])
            self.Game.HexBoard.setReferenceToGame(self.Game)
            
            self._finished = False
            self.start()
            
        print("Iterations finished")
        print("Start writing output files")
        
        Q = sorted(Q, key=lambda x:x[1])
        
        f = open('output.txt', 'w+')
        
        f.write("Most used vertices: \n")
        
        f.write(str(collections.Counter(self.WonVertices)) + "\n\n")
        
        f.write("Win statistics:\n\n")
        
        f.write("1 gewonnen: " + str(round(Winners.count(1)*100/len(Winners))) + "%, 2 gewonnen: " + str(round(Winners.count(2)*100/len(Winners))) + "%\n\n")
        
        f.write("moves per game // game state to be loaded @ Game->loadState()\n")
        
        for q in Q:
            f.write((str(q[0]) + "," + str(q[1]) + "," + str(q[2]) + "\n"))
        
        
        
        print("Output files written")
        print("Terminated")
        print("------------------")

    def onGameFinished(self):
        #print("Spieler", self.Game.HexBoard.winner(), "hat gewonnen!")
        self._finished = True
        
    def receiveMove(self, move):
        # do somehting
        return 0
    
    def won(self, winner):
        print("won")