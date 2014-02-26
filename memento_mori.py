from ls_square import LS_square
from ls_session import LS_session
from tkinter import *
from PIL import *
from PIL import ImageTk
import PIL.Image
import os
import math
import tkinter as tk
import pickle as pickle
#creates a root with widgets and dialoge to start session

class Memento_Mori(Frame):
    
    def __init__(self):
        self.root = tk.Tk()

        self.resolution = [1600, 900]
        self.z_level = 0
        self.view_rot = 0 #adding 1 to rot represents a clockwise rotation
        tk.Frame.__init__(self, self.root)
        
        self.root.configure(background = "black")
        self.root.wm_title("Memento Mori")
        self.make_widgets()

    def start(self):
        self.root.mainloop()

    def openfolder(self):
        folderloc = tk.filedialog.askdirectory()
        self.session = LS_session(folderloc)
        self.fulldrawmap()

    def opensession(self):
        pickleloc = tk.filedialog.askopenfilename()
        self.session = pickle.load(open(pickleloc, "rb"))
        self.fulldrawmap()
        print("LS_session opened from pickle")

    def savesession(self):
        folderloc = tk.filedialog.askdirectory()
        pickleloc = os.path.join(folderloc, "session.p")
        pickle.dump(self.session, open(pickleloc, "wb"))
        print("LS_session saved to pickle")

    def click(self, event):
        self.clickx = event.x
        self.clicky = event.y

    def clickdrag(self, event):
        self.x_canoff = self.x_canoff + int((event.x - self.clickx)/2)
        self.y_canoff = self.y_canoff + int((event.y - self.clicky)/2)
        self.maincan.tk.call(self.maincan._w, 'scan', 'dragto', self.x_canoff, self.y_canoff, 1)
        self.clickx = event.x
        self.clicky = event.y

    def doubleclick(self, event):
        self.view_rot = (self.view_rot+1)%4
        self.fulldrawmap()

    def make_widgets(self):
        
        #menu bar
        menubar = Menu(self.root)
        self.root["menu"] = menubar

        self.x_canoff = 0
        self.y_canoff = 0
        
        filemenu = Menu(menubar)
        optionmenu = Menu(menubar)
        
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Options", menu=optionmenu)

        filemenu.add_command(label="Open from folder", command=self.openfolder)
        filemenu.add_command(label="Open old session", command=self.opensession)
        filemenu.add_command(label="Save current session", command=self.savesession)
        optionmenu.add_command(label="Nothing")

        #main canvas
        self.maincan = tk.Canvas(master=self.root)

        self.maincan.titlecardpil = PIL.Image.open("titlecard.png")
        self.maincan.titlecard = ImageTk.PhotoImage(self.maincan.titlecardpil)
        self.maincan.config(width = self.resolution[0]-5, height = self.resolution[1]-10, background = "black")
        
        title = self.maincan.create_image(0,0,image=self.maincan.titlecard, anchor="nw")

        self.maincan.grid(row="0")
        self.maincan.bind("<Button-1>", self.click)
        self.maincan.bind("<B1-Motion>", self.clickdrag)
        self.maincan.bind("<Double-Button-1>", self.doubleclick)

    def fulldrawmap(self):

        off_width = 114/2
        off_height = 80/2

        e_1 = [off_height, off_width]
        e_2 = [off_height, -off_width] #basis vectors : [y,x]

        map_arr = self.session.map_arr

        x_dim = len(map_arr[0][0])
        y_dim = len(map_arr[0])
        z_dim = len(map_arr)

        self.backdrop = PIL.Image.new("RGB", (int(off_width*(x_dim + y_dim+4)), int(off_height*(x_dim + y_dim+4))), "black")

        l = self.z_level #TODO make it iterate over zs

        self.image_list = []

        direction_permute = ["NS", "EW", "NS", "EW", "NS", "NE", "ES", "SW", "NW", "NE", "ES", "SW", "NES", "ESW", "NSW", "NEW", "NES", "ESW", "NSW", "N", "E", "S", "W", "N", "E", "S"]

        ordering_list = [[range(y_dim), range(x_dim)],[range(y_dim-1,-1,-1), range(x_dim)],[range(y_dim-1,-1,-1), range(x_dim-1,-1,-1)],[range(y_dim), range(x_dim-1,-1,-1)]]

        y_order = ordering_list[self.view_rot][0]
        x_order = ordering_list[self.view_rot][1]

        for i in y_order:
            for j in x_order:
                cur_ssquare = map_arr[l][i][j]

                if self.view_rot == 0:
                    rel_y = i*off_height + j*off_height
                    rel_x = j*off_width - i*off_width + off_width*(y_dim + 1)

                if self.view_rot == 1:
                    rel_y = (y_dim-i)*off_height + j*off_height
                    rel_x = -j*off_width + (y_dim-i)*off_width + off_width*(x_dim + 1)

                if self.view_rot == 2:
                    rel_y = (y_dim-i)*off_height + (x_dim-j)*off_height
                    rel_x = (x_dim-j)*off_width - (y_dim-i)*off_width + off_width*(y_dim + 1)

                if self.view_rot == 3:
                    rel_y = i*off_height + (x_dim-j)*off_height
                    rel_x = -(x_dim-j)*off_width + i*off_width + off_width*(x_dim + 1)
                
                if cur_ssquare.type == "wall":
                    trueorientation = cur_ssquare.wallorientation

                    if trueorientation != "":

                        if trueorientation == "NESW":
                            filename = "NESW.png"

                        else:

                            wall_index = direction_permute.index(trueorientation) + self.view_rot
                            filename = direction_permute[wall_index] + ".png" #reassigns filename according to rotation

                    else:
                        filename = "pillar.png"

                    if cur_ssquare.symb == "B":
                        folder = "default_wall"

                    imgpath = os.path.join(folder, filename)
                    image = PIL.Image.open(imgpath)
                    
                    self.image_list.append(image)
                    
                    self.backdrop.paste(image, (int(rel_x), int(rel_y)), image)#draw onto file

                if cur_ssquare.contained_ch != None:
                    cur_ch = cur_ssquare.contained_ch
                    ch_sprite_folder = cur_ch.sprite_folder

                    direction_index = direction_permute.index(cur_ch.orientation) + self.view_rot
                    base_filename = direction_permute[direction_index]

                    filename = base_filename + cur_ch.visual_state + cur_ch.anim_state + ".png"

                    imgpath = os.path.join(ch_sprite_folder, filename)
                    image = PIL.Image.open(imgpath)

                    self.backdrop.paste(image, (int(rel_x), int(rel_y)), image)#draw onto file
                    
        self.map_image = ImageTk.PhotoImage(self.backdrop)
        title = self.maincan.create_image(0,0,image=self.map_image, anchor="nw")
        
Memento_Mori().start()

#self.maincan.testimg2 = PIL.Image.open("testimg2.png")
#self.maincan.titlecardpil.paste(self.maincan.testimg2, (50,40), self.maincan.testimg2)
