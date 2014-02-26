#by 6n0m0n, SpaceSheep, and malachite_sprite
from ls_behavior import LS_behavior
from ls_lowbehavior import LS_lowbehavior

class LS_move(LS_lowbehavior):

    def __init__(self, session, character, move_loc):

        LS_lowbehavior.__init__(self, session, character)
        self.move_loc = move_loc
        self.subtype = "move"
        print("Move initiated")

    def update_character(self):

        if status == "success":
            self.character.set_position(move_loc)
            
