from collections import Counter

class LS_square: #handles all info about a map location
    #ch locations are recorded in chfile, not anywhere in the mapfile

    def __init__(self, mapfile, ylength, x, y, z, edgesymb):
        self.xloc = x
        self.yloc = y
        self.zloc = z
        self.contained_ch = None
        self.neighsymb = []

        self.line = self.zloc*ylength + self.yloc

        self.symb = mapfile[self.line][self.xloc]

        self.type = gettype(self.symb)

        self.set_pathblocker()

        self.n_pad = (self.yloc != 0)
        self.e_pad = (self.xloc < (len(mapfile[0])-2))
        self.s_pad = (self.yloc < ylength-1)
        self.w_pad = (self.xloc != 0)
        
        #neighsymb = [N,E,S,W]
        if (self.n_pad): #N
            self.neighsymb.append(mapfile[(self.line-1)][self.xloc])
        else:
            self.neighsymb.append(edgesymb)

        if (self.e_pad): #E
            self.neighsymb.append(mapfile[self.line][(self.xloc+1)])
        else:
            self.neighsymb.append(edgesymb)

        if (self.s_pad): #S
            self.neighsymb.append(mapfile[(self.line+1)][self.xloc])
        else:
            self.neighsymb.append(edgesymb)

        if (self.w_pad): #W
            self.neighsymb.append(mapfile[self.line][(self.xloc-1)])
        else:
            self.neighsymb.append(edgesymb)

        if self.type == "wall":
            self.wallinit(self.symb, self.neighsymb, mapfile, edgesymb)

    def set_pathblocker(self):

        pathblockers = "BX"
        
        if self.symb in pathblockers:
            self.pathblocker = True

        else:
            self.pathblocker = False

    def setwallfloor(self, direction, symb):
        if direction == "NW" or direction == "WN":
            self.nw_floor = symb

        elif direction == "NE" or direction == "EN":
            self.ne_floor = symb

        elif direction == "ES" or direction == "SE":
            self.es_floor = symb

        elif direction == "SW" or direction == "WS":
            self.sw_floor = symb

        elif direction == "N":
            self.ne_floor = symb
            self.nw_floor = symb

        elif direction == "E":
            self.ne_floor = symb
            self.es_floor = symb

        elif direction == "S":
            self.es_floor = symb
            self.sw_floor = symb

        elif direction == "W":
            self.sw_floor = symb
            self.nw_floor = symb

        else:
            print("~~~~~~~~~~SETWALLFLOOR ERROR~~~~~~~~~~")

    def wallinit(self, symb, neighsymb, mapfile, edgesymb):
        self.wallorientation = ""

        neighwallval = ["N", "E", "S", "W"]
        addend_arr = [[0, -1],[1, 0],[0, 1],[-1, 0]] #[xaddend,yaddend]

        for j in range(4):
            if gettype(neighsymb[j]) == "wall":
                self.wallorientation = self.wallorientation + neighwallval[j]

        #print(self.wallorientation)

        neighfloor = neighsymb #this bit assigns four cosmetic floor sub-tiles

        for j in neighfloor: #check whether neighbors are floor
            if gettype(j) != "floor":
                neighfloor[neighfloor.index(j)] = edgesymb

        if len(self.wallorientation) == 0: #pillar wall

            neighcounter = Counter(neighfloor)
            allfloor = neighcounter.most_common(1)

            for i in ["NW", "NE", "ES", "SW"]:
                self.setwallfloor(i, allfloor)

        self.realwallorientation = self.wallorientation #just in case we need to keep track of terminal walls

        if len(self.wallorientation) == 1: #turn terminal walls into ns or ew walls

            if (self.wallorientation == "N") or (self.wallorientation == "S"):
                self.wallorientation = "NS"
            else:
                self.wallorientation = "EW"

        if len(self.wallorientation) == 2: #straight walls and elbow walls

            if (self.wallorientation == "NS"): #ns wall

                self.nw_floor = neighfloor[3]
                self.sw_floor = neighfloor[3]

                self.ne_floor = neighfloor[1]
                self.es_floor = neighfloor[1]        

            if (self.wallorientation == "EW"): #ew wall

                self.nw_floor = neighfloor[0]
                self.ne_floor = neighfloor[0]

                self.sw_floor = neighfloor[2]
                self.es_floor = neighfloor[2]

            if self.wallorientation in "NESWNW": #elbows only

                if "N" in self.wallorientation:
                    yaddend = -1
                else:
                    yaddend = 1

                if "W" in self.wallorientation:
                    xaddend = -1
                else:
                    xaddend = 1
                    
                #set floor in elbow
                    
                inelbow = mapfile[(self.line+yaddend)][(self.xloc+xaddend)]

                if gettype(inelbow) == "floor": #if stuff in elbow is floor, set in-elbow floor to that
                    self.setwallfloor(self.wallorientation, inelbow)

                else:
                    self.setwallfloor(self.wallorientation, edgesymb)

                #set floor outside elbow

                for j in neighwallval:
                    if not(j in self.wallorientation): #[xaddend, yaddend]
                        
                        add_ind = neighwallval.index(j)
                        
                        xaddend = addend_arr[add_ind][0]
                        yaddend = addend_arr[add_ind][1]

                        if pad(self, j) and (gettype(mapfile[(self.line+yaddend)][(self.xloc+xaddend)]) == "floor"):

                            self.setwallfloor(j, mapfile[(self.line+yaddend)][(self.xloc+xaddend)])

                        else:

                            self.setwallfloor(j, edgesymb)

        if len(self.wallorientation) == 3: #t-walls

            pair0 = self.wallorientation[0] + self.wallorientation[1]
            pair1 = self.wallorientation[0] + self.wallorientation[2]
            pair2 = self.wallorientation[1] + self.wallorientation[2]

            pairlist = [pair0, pair1, pair2]

            for m in pairlist: #set bits in elbow
                if m in "NESWNW": #check if elbow
                    
                    if "N" in m:
                        yaddend = -1
                    else:
                        yaddend = 1

                    if "W" in m:
                        xaddend = -1
                    else:
                        xaddend = 1

                    inelbow = mapfile[(self.line+yaddend)][(self.xloc+xaddend)]

                    if gettype(inelbow) == "floor": #if stuff in elbow is floor, set in-elbow floor to that
                        self.setwallfloor(m, inelbow)

                    else:
                        self.setwallfloor(m, edgesymb)

                    inelbow = mapfile[(self.line+yaddend)][(self.xloc+xaddend)]

            for j in neighwallval: #set the bits not in elbows
                if not(j in self.wallorientation):

                    add_ind = neighwallval.index(j)

                    xaddend = addend_arr[add_ind][0]
                    yaddend = addend_arr[add_ind][1]

                    
                    if pad(self, j) and (gettype(mapfile[(self.line+yaddend)][(self.xloc+xaddend)]) == "floor"):

                        self.setwallfloor(j, mapfile[(self.line+yaddend)][(self.xloc+xaddend)])

                    else:

                        self.setwallfloor(j, edgesymb)

        if len(self.wallorientation) == 4: #x-walls

            elbows = ["NE","ES","SW","NW"]
            elbow_addends = [[1,-1],[1,1],[-1,1],[-1,-1]] #[xaddend,yaddend]
            
            for m in range(4):

                xaddend = elbow_addends[m][0]
                yaddend = elbow_addends[m][1]

                elbow = elbows[m]

                if pad(self, elbow) and (gettype(mapfile[(self.line+yaddend)][(self.xloc+xaddend)]) == "floor"):

                    self.setwallfloor(elbow, mapfile[(self.line+yaddend)][(self.xloc+xaddend)])

                else:

                    self.setwallfloor(elbow, edgesymb)

#END of Ssquare CLASS

def pad(self, direction):
    if direction == "N":
        return self.n_pad
    
    if direction == "E":
        return self.e_pad
    
    if direction == "S":
        return self.s_pad
    
    if direction == "W":
        return self.w_pad

def gettype(symb):
    wall_list = ["S", "B"]
    floor_list = ["_", "f"]

    if symb in wall_list:
        return "wall"
    if symb in floor_list:
        return "floor"
