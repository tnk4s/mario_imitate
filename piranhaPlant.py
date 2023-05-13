import pyxel
from character import Character

class PiranhaPlant(Character):
    def __init__(self, hp, size_x, size_y, inum, x_position, y_position):
        Character.__init__(self, hp, size_x, size_y, inum)
        self.init_x = x_position
        self.init_y = y_position
        self.x = self.init_x
        self.y = self.init_y
        self.mouth_flag = 0
        self.mouth_counter = 30
    
    def __in_and_out(self):
        if self.mouth_flag == 0:
            pyxel.blt(self.x, self.y, self.img_num, 0, 0, self.size_x, self.size_y, self.hide_color)#close
        else:
            pyxel.blt(self.x, self.y, self.img_num, 10, 0, self.size_x, self.size_y, self.hide_color)#open
        
        self.mouth_counter = self.mouth_counter - 1
        if self.mouth_counter == 0:
            self.mouth_flag = 1 - self.mouth_flag
            self.mouth_counter = 30
    
    def draw(self, floor, map_p):
        self.x = self.init_x - map_p
        Character.draw(self, floor)
        self.__in_and_out()
