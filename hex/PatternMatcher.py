from Pattern import *

import random
from random import shuffle

class PatternMatcher:
    
    # -------------------------------------------------------------------------------------------
    # ---------------------------- General Interface --------------------------------------------
    # -------------------------------------------------------------------------------------------
    
    def __init__(self, model, ki):
        
        self.Model = model
        self.KI = ki
        
        self.FirstMove = [-1,-1]
        
        self.Patterns = {}
        
        # 2 Bridge oben links
        self.addPattern("E0,0E,00,x0;0-0,6-3,20-0")
        
        # 2 Bridge oben blocken
        self.addPattern("00E,000,0E0,000,x00;0-0")
        
        # 2 Bridge oben rechts blocken
        self.addPattern("000E,0E00,0000,x000;0-0")
        
        # 2 Bridge nach unten blocken
        self.addPattern("?0E0,0000,0x00;0-0")
        
        # eigene Steine zur Seite bringen // unten links
        self.addPattern("?0P,x0?;0-1")
        self.addPattern("?0x,P0?;0-1")
        self.addPattern("P0,0x;0-1")
        
        #JannisBrückenbauenamanfang
        self.addPattern("x00,0P0,00P;0-1")
        self.addPattern("P00,0P0,00x;0-1")
        self.addPattern("??00x,00P0?,P00??;0-1")
        self.addPattern("??00P,?0P00,x00??;0-1")
            
        self.addPattern("-x;0-9999")
        
        #JannisBrückenverhindern
        self.addPattern("00x0,??00,?0E0,?00?,0E0?;0-2")
        self.addPattern("0E,xP;0-3")
        self.addPattern("xP,E0;0-3")
        
        #JannisBrückenbauenspeziale
        self.addPattern("P,x,P;0-2")
        
        # Brücken schließen
        #self.addPattern("0P,P0;x---;0;0;00000;0")
        self.addPattern("0xP,P00;0-2.5")#<--- WERT GEÄNDERT
        self.addPattern("P0,xP;0-2.5")#<--- WERT GEÄNDERT
        #brücken schließen,wenn der gegner den anderen stein, der die brücke schließt gelegt hat.
        self.addPattern("Px,EP;0-3")
        self.addPattern("PE,xP;0-3")
        self.addPattern("?P,Ex,P?;0-0")
        self.addPattern("?P,xE,P?;0-0")
        self.addPattern("?xP,PE?;0-3")
        self.addPattern("?EP,Px?;0-3")
        
        # 1- Brücke verhindern
        self.addPattern("?E?,Px?,E??;0-0")
        
        # Gegner blockieren, selber brücke bauen
        self.addPattern("00P,E00,x00;0-0")
        
        # 2 bridge connecten
        self.addPattern("P0?,0x0,?0P;0-0")
        
        self.Vertices = dict(self.Model.Vertices)
        
    
    def getMove(self):
        
        # save game state
        self.GameState = self.mapGameState()

        # check for pattern occurence
        patterns = self.checkPatterns()
        
        if len(patterns) > 0:
            
            patternToSelect = self.getBestPattern(patterns)
            #patternToSelect = random.choice(patterns)
            
            i_shift = int(patternToSelect[1][0])
            j_shift = int(patternToSelect[1][1])
            i = int(patternToSelect[1][2])
            j = int(patternToSelect[1][3])
            
            #if i_shift + i >= self.KI.Size.m or j_shift + j >= self.KI.Size.n:
            #print("Pattern Used:", patternToSelect[1][4], "@", i_shift, j_shift, "with", i, j)
            
            return [i_shift + i, j_shift + j]
        
        else:
            return False
    
    # -------------------------------------------------------------------------------------------
    # ---------------------------- Internal Functions -------------------------------------------
    # -------------------------------------------------------------------------------------------
    
    
    def addPattern(self, text):
        
        modes = text.split(";")
        
        if self.KI.getPlayerIdentity() == 1:
            reverse = False
        else:
            reverse = True
        
        self.Patterns[modes[0]] = Pattern(reverse, modes[0], modes[1])
    
    def mapGameState(self):
        
        gameState = ""
        
        for i in range(self.Model.size[0]):
            for j in range(self.Model.size[1]):
                
                vertex = self.Model.getVertex(i,j)
                
                player = vertex.player
                if vertex.player == None:
                    player = 0
                    
                gameState += str(player)
        
        return gameState
    
    # get Pattern by dynamic weight
    def getBestPattern(self, patterns):
        
        Q = []
        
        # for each pattern
        for pattern in patterns:
            
            # check the weight definitions
            if len(pattern[0]) > 1:
                
                added = False
                # if multiple weights defined
                for weight in pattern[0]:
                    
                    # check which one is applicable according to counter
                    if weight[0] >= self.KI._moveCounter:
                        Q.append([weight[1], pattern[1:]])
                
                # if nothing is found, just add the first one
                if not added:
                    Q.append([pattern[0][0][1], pattern[1:]])
                    
            else:
                Q.append([pattern[0][0][1], pattern[1:]])
                
        # get now the dynamic maximum
        return max(Q, key=lambda x:x[0])
    
    def checkPatterns(self):
        
        PatternsFound = []
        
        player = self.KI.currentPlayer()
        
        if player == 2:
            enemy = 1
        else:
            enemy = 2
        
        #print("enemy is", enemy)
        translator = {"x": 0, "0": 0, "E": enemy, "e": enemy, "P": player, "p": player}
        
        for key, pattern in self.Patterns.items():
            
            # calc min shift top
            y0 = -pattern.topMargin
            yn = self.Model.size[0] - pattern.m + 1 + pattern.topMargin + pattern.bottomMargin
                
            x0 = -pattern.leftMargin
            xn = self.Model.size[1] - pattern.n + 1 + pattern.leftMargin + pattern.rightMargin
                
            for i_shift in range(y0, yn):

                for j_shift in range(x0, xn):
                    
                    matching = True
                    
                    for i in range(pattern.m):
                        for j in range(pattern.n):
                                                        
                            
                            patternIndex = i * pattern.n + j
                            globalIndex = (i_shift + i) * self.Model.size[0] + j_shift + j
                            #print(globalIndex)
                            
                            #print(pattern.pattern, patternIndex, i, j, pattern.n)
                            
                            patternVal = pattern.pattern[patternIndex]
                            
                            if patternVal != "?":
                                
                                # border detection
                                if patternVal == "-":
                                    if (i_shift + i > self.KI.Size.m or i_shift + i < 0 or j_shift + j > self.KI.Size.n or j_shift + j < 0):
                                        pass
                                    else:
                                        matching = False
                                        break
                                    
                                elif len(self.GameState) > globalIndex and globalIndex >= 0:
                                                                        
                                    patternComp = str(translator[patternVal])
                                    gameComp = str(self.GameState[globalIndex])
                                    
                                    
                                    
                                    #print(patternComp, gameComp)
                                    
                                    if patternVal == "e" and (gameComp == "0" or gameComp == patternComp):
                                        print("alternative enemy")
                                        
                                    elif patternVal == "p" and (gameComp == "0" or gameComp == patternComp):
                                        print("alternative player")
                                                                        
                                    elif patternComp != gameComp:
                                        matching = False
                                        break
                                else:
                                    matching = False
                                    break
                                
                        
                    if matching == True and not self.Model.isMarked(i_shift + pattern.i, j_shift + pattern.j):
                        
                        #if i_shift + pattern.i < 
                        PatternsFound.append([pattern.weight, i_shift, j_shift, pattern.i, pattern.j, pattern.pattern])
        
        return PatternsFound
    