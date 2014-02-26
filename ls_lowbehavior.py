#by 6n0m0n, SpaceSheep, and malachite_sprite
from ls_behavior import LS_behavior

class LS_lowbehavior(LS_behavior):

    def __init__(self, session, character):
        
        LS_behavior.__init__(self, session, character)
        
    def update_triggers(self):
        
        self.session.add_lowbehavior(self)

    def update_variables(self):
        
        bum = True

    def update_character(self):

        bum = True
        
        
