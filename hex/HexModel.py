from Hexagon import *
#Hex Board enthält die Game Logik und speichert die States

class HexModel:
    
    def __init__(self, m, n):
        
        self.size = [m, n]
        
        # keep track, increment on each added vertex
        self._groupCounter = 2
        
        # player
        self._player = 1
        
        # bool to determine machine state
        self._finished = False
        
        # dictionary for all vertices
        self.Vertices = {}
        
        for i in range(m):
            for j in range(n):
                # add Hexagon instance to the dict
                # with key => i;j
                self.Vertices[str(i) + "," + str(j)] = Hexagon(i, j)
    
    # vertex is clicked
    def isMarked(self, i, j):
        
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
            player = self.getPlayer()
        elif mode == "enemy":
            if self.getPlayer() == 1:
                player = 2
            else:
                player = 1
        else:
            player = None
        
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
        
        # FIXME return victory path
        return self.getVertices("unmarked")
    
    
    # in case of a won game
    # return last player
    def winner(self):
        
        return self.getPlayer()
    
    # get all surrounding vertices
    # that are marked by the same player
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
                        if vertex.player == self.getPlayer():
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
        vertex.player = self.getPlayer()
        
        # first add it to a new group (later on merge them)
        vertex.group = self._groupCounter
        
        # increment the group counter to avoid conflicts
        self._groupCounter = self._groupCounter +1
        
        # the following lines manipulate the groups of
        # vertices at the border of the gameboard
        # red: left 0, right -1
        # blue: top 0, right -1
        
        if self.getPlayer() == 2:
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
            if (-1 in groups and 0 in groups):
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
    
    # game finished event
    def onGameFinished(self):
        self._finished = True
    