import Size
from Hexagon import *
import copy

class DijkstraBase:
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.visited = False
        self.weight = float("inf")
        self.predecessor = None
        
class ConnectedComponent(DijkstraBase):
    
    def __init__(self, vertices = []):
        
        super().__init__()
        
        if len(vertices) > 0:
            self.group = vertices[0].group
            self.Vertices = vertices
        else:
            self.group = None
            self.Vertices = []
        self.distances = []
    
    def add(self, vertex):
        if self.group == None:
            self.group = vertex.groupd
        self.Vertices.append(vertex)
    
    def addDistance(self, conComp, len):
        self.distances.append([conComp, len])
    
    def setDistance(self, conComp, len):
        for i, comp in enumerate(self.distances):
            if comp[0].group == conComp.group:
                self.distances[i][1] = len
                
    def getDistance(self, conComp):
        for dists in self.distances:
            if dists[0].group == conComp.group:
                return dists[1]
    
class ConnectedComponents:
    
    def __init__(self, components = []):
        if len(components) > 0:
            self.components = components
        else:
            self.components = []
        
    def add(self, component):
        self.components.append(component)
    
    def getAll(self):
        return self.components
    
    def getComponentByGroup(self, group):
        for comp in self.components:
            if comp.group == group:
                return comp
        return None
    
    def insert(self, vertex):
        comp = self.getComponentByGroup(vertex.group)
        if comp != None:
            comp.add(vertex)
        else:
            self.components.append(ConnectedComponent([vertex]))

class Vertex(DijkstraBase):
    
    def __init__(self, i, j, group):
        
        super().__init__()
        
        self.i = i
        self.j = j
        self.group = group

class SearchGraph:
    
    def __init__(self, ki):
        self.KI = ki
        self.Vertices = []
        for i in range(self.KI.Size.m):
            Row = []
            for j in range(self.KI.Size.n):
                vertex = self.KI.HexBoard.getVertex(i, j)
                
                group = vertex.group
                if self.KI.getPlayerIdentity() == 2:
                    if i == 0:
                        group = -11
                    elif i == self.KI.Size.m-1:
                        group = -12
                else:
                    if j == 0:
                        group = -11
                    elif j == self.KI.Size.n-1:
                        group = -12
                
                Row.append(Vertex(vertex.i, vertex.j, group))
                
            self.Vertices.append(Row)
        #print("I am Player:",self.KI.getPlayerIdentity())
    
    def getMinWeightVertex(self):
        Q = []
        for row in self.Vertices:
            for vtx in row:
                if not vtx.visited:
                    Q.append(vtx)
        
        if len(Q) > 0:
            return min(Q, key=lambda x:x.weight)
        else:
            return False
    
    def getVertex(self,i,j):
        return self.Vertices[i][j]
    
    def isValidCoordinate(self, i, j):
        if i >= 0 and j >= 0 and i < self.KI.Size.m and j < self.KI.Size.n:
            return True
        else:
            return False
    
    def getSurroundingVertices(self,i,j,unvisited=True):
        
        indices = [[-1,0],[-1,1],[0,-1],[0,1],[1, -1],[1,0]]
        Vtcs = []
        
        for index in indices:
            v, w = i+index[0], j+index[1]
            if self.isValidCoordinate(v,w):
                vtx = self.getVertex(v, w)
                ownedBy = self.KI.HexBoard.getVertex(v,w).player
                if vtx.visited == False and ownedBy in [None, self.KI.getPlayerIdentity()]:
                    Vtcs.append(vtx)

        return Vtcs
        
    def reset(self):
        for row in self.Vertices:
            for vertex in row:
                vertex.visited = False
                vertex.weight = float("inf")
    
    def getMinimum(self, vertex, group):
                
        self.reset()
        
        startVertex = self.getVertex(vertex.i, vertex.j)
        startVertex.visited = True
        startVertex.weight = 0
        
        visitCounter = 1
        
        vtx = startVertex
        while visitCounter != len(self.Vertices) * len(self.Vertices[0]):
            
            neighbours = self.getSurroundingVertices(vtx.i, vtx.j)
            for neighbour in neighbours:
                if neighbour.group == vtx.group and vtx.group != None:
                    if vtx.weight < neighbour.weight:
                        neighbour.weight = vtx.weight
                        neighbour.predecessor = vtx
                else:
                    if vtx.weight + 1 < neighbour.weight:
                        neighbour.weight = vtx.weight + 1
                        neighbour.predecessor = vtx
            
            vtx = self.getMinWeightVertex()
            
            if vtx == False:
                break#return float("inf")
            
            vtx.visited = True
        
        Q = []
        for row in self.Vertices:
            for vtx in row:
                
                if vtx.group == group:
                    Q.append(vtx)
        vtxMin = min(Q, key=lambda x:x.weight)
        vtxMin.route = self.getPredecessors(vtxMin)
        return vtxMin
        
    def getPredecessors(self, vtx):
        Q = []
        for q in range(self.KI.Size.m * self.KI.Size.n):
            if vtx.predecessor != None:
                Q.append(copy.copy(vtx))
                vtx = vtx.predecessor
            else:
                return Q

