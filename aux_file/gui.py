from ssquare import Ssquare
from session import Session
from tkinter import *
from PIL import *
from PIL import ImageTk
import PIL.Image
#creates a window with widgets and dialoge to start session

class Gui(Tk):

    def openfolder(self):
        folderloc= filedialog.askdirectory()
        self.session = Session(folderloc)
        self.session.update()
        self.drawmap()
    
    def __init__(self):
        Tk.__init__(self)

        resolution = [1600, 900]
        z_level = 0
        
        self.configure(background="green")
        
        #menu bar
        menubar = Menu(self)
        self["menu"] = menubar
        
        filemenu = Menu(menubar)
        optionmenu = Menu(menubar)
        
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Options", menu=optionmenu)

        filemenu.add_command(label="Open", command=self.openfolder)
        optionmenu.add_command(label="Nothing")

        #main canvas
        self.maincan = Canvas(master=self)

        self.maincan.titlecardpil = PIL.Image.open("titlecard.png")
        #self.maincan.testimg2 = PIL.Image.open("testimg2.png")
        #self.maincan.titlecardpil.paste(self.maincan.testimg2, (50,40), self.maincan.testimg2)
        self.maincan.titlecard = ImageTk.PhotoImage(self.maincan.titlecardpil)
        self.maincan.config(width = resolution[0]-5, height = resolution[1]-10, background = "green")
        
        title = self.maincan.create_image(0,0,image=self.maincan.titlecard, anchor="nw")

        self.maincan.grid(row="0")

    def drawmap(self):

        map_arr = self.session.map_arr
        print("Map loaded into gui")

        x_dim = len(map_arr[0][0])
        y_dim = len(map_arr[0])
        z_dim = len(map_arr)

        print(x_dim, y_dim, z_dim)
        print(z_level)

Gui()
