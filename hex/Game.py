from HexGUI import *
from HexKI import *
from HexBoard import HexBoard

from PlayerController import *

from EventManager import EventManager
from Size import *
from MachineGUI import *

import random


class Game(PlayerController):
    
    
    
    def __init__(self, m, n, mode):
        
        super().__init__()
        
        # init all events
        EventManager.initEvents()
        
        EventManager.subscribe("GameFinished", self.onGameFinished)
        EventManager.subscribe("GameStarted", self.onGameStarted)
        EventManager.subscribe("ToggleVictoryPath", self.onToggleVictoryPath)
        
        self._pause = False
        
        # save size and mode
        self.Size = Size(m,n)
        self.mode = mode
        
        # instantiate model and view
        self.HexBoard = HexBoard(self.Size.m, self.Size.n)
        self.HexBoard.setReferenceToGame(self)
        
        self.GameState = 0
        
        self.moveCounter = 0
        
        if self.UIRequired():
            self.HexGUI = HexGUI(self.Size.m, self.Size.n, self)
        else:
            self.MachineGUI = MachineGUI(self.Size.m, self.Size.n, self)
        
        if self.mode == "ki":
            self.KI = HexKI(self.Size.m, self.Size.n)
        
        if self.mode == "inter" or self.mode == "machine":
            
            self.KI = []
            self.KI.append(HexKI(self.Size.m, self.Size.n))
            self.KI.append(HexKI(self.Size.m, self.Size.n))
            
            self._currentPlayerType = "ki"
        
        
        if self.UIRequired():
            
            EventManager.subscribe("UITick", self.onUITick)
            
            # main loop starts for event receiving
            self.HexGUI.mainloop()
        
        if self.UIRequired() == False:
            self.GameState = 1
            self.MachineGUI.gameLoop()
        
        
        
    # called every nth milliseconds / specified in HexGUI
    def onUITick(self):
        
        # do the KI Move if current player is KI
        self.doKIMove()
        
    
    # toggle visibility of current player's victory path
    def onToggleVictoryPath(self):
        
        # but just if UI is really required
        if self.UIRequired():
            
            # get the vertices from the board
            vertices = self.HexBoard.getVictoryPath()
            
            # and pass them over to the GUI
            self.HexGUI._GUIGameBoard.Pattern.toggleVictoryPath(vertices)
            self.HexGUI.draw()
    
    # pause the KI movements 
    def pause(self):
        self._pause = not self._pause
    
    # is the UI required (used for game anylsis "machine" mode)
    def UIRequired(self):
        
        if self.mode == "human" or self.mode == "ki" or self.mode == "inter":
            return True
        else:
            return False
    
    # start a new round
    def start(self, firstPlayer):
        
        self.GameState = 0
        
        EventManager.notify("GameStarting")
        
        # move counter init
        self.moveCounter = 0
        
        # generate fresh state
        self.HexBoard = HexBoard(self.Size.m, self.Size.n)
        self.HexBoard.setReferenceToGame(self)
        
        # current player depending on decision
        self._currentPlayer = firstPlayer
        
        # if random number wanted, generate one
        if firstPlayer == 0:
            self.chooseFirst()
        
        
        if self.mode == "ki":
            self.KI = HexKI(self.Size.m, self.Size.n)
        
        if self.mode == "inter" or self.mode == "machine":
            
            self.KI = []
            self.KI.append(HexKI(self.Size.m, self.Size.n))
            self.KI.append(HexKI(self.Size.m, self.Size.n))
            
            self._currentPlayerType = "ki"
        
        EventManager.notify("GameStarted")
    
    def onGameStarted(self):
        
        self.GameState = 1
        
        if self.UIRequired():
            # draw the gui
            self.HexGUI.draw()
        
        
    # Game finished event
    def onGameFinished(self):
        
        self.GameState = 0
        
        if self.UIRequired():
            # move over to main menu and present the winner
            #self.HexGUI.openPage("menu")
            self.HexGUI.won(self.HexBoard.winner())
    
    def loadState(self):
        
        state = [[0, 2, 0, 0, 0, 0, 0, 2, 2, 0, 2], [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0], [2, 2, 2, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 2, 2, 0, 1, 0, 0, 0, 0], [2, 0, 2, 1, 1, 1, 1, 1, 0, 0, 0], [0, 1, 1, 0, 2, 2, 1, 1, 1, 2, 0], [1, 1, 2, 2, 0, 0, 2, 0, 1, 0, 0], [1, 1, 2, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 2], [2, 2, 0, 0, 1, 2, 1, 1, 0, 1, 1]]

        self.HexBoard.readBoard(state)

    
    # control flow for click event
    def makeMove(self, move):
        
        
                
        # Notify 
        EventManager.notify("MoveBegan")
        
        # if already marked dont do anything
        if self.HexBoard.isMarked(move[0], move[1]):
            EventManager.notify("MoveDenied")
            
        else:
            
            # otherwise count the click
            self.moveCounter = self.moveCounter + 1
            
            # notify Model
            self.HexBoard.receiveMove(move)
            
            if self.mode == "inter":
                self.KI[0].receiveMove(move)
                self.KI[1].receiveMove(move)
                '''if self.moveCounter > 3:
                    print(self.KI[0].PatternMatcher.mapGameState())
                    print(self.KI[1].PatternMatcher.mapGameState())'''
            elif self.mode == "ki":
                self.KI.receiveMove(move)
            
            # notify View
            self.changePlayer()
            EventManager.notify("PlayerChanged")
 
        EventManager.notify("MoveFinished")
    
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
    
    def doKIMove(self):
        
        if self.GameState == 1:
            
            if not self.isPlayerHuman() and self.mode == "ki":
                move = self.KI.nextMove()
                self.makeMove(move)
    
            elif self.mode == "inter" or self.mode == "machine":
                move = self.KI[self.currentPlayer()-1].nextMove()
                self.makeMove(move)
        
        