class GraphSearch:
    
    def __init__(self, ki):
        
        self.KI = ki
        
    
    def getConnectingMoves(self):
                
        # suche alle zusammenhangskomponenten
        self.connectedComps = self.getConnectedComponents()
                
        # get a search object
        Search = SearchGraph(self.KI)
        
        dists = []
        if self.KI.getPlayerIdentity() == 1:
            for i in range(self.KI.Size.m):
                dists.append(copy.copy(Search.getMinimum(self.KI.HexBoard.getVertex(i, 0), -12)))
                Search.reset()
        else:
            for j in range(self.KI.Size.n):
                dists.append(copy.copy(Search.getMinimum(self.KI.HexBoard.getVertex(0, j), -12)))
                Search.reset()

        x = min(dists, key=lambda x:x.weight)
        
        Q = []
        for vtx in x.route:
            if not self.KI.HexBoard.isMarked(vtx.i, vtx.j):
                Q.append([vtx.i, vtx.j])
                
        return Q
    
        
        
        # gib die menge abzüglich der concom aus
    def getMinCombinations(self):
        
        # drehe alle gewichte der borders um
        border0 = self.connectedComps.getComponentByGroup(-11)
        border1 = self.connectedComps.getComponentByGroup(-12)
        for comp in self.connectedComps.getAll():
            
            if comp.weight > 0:
                border0.setDistance(comp, comp.getDistance(border0))
                border1.setDistance(comp, comp.getDistance(border1)) 
        
        
        visitCounter = 1
        
        startComp = self.connectedComps.getComponentByGroup(-11)
        startComp.visited = True
        startComp.weight = 0
        
        curComp = startComp
        while visitCounter < len(self.connectedComps.getAll()):
            
            # surroundings and set all weights
            _comps = self.connectedComps.getAll()
            comps = []
            for comp in _comps:
                if not comp.visited:
                    if comp.weight > curComp.weight and (curComp.group > 0 or comp.group > 0):
                        comp.weight = curComp.weight + curComp.getDistance(comp)
                    comps.append(comp)
            
            
            # check exit
            if comp.group == -12:
                return comp.weight
            
            
            # get minimum
            if len(comps) > 0:
                curComp = min(comps, key=lambda x:x.weight)
            else:
                return
            
            visitCounter += 1
    
    
    
    # get connected components owned by the player
    def getConnectedComponents(self):
        
        connectedComps = ConnectedComponents()
        for i in range(self.KI.Size.m):
            for j in range(self.KI.Size.n):
                vertex = self.KI.HexBoard.getVertex(i, j)
                if vertex.player == self.KI.getPlayerIdentity():
                    connectedComps.insert(vertex)
        
        # register virtual border group       
        border0 = ConnectedComponent([Hexagon(-1,-1)])
        border0.group = -11
        
        border1 = ConnectedComponent([Hexagon(-2,-2)])
        border1.group = -12
        
        connectedComps.add(border0)
        connectedComps.add(border1)         
                
        return connectedComps      
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                