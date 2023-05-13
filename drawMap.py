import pyxel
from piranhaPlant import PiranhaPlant as Plant

class DummyMap:

    def __init__(self, mname):
        self.mname = mname
        
        with open(mname) as f:
            self.map_tiles = f.readlines()
        
        self.width=len(self.map_tiles[0])
        self.height=len(self.map_tiles)

        self.goombas = []
        self.plants = []
        self.__summon_chara()

        self.draw_p = 0
        self.not_plant_flag = 0

    def __summon_chara(self):
        for i in range(self.height-1):
            for j in range(self.width-1):
                map_line = self.map_tiles[i] 
                #if map_line[j] == str(2):
                #    self.goombas.append(Goo(1, 10, 10, 1, j*10, i*10))
                if map_line[j] == str(3):
                    self.plants.append(Plant(1, 10, 10, 1, j*10, i*10))
    
    def __draw_charas(self, map_p):
        if self.not_plant_flag == 0:
            for i in self.plants:
                if i.hp != 0:
                    i.draw(1, map_p)
    
    def __draw_items(self,i_type, ix, iy):
        if i_type == 5:
            pyxel.circ(ix, iy, 3, 10)
        elif i_type == 6:
            pyxel.blt(ix, iy, 2, 10, 0, 10, 10, 0)
        elif i_type == 9:
            pyxel.blt(ix, iy, 2, 0, 0, 10, 10, 0)

    def __del_plant(self, xi, yi):
        for i in self.plants:
            if i.init_x / 10 == xi and i.init_y / 10 == yi:
                print('kill')
                i.hp = 0

    def __del_item(self, istr,xi):
        l_str = list(istr)
        l_str[xi] = '0'
        return str("".join(l_str))

    def __hit_object(self, istr, xi, yi, h_item, ene_mode, who):
        wall = ene_mode
        item = 0
        if istr[xi] == str(1):
            wall = 1
            #if who == 'fireball' &&
        if istr[xi] == str(3) and ene_mode == 1:#パックンフラワーと接触
            #if who == 'fireball':
            #    istr = self.__del_item(istr, xi)
            #    self.__del_plant(xi, yi)
            if self.not_plant_flag == 0:
                item = 1
        if istr[xi] == str(3) and ene_mode == 0:#パックンフラワーと接触
            if who == 'fireball':
                istr = self.__del_item(istr, xi)
                self.__del_plant(xi, yi)
            #item = 1
        elif istr[xi] == str(5) and who == 'mario':#コインと接触
            istr = self.__del_item(istr, xi)
            item = 5
        elif istr[xi] == str(6) and who == 'mario':#ファイアーフラワーと接触
            istr = self.__del_item(istr, xi)
            item = 6
        elif istr[xi] == str(9) and who == 'mario':#ゴールフラグと接触
            item = 9
        if h_item != 0:
            item = h_item
        return wall, item, istr

    def get_exist(self, mx, my, who):
        exist = [0,0,0,0,0]
        xp = int(mx/10)
        yp = int(my/10)
        xp_a = mx % 10
        yp_a = my % 10
        '''
        if xp == 0:
            xp = xp + 1
        if yp == 0:
            yp = yp + 1
        '''
        map_line_0 = self.map_tiles[yp-1]
        map_line_1 = self.map_tiles[yp]
        map_line_2 = self.map_tiles[yp+1]
        if map_line_0[xp] != str(0) and who == 'mario':
            exist[0], exist[4], map_line_0 = self.__hit_object(map_line_0, xp, yp-1, exist[4], 0, who)

        if map_line_1[xp-1] != str(0):
            if xp_a < 1:
                exist[1], exist[4], map_line_1 = self.__hit_object(map_line_1, xp-1, yp, exist[4], 0, who)

        if map_line_1[xp+1] != str(0):
            exist[2], exist[4], map_line_1 = self.__hit_object(map_line_1, xp+1, yp, exist[4], 0, who)

        if map_line_2[xp] != str(0) and who == 'mario':
            exist[3], exist[4], map_line_2 = self.__hit_object(map_line_2, xp, yp+1, exist[4], 0, who)

        if map_line_2[xp + 1] != str(0) and xp_a > 5 and who == 'mario':
            exist[3], exist[4], map_line_2 = self.__hit_object(map_line_2, xp+1, yp+1, exist[4], 0, who)
        
        if map_line_1[xp] != str(0):
            exist[3], exist[4], map_line_1 = self.__hit_object(map_line_1, xp, yp, 0, 1, who)

        #変更適用
        self.map_tiles[yp-1] = map_line_0
        self.map_tiles[yp] = map_line_1
        self.map_tiles[yp+1] = map_line_2
        
        return exist
        
    def not_plants(self, notcode):
        if notcode == 'EASY':
            self.not_plant_flag = 1
        else:
            self.not_plant_flag = 0

    #mpはマップの左からのpixel数
    def draw(self,mx):
        mp_a = int(mx % 10)
        #pyxel.text(0, 20, 'mp_a : ' + str(mp_a), 7)

        self.draw_p = int(mx/10) - 3
        
        for i in range(12):
            map_line = self.map_tiles[i] 
            for j in range(17):
                if j + self.draw_p > len(map_line)-1:
                    break
                if j == 0:
                    if map_line[j + self.draw_p] == str(1):
                        pyxel.rect(0, i*10, (10-mp_a), 10, 11)
                else:
                    if map_line[j + self.draw_p] == str(1):
                        pyxel.rect(j*10 - mp_a, i*10, 10, 10, 11)
                
                if map_line[j + self.draw_p] == str(5):#コイン
                    #pyxel.circ(j*10+5 - mp_a, i*10+5, 3, 10)
                    self.__draw_items(5, j*10+5 - mp_a, i*10+5)
                if map_line[j + self.draw_p] == str(6):#ファイアーフラワー
                    self.__draw_items(6, j*10 - mp_a, i*10)
                elif map_line[j + self.draw_p] == str(9):#ゴール
                    self.__draw_items(9, j*10 - mp_a, i*10)
        
        self.__draw_charas(int((mx-30)/10)*10 + mp_a)

            


