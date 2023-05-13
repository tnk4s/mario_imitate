import pyxel
from mario import Mario
from drawMap import DummyMap
from modeSelect import ModeSelect 
import datetime
import time

class App:
    def __init__(self):
        pyxel.init(160, 120, fps=60)#, caption='Mario?')#(w,h)
        pyxel.load("./resource/mario.pyxres")

        self.draw_page = 0 #0:select_difficulty 1:mario 2:select_play
        self.difficulty = ''
        self.select_difficulty = ModeSelect('Select Difficulty', ['NORMAL', 'EASY'])
        self.select_play = ModeSelect('CONTINUE?', ['CONTINUE', 'END'])

        self.map_limit = 3
        self.now_map = 1
        self.map = DummyMap("./maps/map1.txt")
        self.mario = Mario(1, 10, 10, 0, self.map.width*10)
        self.mario_positon = 0
        self.map_exist = [0,0,0,0,0]#[上,左,右,下,敵]
        self.fireball_exist = [0,0,0,0,0]
        self.game_set_flag = 0
        self.game_set_counter = 0

        #pyxel.playm(0, loop=True)
        self.dt_start = datetime.datetime.now()
        self.dt_end = None
        self.td = None
        self.redo_counter = 0
        pyxel.run(self.update, self.draw)
    
    def __redo(self, map_num):
        self.draw_page = 0 #0:select_difficulty 1:mario 2:select_play
        self.difficulty = ''
        self.select_difficulty = ModeSelect('Select Difficulty', ['NORMAL', 'EASY'])
        self.select_play = ModeSelect('CONTINUE?', ['CONTINUE', 'END'])

        self.now_map = map_num
        if self.now_map > self.map_limit:
            self.now_map = self.map_limit
        map_name = './maps/map' + str(map_num) + '.txt'
        self.map = DummyMap(map_name)
        self.mario = Mario(1, 10, 10, 0, self.map.width*10)
        self.mario_positon = 0
        self.map_exist = [0,0,0,0,0]#[上,左,右,下,敵]
        self.fireball_exist = [0,0,0,0,0]
        self.game_set_flag = 0
        self.game_set_counter = 0

        self.dt_start = datetime.datetime.now()
        self.dt_end = None
        self.td = None

        self.redo_counter = 30

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        self.map_exist = self.map.get_exist(self.mario.x, self.mario.y, 'mario')
    
        for i in range(self.mario.fire_limit):
            if self.mario.fire_balls[i].draw_flag == 1:
                self.fireball_exist = self.map.get_exist(self.mario.fire_balls[i].x, self.mario.fire_balls[i].y, 'fireball')
                self.mario.fire_balls[i].hit(self.fireball_exist)
        
        self.update_player()
        
    def update_player(self):
        if self.draw_page == 0:
            if self.redo_counter != 0:
                    self.redo_counter = self.redo_counter - 1
            if pyxel.btn(pyxel.KEY_RIGHT): #or pyxel.btn(pyxel.GAMEPAD_1_RIGHT):
                if self.redo_counter == 0:
                    self.difficulty = self.select_difficulty.decide()
                    self.map.not_plants(self.difficulty)
                    print('select difficulty!')
                    self.draw_page = 1
                    #pyxel.playm(0, loop=True)
                    pyxel.play(0,0,loop = False)#開始音
            if pyxel.btn(pyxel.KEY_UP):# or pyxel.btn(pyxel.GAMEPAD_1_UP):
                self.select_difficulty.select_up()
            if pyxel.btn(pyxel.KEY_DOWN):# or pyxel.btn(pyxel.GAMEPAD_1_DOWN):
                self.select_difficulty.select_down()

        elif self.draw_page == 1:
            if pyxel.btn(pyxel.KEY_LEFT):# or pyxel.btn(pyxel.GAMEPAD_1_LEFT):
                if self.map_exist[1] != 1:
                    if self.map_exist[3] != 1 and self.mario.jump_count == 0:
                        pass
                    else:
                        self.mario.move('LEFT')
            if pyxel.btn(pyxel.KEY_RIGHT):# or pyxel.btn(pyxel.GAMEPAD_1_RIGHT):
                if self.map_exist[2] != 1:
                    if self.map_exist[3] != 1 and self.mario.jump_count == 0:
                        pass
                    else:
                        self.mario.move('RIGHT')
            if pyxel.btn(pyxel.KEY_UP):# or pyxel.btn(pyxel.GAMEPAD_1_UP):
                if self.map_exist[0] != 1 and self.map_exist[3] == 1 and self.mario.jump_count == 0:
                    self.mario.jump_count = 10
                    self.mario.move('JUMP')
            if pyxel.btn(pyxel.KEY_DOWN):# or pyxel.btn(pyxel.GAMEPAD_1_DOWN):
                self.mario.attack()
            
            if self.map_exist[0] == 1:#頭がぶつかったら墜落
                self.mario.jump_count = 0
            '''
            elif self.map_exist[1] == 1 and self.map_exist[3] != 1:
                self.mario.x = self.mario.x + 1
            elif self.map_exist[2] == 1 and self.map_exist[3] != 1:
                self.mario.x = self.mario.x - 1
            '''
        elif self.draw_page == 2:
            if pyxel.btn(pyxel.KEY_RIGHT):# or pyxel.btn(pyxel.GAMEPAD_1_RIGHT):
                retry = self.select_play.decide()
                if retry == 'CONTINUE':
                    self.__redo(1)
                else:
                    pyxel.quit()
            if pyxel.btn(pyxel.KEY_UP):# or pyxel.btn(pyxel.GAMEPAD_1_UP):
                self.select_play.select_up()
            if pyxel.btn(pyxel.KEY_DOWN):# or pyxel.btn(pyxel.GAMEPAD_1_DOWN):
                self.select_play.select_down()


    def draw(self):
        pyxel.cls(0)
        #pyxel.text(55, 41, "Hello, Pyxel!", pyxel.frame_count % 16)
        if self.draw_page == 0:
            self.select_difficulty.draw()
        elif self.draw_page == 1:
            self.map.draw(self.mario.x)
            self.mario.contact(self.map_exist[4])
            self.mario.draw(self.map_exist[3])

            #draw status
            stage_name = 'stage : ' + str(self.now_map)
            pyxel.text(0, 0, stage_name, 7)
            message = 'coin : ' + str(self.mario.coin_num)
            pyxel.text(0, 10, message, 7)
            message = 'mode : ' + str(self.mario.mode)
            pyxel.text(0, 20, message, 7)

            if self.game_set_flag != 0:
                self.game_set_counter = self.game_set_counter + 1
            if self.game_set_counter == 240:
                if self.game_set_flag == 1:#しぼう
                    self.draw_page = 2
                elif self.game_set_flag == 2:
                    if self.now_map == self.map_limit:
                        self.draw_page = 2
                    else:
                        self.__redo(self.now_map + 1)
            self.game_judge()
            
        elif self.draw_page == 2:
            self.select_play.draw()

    def game_judge(self):
        if self.mario.hp == 0:
            #print('GAME SET !')
            pyxel.text(58, 41, 'GAME OVER !', pyxel.frame_count % 16)
            if self.game_set_flag == 0:
                pyxel.play(0,5,loop = False)#しぼう音
                self.game_set_flag = 1
                
        elif self.map_exist[4] == 9:
            if self.game_set_flag == 0:
                pyxel.play(0,6,loop = False)#クリア音
                self.game_set_flag = 2
                self.dt_end = datetime.datetime.now()
                self.td = self.dt_end - self.dt_start
                print(self.td.total_seconds())
                
            pyxel.text(58, 31, 'GAME CLEAR !', pyxel.frame_count % 16)
            message = ['coin : ' + str(self.mario.coin_num), 'TIME : ' + str(int(self.td.total_seconds()))+'s']
            for i,v in enumerate(message):
                pyxel.text(58, 41 + 10*i, v, 7)
            
            
      
if __name__ == '__main__':
    play = 1
    while play == 1:
        play = App()