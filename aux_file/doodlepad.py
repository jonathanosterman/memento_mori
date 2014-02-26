if self.wallorientation in "NESWNW" #check whether it's an elbow









#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

            else: #elbow wall, remember:[NESW]

                if (self.wallorientation == "NE"):
                    if (self.n_pad and self.e_pad) and gettype(mapfile[(self.line-1)][self.xloc+1]) == "floor":
                        self.ne_floor = mapfile[(self.line-1)][self.xloc+1]

                    else:
                        self.ne_floor = edgesymb

                    self.es_floor = neighfloor[2]
                    self.nw_floor = neighfloor[3]
                    self.sw_floor = neighfloor[3] #TODO not sure if this is the prettiest way

                if (self.wallorientation == "NW"):
                    if (self.n_pad and self.w_pad) and gettype(mapfile[(self.line-1)][self.xloc-1]) == "floor":
                        self.nw_floor = mapfile[(self.line-1)][self.xloc-1]

                    else:
                        self.nw_floor = edgesymb

                    self.es_floor = neighfloor[1]
                    self.ne_floor = neighfloor[2]
                    self.sw_floor = neighfloor[2] #TODO not sure if this is the prettiest way

                if (self.wallorientation == "ES"):
                    if (self.s_pad and self.e_pad) and gettype(mapfile[(self.line+1)][self.xloc+1]) == "floor":
                        self.es_floor = mapfile[(self.line+1)][self.xloc+1]

                    else:
                        self.es_floor = edgesymb

                    self.ne_floor = neighfloor[0]
                    self.nw_floor = neighfloor[3]
                    self.sw_floor = neighfloor[3] #TODO not sure if this is the prettiest way

                if (self.wallorientation == "SW"):
                    if (self.s_pad and self.w_pad) and gettype(mapfile[(self.line+1)][self.xloc-1]) == "floor":
                        self.sw_floor = mapfile[(self.line+1)][self.xloc-1]

                    else:
                        self.sw_floor = edgesymb

                    self.ne_floor = neighfloor[1]
                    self.nw_floor = neighfloor[0]
                    self.es_floor = neighfloor[1] #TODO not sure if this is the prettiest way
                    
        if len(self.wallorientation) == 3: #T-walls

            bum = True
