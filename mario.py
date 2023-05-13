import pyxel
from character import Character

class Mario(Character):
    def __init__(self, hp, size_x, size_y, inum, x_limit):
        Character.__init__(self, hp, size_x, size_y, inum)
        self.x = 30
        self.x_limit = x_limit
        self.dash_flag = 0
        self.jump_count = 0
        self.coin_num = 0
        self.mode = 0

        self.fire_limit = 5
        self.fired = 0
        self.reloading = 0
        self.fire_balls = []
        for i in range(self.fire_limit):#装填
            self.fire_balls.append(FireBall())

        #pyxel.play(0,0,loop = False)#開始音
    
    def move(self, direction):
        if direction == 'LEFT':
            self.lr_flag = 1
            #pyxel.image(self.img_num).load(0, 0, self.img_name_L)
            self.x -= 2
            if self.x < 30:
                self.x = 30
        elif direction == 'RIGHT':
            self.lr_flag = 0
            #pyxel.image(self.img_num).load(0, 0, self.img_name_R)
            self.x += 2
            if self.x > (self.x_limit - self.size_x) -10:
                self.x = self.x_limit - self.size_x -10
        elif direction == 'JUMP':
            if self.jump_count > 5:
                self.y -= 5
            if self.jump_count == 10:
                pyxel.play(0,2,loop = False)#ジャンプ音
            self.jump_count = self.jump_count -1
            #if self.jump_count < 0:
            #    self.jump_count = 0 
    
    def contact(self, contact_type):
        if contact_type == 1:
            self.hp = self.hp - 1 
            if self.hp < 0:
                self.hp = 0
            #print('HIT! : hp =', self.hp)
        elif contact_type == 5:
            self.coin_num = self.coin_num + 1
            pyxel.play(0,1,loop = False)#コイン音
        elif contact_type == 6:
            self.mode = 1
            self.hp = self.hp + 1
            pyxel.play(0,4,loop = False)#返信音
    
    def attack(self):
        if self.mode == 1 and self.reloading == 0:
            self.fire_balls[self.fired].fire(self.lr_flag, self.x, self.y)
            self.fired = self.fired + 1
            pyxel.play(0,3,loop = False)#攻撃音
            if self.fired > 4:
                self.fired = 0
            self.reloading = 20
            

    def draw(self, floor):
        #pyxel.text(0, 10, 'x : '+str(self.x), 7)
        if self.hp == 0:
            return
        if self.lr_flag == 0: #R
            pyxel.blt(30, self.y, self.img_num, 10, 0+self.mode*10, self.size_x, self.size_y, self.hide_color)
        else: #L
            pyxel.blt(30, self.y, self.img_num, 0, 0+self.mode*10, self.size_x, self.size_y, self.hide_color)
        Character.draw(self, floor)
        if self.jump_count > 0:
            self.move('JUMP')
        
        if self.reloading > 0:
            self.reloading = self.reloading - 1
        for i in range(self.fire_limit):
            self.fire_balls[i].draw()

class FireBall:
    def __init__(self):
        self.size_x = 10
        self.size_y = 10
        self.draw_x = 0
        self.x = 0
        self.y = 0
        self.draw_flag = 0# 1=R 2=L
        self.damage = 1
    
    def fire(self, lr_flag, mx, my):
        self.draw_flag = lr_flag + 1
        self.draw_x = 30
        self.x = mx
        self.y = my
    
    def hit(self, map_exist):
        if (map_exist[1] == 1 and map_exist[4] != 1) or (map_exist[2] == 1 and map_exist[4] != 1) or  map_exist[4] == 1:
        #if map_exist[4] == 1:
            print('hit!')
            print(map_exist[1], map_exist[2], map_exist[4])
            self.draw_flag = 0
            self.x = 0
            self.y = 0

    def draw(self):
        if self.draw_flag != 0:
            if self.draw_flag == 1:#R
                self.x = self.x + 2
                self.draw_x = self.draw_x + 2
                if self.draw_x > 150:
                    self.draw_flag = 0
                    self.draw_x = 0
                    self.x = 0
                    self.y = 0
                else:
                    pyxel.blt(self.draw_x, self.y, 0, 30, 10, self.size_x, self.size_y, 0)
            else:#L
                self.x = self.x - 2
                self.draw_x = self.draw_x - 2
                if self.draw_x < 0:
                    self.draw_flag = 0
                    self.draw_x = 0
                    self.x = 0
                    self.y = 0
                else:
                    pyxel.blt(self.draw_x, self.y, 0, 20, 10, self.size_x, self.size_y, 0)
        


