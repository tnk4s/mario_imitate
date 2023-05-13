import pyxel

class Character:

    def __init__(self, hp, size_x, size_y, inum):
        pyxel.load("./resource/mario.pyxres")
        self.hp = hp
        self.x = 0
        self.y = 0#120 - size_y
        self.size_x = size_x
        self.size_y = size_y
        
        self.lr_flag = 0
        self.img_num = inum
        self.hide_color = 0
        #self.img_name_L = img_name + '_L.png'
        #self.img_name_R = img_name + '_R.png'
        #pyxel.image(self.img_num).load(0, 0, self.img_name_R)
        
    def get_position(self):
        position = [self.x, self.y]
        return position
    
    def draw(self, floor):
        #pyxel.cls(0)

        if self.y < (120 - self.size_y) and floor != 1:#疑似重力
            self.y += 1
            


