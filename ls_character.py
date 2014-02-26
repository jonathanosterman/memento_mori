#by 6n0m0n, SpaceSheep, and malachite_sprite

from ls_behavior import LS_behavior
from ls_lowbehavior import LS_lowbehavior
from ls_move import LS_move

class LS_character:

    def __init__(self, session, chindex, ch_info_list):
        
        self.session = session
        
        self.chindex = chindex

        self.roots = []

        self.type = None
        self.subtype = None

        self.name = None
        self.visual_state = ""
        self.anim_state = ""
        self.sprite_folder = None
        self.personality = None
        self.nat_health = None
        self.cur_health = None
        self.nat_calm = None
        self.cur_calm = None
        self.item_arr = []
        self.position = []
        self.orientation = None
        #BEGIN string parser
        label_list = ["type", "subtype", "name", "orientation", "personality", "sprite_folder"]

        for j in label_list:
            for i in ch_info_list:

                if j == i.split("=")[0]:
                    set_str = i.split("=")[1]
                    setattr(self, j, set_str)

                    print (set_str)

        int_attr_list = ["nat_health", "cur_health", "nat_calm", "cur_calm"]

        for j in int_attr_list:
            for i in ch_info_list:

                if j == i.split("=")[0]:
                    set_int = int(i.split("=")[1])
                    setattr(self, j, set_int)

                    print (set_int)

        int_array_attr_list = ["position"]

        for j in int_array_attr_list:
            for i in ch_info_list:

                if j == i.split("=")[0]:

                    arg_split = i.split("=")[1].split(",")
                    set_array = []
                    
                    for k in arg_split:
                        set_array.append(int(k))

                    setattr(self, j, set_array)
                    print(set_array)
        #END string parser
        print(session.map_arr[self.position[0]][self.position[1]][self.position[2]])

        session.map_arr[self.position[0]][self.position[1]][self.position[2]].contained_ch = self #sloppy in general; only do this when initializing from file
        
    def update(self):

        for i in self.roots:
            i.update()

    def set_position(self, move_loc):

        self.session.map_arr[self.position[0]][self.position[1]][self.position[2]].contained_ch = None
        self.session.map_arr[move_loc[0]][move_loc[1]][move_loc[2]].contained_ch = self
        self.position = move_loc
