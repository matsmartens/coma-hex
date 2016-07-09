from tkinter import *

from MenuView import MenuView
from GameView import GameView
from EventManager import EventManager

class HexGUI:
    
    def __init__(self, m, n, Game):
        self.size = [m,n]
        self.Game = Game
        
        self.screenSize = [800, 600]
        
        EventManager.subscribe("MoveFinished", self.onMoveFinished)
        
        # init Tkinter
        self.tkInstance = Tk()
        self.tkInstance.title("HexGame by Daniel, Jannis and Mats")
        self.tkInstance.after(1000, self.onUITick)
        
        self._GUIMenu = MenuView(self.tkInstance, self)
        self._GUIGameBoard = GameView(self.tkInstance, self, Game)
        
        
        self._GUIMenu.show()
        
    # called on every GUI Clock tick
    def onUITick(self):
        
        if not self.Game._pause:
            # notify subscripts
            EventManager.notify("UITick")
        
        
        # redo this step every nth seconds
        self.tkInstance.after(200, self.onUITick)
    
    def mainloop(self):
        mainloop()
    
    def receiveMove(self, move):
        # do somehting
        return 0
    
    def setFirst(self):
        # todo
        return 0
    
    def won(self, winner):
        #self._GUIMenu.won(winner)
        self._GUIGameBoard.won(winner)
    
    def onMoveFinished(self):
        
        # show the Swap Button
        if self.Game.moveCounter == 1:
            self.Game.HexGUI._GUIGameBoard.showPlayerSwap()
        
        # and hide if second hexagon is marked
        if self.Game.moveCounter == 2:
            self.Game.HexGUI._GUIGameBoard.hidePlayerSwap()
        
        self.draw()
    
    def draw(self):
        self._GUIMenu.draw()
        self._GUIGameBoard.draw()
    
    def openPage(self, page):
        
        if page == "menu":
            self._GUIMenu.show()
            self._GUIGameBoard.hide()
        elif page == "game":
            self._GUIMenu.hide()
            self._GUIGameBoard.show()
            EventManager.notify("GameUILoaded")
    
    
