from ls_square import LS_square
from ls_character import LS_character
import os
import math
from random import randrange

class LS_session: #loads up a save's various files, contains game info, talks to gui about display, organizes updates

    def __init__(self, folderloc):

        self.map_arr = []
        self.movetry_arr = []
        self.ch_arr = []
        self.lb_arr = []
        self.folderloc = folderloc
        
        self.fullmapfile = open(os.path.join(folderloc, "region.txt"), "r+").readlines()

        self.chfile = open(os.path.join(folderloc, "ch.txt"), "r+").readlines()

        self.makemap()
        self.initialize_chs()

    def update(self):

        for i in self.ch_arr:
            i.update()

    def add_lowbehavior(self, lowbehavior):
        
        self.lb_arr.append(lowbehavior)
        print("behavior appended")

        assert self.lb_arr[-1] is lowbehavior
        
        if len(self.lb_arr) == len(self.ch_arr):
            self.try_lb_updates()
            print("Trying updates")
            print(self.lb_arr)

    def try_lb_updates(self):

        self.success_dict = {}
        self.already_there = []
        self.movefrom_arr = self.movetry_arr
        self.staying_arr = self.movetry_arr
        print(self.movetry_arr)

        for w in self.lb_arr:
            self.already_there.append(w.character.position) #lists in the same order where the characters already are

        for i in range(len(self.lb_arr)):
            
            if self.lb_arr[i].subtype == "move": #check move commands
                self.movetry_arr[self.lb_arr[i].move_loc[0]][self.lb_arr[i].move_loc[1]][self.lb_arr[i].move_loc[2]].append(i)

        for i in range(len(self.already_there)):

            if self.lb_arr[i].subtype == "move":
                self.movefrom_arr[already_there[i][0]][already_there[i][1]][already_there[i][2]] = i 

            else:
                self.staying_arr[already_there[i][0]][already_there[i][1]][already_there[i][2]] = i

        for i in range(len(self.movetry_arr)):
            for j in range(len(self.movetry_arr[i])):
                for k in range(len(self.movetry_arr[i][j])):

                    if staying_arr[i][j][k] != None: #i.e. someone is staying put here; important that this goes first!

                        for w in self.movetry_arr[i][j][k]: #w is not an index here
                            self.success_dict[w] = "failure" #can't move where someone is standing still

                    if len(self.movetry_arr[i][j][k]) > 1:
                        winner_index = randrange(len(self.movetry_arr[i][j][k]))
                        
                        for p in range(len(self.movetry_arr[i][j][k])):

                            if p == winner_index and self.success_dict[self.movetry_arr[i][j][k][p]] != "failure": #could have failed in the staying check
                                self.success_dict[self.movetry_arr[i][j][k][p]] = "no_move_conflict" #does not totally determine if you can move; need to check dependencies

                            else:
                                self.success_dict[self.movetry_arr[i][j][k][p]] = "failure" #means you will not move

                    if len(self.movetry_arr[i][j][k]) == 1:

                        self.success_dict[self.movetry_arr[i][j][k][0]] = "no_move_conflict"

                    if movefrom_arr[i][j][k] != None: #i.e. someone is standing where you're trying to go, but they want to move too

                        for w in self.movetry_arr[i][j][k]:
                            self.success_dict[w] = movefrom_arr[i][j][k] #can only ever contain one anyway; index indicates a character as per its command index in the lb_arr

        print(self.success_dict)

        self.lb_arr = []
        #NEED TO CLEAN MOVETRY_ARR

    def initialize_chs(self):

        for i in range(len(self.chfile)):
            chindex = i
            ch_info_list = self.chfile[i].split(";")
            character = LS_character(self, chindex, ch_info_list)
            self.ch_arr.append(character)

    def makemap(self):

        ylength = int(self.fullmapfile[0][0]) #the y length of a z-level
        
        self.fullmapfile.pop(0)
        
        edgesymb = self.fullmapfile[0][0]
        self.fullmapfile.pop(0)

        self.mapfile = self.fullmapfile

        #print(self.mapfile)

        #print(len(self.mapfile[0])-2)

        #z[y[x]], or map_arr[z][y][x]
        
        for j in range(len(self.mapfile)):
            for i in range((len(self.mapfile[0])-1)): #len(mapfile[0])-1

                xcoord = i
                ycoord = j % ylength
                zcoord = int(math.floor(j / ylength))

                #print(xcoord)
                #print(ycoord)
                #print(zcoord)

                square = LS_square(self.mapfile, ylength, xcoord, ycoord, zcoord, edgesymb)
                    
                if xcoord == 0: #beginning of an x-line

                    if ycoord == 0: #beginning of a z-level
                        new_zlist = []
                        self.map_arr.append(new_zlist)

                    new_ylist = []
                    self.map_arr[zcoord].append(new_ylist)


                self.map_arr[zcoord][ycoord].append(square)
                
                if xcoord == 0:

                    if ycoord == 0:
                        new_zlist = []
                        self.movetry_arr.append(new_zlist)

                    new_ylist = []
                    self.movetry_arr[zcoord].append(new_ylist)

                self.movetry_arr[zcoord][ycoord].append([])

                    
            
