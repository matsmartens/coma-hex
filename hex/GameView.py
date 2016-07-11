from tkinter import *
from EventManager import *
from HexagonPattern import HexagonPattern

class GameView:
    
    def __init__(self, master, GUI, game):        
        # Size of the Canvas Widget
        self.canvas_width = GUI.screenSize[0]
        self.canvas_height = GUI.screenSize[1]
        
        self.GUI = GUI
        self.Game = game
        
        # Iniitate Canvas object and pack
        self.canvas = Canvas(master, width = self.canvas_width, height = self.canvas_height)
        
        self.canvas.bind("<Motion>", self.onMouseOver)
        self.canvas.bind("<Leave>", self.onMouseLeft)
        self.canvas.bind("<Button>", self.onClick)
        
        self.WinnerLabelText = StringVar()
        self.WinnerLabel = Label(master, textvariable=self.WinnerLabelText)
        
        
        self.ReturnToMenuButton = Button(master, text="Back to Menu", command=self.returnToMenu)
        
        self.LoadStateButton = Button(master, text="Load State", command=self.loadState)
        
        self.PrintStateButton = Button(master, text="Print State", command=self.printState)
        
        self.PlayerSwapButton = Button(master,
                             text="Swap Player",
                             command=self.swapPlayer)
        
        self.ShowVictoryPathButton = Button(master,
                             text="Toggle Victory Path",
                             command=self.toggleVictoryPath)
        
        self.PauseButton = Button(master, text="Pause", command=self.togglePause)
        
        # Create Hexgame Interface
        self.Pattern = HexagonPattern(self)
        
        # Initial Drawing
        self.draw()
    
    def printState(self):
        print(self.Game.getBoard())
    
    def loadState(self):
        self.Game.loadState()
    
    def togglePause(self):
        
        self.Game.pause()
        
    def returnToMenu(self):
        self.GUI.openPage("menu")
        
    def won(self, player):
        self.WinnerLabel.pack(side=LEFT)
        self.WinnerLabelText.set("Player " + str(player) + " won!")
        self.Pattern.won()
    
    def swapPlayer(self):
        self.Game.changePlayer()
        self.Game.HexBoard.switchColors()
        self.hidePlayerSwap()
        self.draw()
    
    def showPlayerSwap(self):
        self.PlayerSwapButton.pack(side=LEFT)
    
    def hidePlayerSwap(self):
        self.PlayerSwapButton.pack_forget()
    
    def show(self):
        self.canvas.pack()
        self.ShowVictoryPathButton.pack(side=LEFT)
        self.ReturnToMenuButton.pack(side=LEFT)
        self.PauseButton.pack(side=LEFT)
        self.LoadStateButton.pack(side=LEFT)
        self.PrintStateButton.pack(side=LEFT)
        
    def hide(self):
        self.canvas.pack_forget()
        self.hidePlayerSwap()
        self.ReturnToMenuButton.pack_forget()
        self.WinnerLabel.pack_forget()
        self.ShowVictoryPathButton.pack_forget()
        self.PauseButton.pack_forget()
        self.LoadStateButton.pack_forget()
        self.PrintStateButton.pack_forget()
    
    def onMouseOver(self, event):
        self.Pattern.onMouseOver(event)
    
    def onMouseLeft(self, event):
        pass
    
    def onClick(self, event):
        if self.Game.isPlayerHuman():
            move = self.Pattern.mapCoordToCell([event.x, event.y])
            self.Game.makeMove(move)
    
    def toggleVictoryPath(self):
        EventManager.notify("ToggleVictoryPath")

    
    def draw(self):
        self.Pattern.draw()
    