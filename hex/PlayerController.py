from random import *

class PlayerController:
    
    def __init__(self):
        
        self._currentPlayer = 1
        self._currentPlayerType = "human"
        
        self._playerIdentity = 0
        
        self.mode = "human"
    
    
    # generate random player number
    def chooseFirst(self):
        self._currentPlayer = round(random.random()) + 1
    
    def setPlayerIdentity(self, player):
        self._playerIdentity = player
    
    def getPlayerIdentity(self):
        return self._playerIdentity
    
    def setCurrentPlayer(self, player):
        self._currentPlayer = player
    
    # is the getter for the private variable
    def currentPlayer(self):
        return self._currentPlayer
    
    def currentEnemy(self):
        if self._currentPlayer == 1:
            return 2
        else:
            return 1
    
    # is the current Player human?
    def isPlayerHuman(self):
        return self._currentPlayerType == "human"
    
    # alter the players
    def changePlayer(self):
        
        if self._currentPlayer == 1:
            self._currentPlayer = 2
            
        else:
            self._currentPlayer = 1
            
        if self.mode == "ki":
            
            if self._currentPlayerType == "human":
                self._currentPlayerType = "ki"
            else:
                self._currentPlayerType = "human"
        
        if self.mode in ["inter", "machine"]:
            
            self._currentPlayerType = "ki"
                