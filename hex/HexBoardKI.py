from HexModel import *
from EventManager import EventManager

class HexBoardKI(HexModel):
    
    def setPlayer(self, player):
        self._player = player
    
    def getPlayer(self):
        return self._player
    
    def getEnemy(self):
        if self.getPlayer() == 1:
            return 2
        else:
            return 1
    
    def receiveMoveByPlayer(self, move, player):
        if player == "player":
            self._myTurn = True
        else:
            self._myTurn = False
        
        self.receiveMove(move)
    
    # game finished event
    def onGameFinished(self):
        #EventManager.notify("KIGameFinished")
        self._finished = True
    