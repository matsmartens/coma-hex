from EventManager import EventManager
from Hexagon import *

class HexBoard:
    
    def __init__(self, m, n):
        
        self.size = [m, n]
        
        # keep track, increment on each added vertex
        self._groupCounter = 2
        
        # bool to determine machine state
        self._finished = False
        
        # want to suppress the EventManager notifications?
        self._eventsSuppressed = False
        
        # dictionary for all vertices
        self.Vertices = {}
        
        for i in range(m):
            for j in range(n):
                # add Hexagon instance to the dict
                # with key => i;j
                self.Vertices[str(i) + "," + str(j)] = Hexagon(i, j)
    
    # set game reference
    def setReferenceToGame(self, game):
        self.Game = game
    
    # suppress Event Manager Notifications
    def suppressEvents(self):
        self._eventsSuppressed = True
    
    # unsuppress Event Manager notifications
    def unsuppressEvents(self):
        self._eventsSuppressed = False
    
    # determine whether Vertex is marked or not
    def isMarked(self, i, j):
        
        # if requested field is out of bounds
        if i >= self.size[0] or i < 0 or j >= self.size[1] or j < 0:
            return False
        
        else:
            
            # retrieve player details of vertex
            state = self.getVertex(i, j).player
            
            if state == None:
                return False
            else:
                return True
    
    # get Vertex at certain index
    def getVertex(self, i, j):
        return self.Vertices[str(i) + "," + str(j)]
    
    # get Vertices
    def getVertices(self, mode = "none"):
        
        vertices = []
        
        if mode == "player":
            player = self.Game.currentPlayer()
        elif mode == "enemy":
            player = self.Game.currentEnemy()
        else:
            player = None
        
        # get all vertices where player atrribute is matching
        for i, vertex in self.Vertices.items():
            
            if vertex.player == player:
                vertices.append(vertex)
        
        return vertices
    
    # return machine state
    def finished(self):
        return self._finished
    
    # get List of Vertices that belong to
    # victory path
    def getVictoryPath(self):
        if self.Game.currentPlayer() == 1:
            z1 = self.size[0]//2
            z2 = 0
            counter = 1
            while self.getVertex(z1,z2).player != self.Game.currentPlayer() and self.getVertex(z1,z2).player != None:
                if counter%2 == 1:
                    z1 += counter
                    counter += 1
                else:
                    z1 -= counter
                    counter += 1
            self.getVertex(z1,z2).victorypath = self.Game.currentPlayer()
            self.victory(z1,z2)
            ausgabeliste = []
            for i,vertex in self.Vertices.items():
                if vertex.victorypath == self.Game.currentPlayer():
                    ausgabeliste.append(vertex)
        else:
            z1 = 0
            z2 = self.size[1]//2
            counter = 1
            while self.getVertex(z1,z2).player != self.Game.currentPlayer() and self.getVertex(z1,z2).player != None:
                if counter%2 == 1:
                    z2 += counter
                    counter += 1
                else:
                    z2 -= counter
                    counter += 1
            self.getVertex(z1,z2).victorypath = self.Game.currentPlayer()
            self.victory(z1,z2)
            ausgabeliste = []
            for i,vertex in self.Vertices.items():
                if vertex.victorypath == self.Game.currentPlayer():
                    ausgabeliste.append(vertex)
        for i,vertex in self.Vertices.items():
            if vertex.victorypath != 0:
                vertex.victorypath = 0
        return ausgabeliste
			
			
    #hilfsfunktion für getvictorypath
    def victory(self, i, j):
        if self.Game.currentPlayer() == 1:
            if j == self.size[1]-1:
                return
            else:
                if self.getVertex(i,j+1).player == self.Game.currentPlayer() or self.getVertex(i,j+1).player == None and self.getVertex(i,j+1).victorypath != -1 and self.getVertex(i,j+1).victorypath != self.Game.currentPlayer():
                    self.getVertex(i,j+1).victorypath = self.Game.currentPlayer()
                    self.victory(i,j+1)
                elif self.getVertex(i-1,j+1).player == self.Game.currentPlayer() or self.getVertex(i-1,j+1).player == None and self.getVertex(i-1,j+1).victorypath != -1 and self.getVertex(i-1,j+1).victorypath != self.Game.currentPlayer():
                    self.getVertex(i-1,j+1).victorypath = self.Game.currentPlayer()
                    self.victory(i-1,j+1)
                elif (self.getVertex(i+1,j).player == self.Game.currentPlayer() or self.getVertex(i+1,j).player == None) and self.getVertex(i+1,j).victorypath != -1 and self.getVertex(i+1,j).victorypath != self.Game.currentPlayer():
                    self.getVertex(i+1,j).victorypath = self.Game.currentPlayer()
                    self.victory(i+1,j)
                elif (self.getVertex(i-1,j).player == self.Game.currentPlayer() or self.getVertex(i+1,j).player == None) and self.getVertex(i-1,j).victorypath != -1 and self.getVertex(i-1,j).victorypath != self.Game.currentPlayer():
                    self.getVertex(i-1,j).victorypath = self.Game.currentPlayer()
                    self.victory(i-1,j)
                elif (self.getVertex(i-1,j-1).player == self.Game.currentPlayer() or self.getVertex(i-1,j-1).player == None) and self.getVertex(i-1,j-1).victorypath != -1 and self.getVertex(i-1,j-1).victorypath != self.Game.currentPlayer():
                    self.getVertex(i-1,j-1).victorypath = self.Game.currentPlayer()
                    self.victory(i-1,j-1)
                elif (self.getVertex(i,j-1).player == self.Game.currentPlayer() or self.getVertex(i,j-1).player == None) and self.getVertex(i,j-1).victorypath != -1:
                    self.getVertex(i,j).victorypath = -1
                    self.victory(i,j-1)
                #else:
                #    self.getVertex(i,j).victorypath = -1
                #    self.victory(i,j)
        else:
            if i == self.size[0]-1:
                return
            else:
                if self.getVertex(i+1,j).player == self.Game.currentPlayer() or self.getVertex(i+1,j).player == None and self.getVertex(i+1,j).victorypath != -1 and self.getVertex(i+1,j).victorypath != self.Game.currentPlayer():
                    self.getVertex(i+1,j).victorypath = self.Game.currentPlayer()
                    self.victory(i+1,j)
                elif self.getVertex(i+1,j-1).player == self.Game.currentPlayer() or self.getVertex(i+1,j-1).player == None and self.getVertex(i+1,j-1).victorypath != -1 and self.getVertex(i+1,j-1).victorypath != self.Game.currentPlayer():
                    self.getVertex(i+1,j-1).victorypath = self.Game.currentPlayer()
                    self.victory(i+1,j-1)
                elif (self.getVertex(i,j+1).player == self.Game.currentPlayer() or self.getVertex(i,j+1).player == None) and self.getVertex(i,j+1).victorypath != -1 and self.getVertex(i,j+1).victorypath != self.Game.currentPlayer():
                    self.getVertex(i,j+1).victorypath = self.Game.currentPlayer()
                    self.victory(i,j+1)
                elif (self.getVertex(i,j-1).player == self.Game.currentPlayer() or self.getVertex(i,j-1).player == None) and self.getVertex(i,j-1).victorypath != -1 and self.getVertex(i,j-1).victorypath != self.Game.currentPlayer():
                    self.getVertex(i,j-1).victorypath = self.Game.currentPlayer()
                    self.victory(i,j-1)
                elif (self.getVertex(i-1,j+1).player == self.Game.currentPlayer() or self.getVertex(i-1,j+1).player == None) and self.getVertex(i-1,j+1).victorypath != -1 and self.getVertex(i-1,j+1).victorypath != self.Game.currentPlayer():
                    self.getVertex(i-1,j+1).victorypath = self.Game.currentPlayer()
                    self.victory(i-1,j+1)
                elif (self.getVertex(i-1,j).player == self.Game.currentPlayer() or self.getVertex(i-1,j).player == None) and self.getVertex(i-1,j).victorypath != -1:
                    self.getVertex(i,j).victorypath = -1
                    self.victory(i-1,j)
                #else:
                 #   self.getVertex(i,j).victorypath = -1  
                  #  self.victory(i,j)	          
   
    
    # in case of a won game return last player
    def winner(self):
        return self.Game.currentPlayer()
    
    # get all surrounding vertices that are marked by the same player
    def getSurroundingVertices(self, i, j, player = -1):
        
        # hold an empty list to store the items in
        Q = []
        
        # some math stuff to mathematically get
        # a representation of the surrounding fields
        # to avoid the eye cancer of a bunch of loops
        for v in range(3):
            for w in range(2):
                
                # check this stuff on a piece of paper
                # to hard to describe
                r = v-1
                s = w
                s = (s * (1 - (abs(r) * 0.5)) * 2) - 1
                
                if r == 1:
                    s = s * (-1)
            
                s = s *(-1)
                r = j - int(r)
                s = i - int(s)
                
                if r >= 0 and r < self.size[1] and s  >= 0 and s < self.size[0]:
                    
                    
                    # get the vertex at that position    
                    vertex = self.getVertex(s, r)
                    
                    if player == -1:
                        
                        # if player marked that vertex..
                        if vertex.player == self.Game.currentPlayer():
                            # .. add that vertex to the list
                            Q.append(vertex)
                    elif player == 0:
                        
                        # if player marked that vertex..
                        if vertex.player == None:
                            # .. add that vertex to the list
                            Q.append(vertex)
                    
                    else:
                        # if player marked that vertex..
                        Q.append(vertex)
        
        return Q
    
    
    lastMove = None
    def receiveMove(self, move):
                
        # first store the last move
        self.lastMove = move
        
        # get the vertex the move pointed on
        vertex = self.getVertex(move[0], move[1])
        
        # mark it
        vertex.player = self.Game.currentPlayer()
        
        # first add it to a new group (later on merge them)
        vertex.group = self._groupCounter
        
        # increment the group counter to avoid conflicts
        self._groupCounter = self._groupCounter +1
        
        # the following lines manipulate the groups of
        # vertices at the border of the gameboard
        # red: left 0, right -1
        # blue: top 0, right -1
        
        if self.Game.currentPlayer() == 2:
            if move[0] == 0:
                vertex.group = 0
            if move[0] == self.size[0]-1:
                vertex.group = -1

        else:
            if move[1] == 0:
                vertex.group = 0
            if move[1] == self.size[1]-1:
                vertex.group = -1
            
        # get the adjacent vertices to that one, which is marked
        adjVertices = self.getSurroundingVertices(move[0], move[1])
        
        # any neightbours?:
        if len(adjVertices) > 0:
            
            # put the marked one to the list
            adjVertices.append(vertex)
            
            # only concentrate on the groups
            groups = [x.group for x in adjVertices]
            
            # WIN Condition
            # either within the gameboard
            # or the last vertex marked has been at the borders
            antwort=[]
            if (-1 in groups and 0 in groups):
                for i , vertex in self.Vertices.items():
                    if vertex.group==-1:
                        print(vertex)
                self.onGameFinished()
                
            # get the minimum group
            minGroup = min(groups)
                        
            # set all neighbours to the minimum of the group       
            for key, value in self.Vertices.items():
                if value.group in groups:
                    value.group = minGroup
            
    
    # read board
    def readBoard(self, board, current = True):

        groupCounter = 2
        
        # iterate over rows and cols
        for i, row in enumerate(board):
            
            for j, col in enumerate(row):
                
                groupCounter += 1
                
                # convert to our way of undefined fields
                group = None
                
                if col == 0:
                    col = None
                    
                
                else:
                    if col == 1:
                        
                        if j == 0:
                            group = 0
                        elif j == self.size[1]-1:
                            group = -1
                        else:
                            group = groupCounter
                            
                    
                    else:
                        if i == 0:
                            group = 0
                        elif i == self.size[0]-1:
                            group = -1
                        else:
                            group = groupCounter
                        
                
                # set the vertex' player 
                vertex = self.getVertex(i, j)
                vertex.player = col
                vertex.group = group
            
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                
                v1 = []
                v2 = []
                
                vertices = self.getSurroundingVertices(i, j,40)
                for vertex in vertices:
                    if vertex.player == 1 and vertex.group != None:
                        v1.append(vertex)
                    elif vertex.player == 2 and vertex.group != None:
                        v2.append(vertex)
                
                v1 = [x.group for x in v1]
                v2 = [x.group for x in v2]
                
                if len(v1) > 0:
                    v1min = min(v1)
                
                if len(v2) > 0:
                    v2min = min(v2)
                
                for i2 in range(self.size[0]):
                    for j2 in range(self.size[1]):
                        
                        vertex = self.getVertex(i2, j2)
                        if len(v1) > 0:
                            if vertex.group in v1:
                                vertex.group = v1min
                        
                        if len(v2) > 0:
                            if vertex.group in v2:
                                vertex.group = v2min
                            
                
                
      
    # switch color of all vertices already marked
    def switchColors(self):
        
        # loop for all vertices and invert them
        for key, value in self.Vertices.items():
            
                if value.player == 1:
                    value.player = 2
                elif value.player == 2:
                    value.player = 1
    
    # return last move
    def getLastMove(self):
        return self.lastMove

    # return a height x width snapshot centered at i, j
    def getWinnerSnapshotBinary(self, height = 5, width = 5):
        
        player = self.winner()
        
        
        
        WinningPatterns = []
        
        # look for winning vertices
        for key, vertex in self.Vertices.items():
            if vertex.group == -1 and vertex.i - 3 > 0 and vertex.i + 3 < 11 and vertex.j - 3 > 0 and vertex.j + 3 < 11:
                
                VerticesA = []
                VerticesB = []
                
                for i in range(-floor(height/2), floor(height/2)):
                    
                    VertexRowA = []
                    VertexRowB = []
                    for j in range(-floor(width/2), floor(width/2)):
                        
                        if self.isValidCoordinate(i+vertex.i, j+vertex.j):
                            
                            v = self.getVertex(i+vertex.i, j+vertex.j)
                            if v.player == player:
                                VertexRowA.append(1)
                                VertexRowB.append(0)
                            elif v.player != None and v.player != player:
                                VertexRowA.append(0)
                                VertexRowB.append(1)
                            else:
                                VertexRowA.append(0)
                                VertexRowB.append(1)
                    
                    VerticesA.extend(VertexRowA)
                    VerticesB.extend(VertexRowB)
                
                VerticesA.extend(VerticesB)
                
                mask = 0b0
                
                for element in VerticesA:
                    if element == 1:
                        mask = (mask << 1) + 0b1
                    else:
                        mask = (mask << 1) + 0b0
                
                WinningPatterns.append(mask)
        
        return WinningPatterns
    # game finished event
    def onGameFinished(self):
        if not self._eventsSuppressed:
            EventManager.notify("GameFinished")
        self._finished = True
    