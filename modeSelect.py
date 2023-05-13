import pyxel

class ModeSelect():
    def __init__(self, message, cont_list):
        self.message = message
        self.cont_list = cont_list
        self.mode = -1
        self.left_x = 70
        self.init_y = 40
        self.dy = 10
        self.selected = 0
        self.input_counter = 0
    
    def select_up(self):
        if self.selected != 0 and self.input_counter == 0:
            self.selected = self.selected - 1
            self.input_counter = 20

    def select_down(self):
        if self.selected != len(self.cont_list)-1 and self.input_counter == 0:
            self.selected = self.selected + 1
            self.input_counter = 20
    
    def decide(self):
        return self.cont_list[self.selected]
        
    def draw(self):
        pyxel.text(80-(len(self.message)/2*4), 20, self.message, 7)
        for i,v in enumerate(self.cont_list):
            pyxel.text(self.left_x, self.init_y + i*self.dy, str(v), 7)

        pyxel.tri(self.left_x-5,self.init_y + self.selected*self.dy, self.left_x-5,self.init_y + self.selected*self.dy+4, self.left_x-1,self.init_y + self.selected*self.dy+2, 12)
        
        if self.input_counter != 0:
            self.input_counter = self.input_counter -1