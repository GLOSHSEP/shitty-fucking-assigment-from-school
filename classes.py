try:
    import pygame 
except: 
    print("ERROR YOU NEED PYGAME INSTALL") 
    exit(1) 
try: 
    import os 
except: 
    print("ERROR YOU NEED THE OS LIBRARY IS YOUR PYTHON INSTALTTION MESSED UP") 
    exit(1) 

class map_game: 
    def __init__(self, map_need): 
        self.map_need = map_need
    def read_map(self, lis_ins, window, extra_vars): 
        for i in self.map_need: 
            exec('lis_ins.append(' + i + ')') 

class obj: 
    def __init__(self, sprite_image, x, y, visible, frozen, window_to_draw): 
        self.sprite_image = sprite_image 
        self.x = x 
        self.y = y 
        self.visible = visible 
        self.frozen = frozen 
        self.sprite = pygame.image.load(sprite_image)
        self.window_to_draw = window_to_draw 
        rectangle = self.sprite.get_rect() 
        self.collision = rectangle 
        self.collision.center = (self.x + (rectangle[2] / 2), self.y + (rectangle[3] / 2)) 
        #ideally you have some string like 'current_instance.instance_code();current.instance_draw() 
        self.inputarray = [""] #[misc_inputs]
        self.returnarray = ["", 0] #[misc_outputs, destroy] 
        self.name = "obj" 

    def instance_code(self): 
        if self.frozen != True: 
            self.update_collision()

    def instance_draw(self): 
        if self.visible == True: 
            self.window_to_draw.blit(self.sprite, (self.x, self.y)) 

    def instance_edit_array(self, io, index, value): 
        if io == "i": 
            self.inputarray[index] = value  
        elif io == "o": 
            self.returnarray[index] = value 

    def instance_done(self): 
        return self.returnarray
    
    def instance_pre(self): 
        return self.inputarray 
    
    def colliding(self, x, y, i_instance): 
        rectmodxy = [x, y, self.collision[2], self.collision[3]]
        return i_instance.collision.colliderect(rectmodxy) 
    
    def key_check_press(self, pre, cur, index): 
        if pre[index] != cur[index]: 
            return True 
        else: 
            return False 
        
    def sign(self, just_a_number_smh): 
        if just_a_number_smh > 0: 
            return 1 
        elif just_a_number_smh < 0: 
            return -1 
        elif just_a_number_smh == 0: 
            return 0 
        
    def update_collision(self): 
        rectangle = self.sprite.get_rect() 
        self.collision = rectangle 
        self.collision.center = (self.x + (rectangle[2] / 2), self.y + (rectangle[3] / 2)) 
    
class player(obj): 
    def __init__(self, sprite_image, x, y, window_to_draw): 
        obj.__init__(self, sprite_image, x, y, True, False, window_to_draw) 
        self.hsp = 0 
        self.vsp = 0 
        self.walksp = 5
        self.grv = 0.5 
        self.grounded = False 
        self.jump_key_hold = False 
        self.z_key_hold = True 
        self.found_ground = False 
        self.executestring = "current_instance.instance_code(input_array, lis_ins);current_instance.instance_draw()"
        self.inputarray = [self.executestring] 
        self.name = "player" 
        self.facing = 1 
        self.health = 3
        self.animations = ["stand", "walk", "jump", "fall"] 
        self.an_state = self.animations[0] 
        self.frame_fps = 0 
        self.frame = 0 
        self.font_draw = pygame.font.Font("fontgame.ttf", 30) 

    def instance_code(self, input_array, lis_ins): 
        if self.frozen != True: 
            #move the player 
            self.move(input_array, lis_ins) 
            #set the collison 
            self.update_collision() 

    def instance_draw(self): 
        if self.visible == True: 
            false = False 
            if self.facing == 1: flip = False 
            else: flip = True
            self.window_to_draw.blit(pygame.transform.flip(self.sprite, flip, False), (self.x, self.y)) 
            health_draw = self.font_draw.render("PLAYER HP:  " + str(self.health), False, (255, 255, 255)) 
            self.window_to_draw.blit(health_draw, (450, 10)) 
    
    def move(self, input_provided, lis_ins): 
        #get player input and translate it to movement baiscally 
        move = input_provided[1] - input_provided[0] 

        self.hsp = move * self.walksp 
        self.vsp = self.vsp + self.grv 

        if self.hsp != 0: 
            self.facing = self.sign(self.hsp)

        if input_provided[3] == True and self.jump_key_hold == False and self.grounded == True: 
            self.jump_key_hold = True 
            self.grounded = False 
            self.vsp -= 15 

        if self.jump_key_hold == True: 
            if input_provided[3] == False: 
                self.jump_key_hold = False 
        
        #collsion
        for i in lis_ins: 
            #wall
            if i.name == "wall": 
                if self.colliding(self.x + self.hsp, self.y, i) == True: 
                    while self.colliding(self.x + self.sign(self.hsp), self.y, i) != True:
                        self.x += self.sign(self.hsp) 
                    self.hsp = 0 

                if self.colliding(self.x, self.y + self.vsp, i) == True: 
                    while self.colliding(self.x, self.y + self.sign(self.vsp), i) != True:
                        self.y += self.sign(self.vsp) 
                    self.vsp = 0 

                if self.colliding(self.x, self.y + self.vsp + 1, i) == True: 
                    self.found_ground = True 
                    self.grounded = True 

                if self.found_ground == False: 
                    self.grounded = False 
                else: 
                    self.grounded = True 
            #fire
            elif i.name == "bullet": 
                if i.enemy == False: 
                    if self.colliding(self.x, self.y, i) == True: 
                        self.health -= 1 
                        lis_ins[0].points -= 200
                        i.returnarray[1] = 1 
                        self.hsp = 0 
                        self.vsp = 0 


        #shooting 
        if input_provided[4] == 1 and self.z_key_hold == False: 
            lis_ins.append(fire(self.x, self.y, self.window_to_draw, 10 * self.facing, 0, ["wall"], True)) 
            self.z_key_hold = True 

        if self.z_key_hold == True: 
            if input_provided[4] == False: 
                self.z_key_hold = False 

        #dying and ending the game 
        if self.health <= 0: lis_ins[0].state = lis_ins[0].states[1] 

        #animation 
        #stand 
        if self.hsp == 0 and self.vsp == 0: 
            self.an_state = self.animations[0] 
        #walk 
        elif self.hsp != 0 and self.vsp == 0 and self.grounded == True: 
            self.an_state = self.animations[1] 
        #jump
        elif self.vsp < 0: 
            self.an_state = self.animations[2] 
        #fall 
        elif self.vsp > 0: 
            self.an_state = self.animations[3] 

        #stand 
        if self.an_state == self.animations[0]:
            self.sprite = pygame.image.load("player.png") 

        #walk 
        elif self.an_state == self.animations[1]: 
            #60 / 30 = 2 
            if self.frame_fps >= 2: 
                #frame 0 
                if self.frame == 0: 
                    self.frame = 1
                    self.sprite = pygame.image.load("player.png") 
                #frame 1
                elif self.frame == 1: 
                    self.frame = 0
                    self.sprite = pygame.image.load("playerwalk.png") 
                self.frame_fps = -1 

        #jump
        elif self.an_state == self.animations[2]:
            self.sprite = pygame.image.load("playerjump.png") 
        #fall
        elif self.an_state == self.animations[3]:
            self.sprite = pygame.image.load("playerfall.png") 

        #add fps counter 
        self.frame_fps += 1

        #reset the ground variable 
        self.found_ground = False 

        #actually move 
        self.x += self.hsp 
        self.y += self.vsp 

class wall(obj): 
    def __init__(self, sprite_image, x, y, window_to_draw): 
        obj.__init__(self, sprite_image, x, y, True, False, window_to_draw) 
        self.inputarray = ["current_instance.instance_draw()"] 
        self.name = "wall" 

class fire(obj): 
    def __init__(self, x, y, window_to_draw, hsp, vsp, kill_objs, enemy): 
        obj.__init__(self, "bullet_1.png", x, y, True, False, window_to_draw)
        self.hsp = hsp 
        self.vsp = vsp 
        self.kill_objs = kill_objs 
        self.inputarray = ["current_instance.instance_code(lis_ins);current_instance.instance_draw()"]
        self.name = "bullet" 
        self.enemy = enemy 
        self.frame = 0 
        self.frame_fps = 0 

    def instance_code(self, lis_ins): 
        if self.frozen != True: 
            #set the collison 
            self.update_collision()

            #move
            self.x += self.hsp 
            self.y += self.vsp 

            #collision 
            for i in lis_ins: 
                for b in self.kill_objs:
                    if i.name == b: 
                        if self.colliding(self.x + self.hsp, self.y, i) == True: 
                            self.returnarray[1] = 1

                        if self.colliding(self.x, self.y + self.vsp, i) == True: 
                            self.returnarray[1] = 1 

            #outside room 
            if self.x <= -64 or self.y <= -64 or self.x >= 704 or self.y >= 544: 
                self.returnarray[1] = 1 

            #animation 
            #60 / 16 = 3.75 so it will run at 16 fps 
            if self.frame_fps >= 3.75: 
                if self.frame == 0: 
                    #set next frame 
                    self.frame = 1 
                    #load sprite 
                    self.sprite = pygame.image.load("bullet_2.png") 
                elif self.frame == 1: 
                    self.frame = 0  
                    self.sprite = pygame.image.load("bullet_1.png") 
                #reset fps counter 
                self.frame_fps = -1 
            #add fps counter 
            self.frame_fps += 1 

class enemy_spawner(obj): 
    def __init__(self, enemy_path, window_to_draw, extra_vars): 
        obj.__init__(self, "wall.png", 0, 0, True, False, window_to_draw) 
        self.enemy_path = enemy_path 
        self.path_step = 0 
        self.counter = 0 
        self.extra_vars = extra_vars 
        self.inputarray = ["current_instance.instance_code(lis_ins, window)"] 

    def instance_code(self, lis_ins, window): 
        if self.frozen != True:
            if self.path_step + 1 <= len(self.enemy_path):  
                current_step = self.enemy_path[self.path_step] 
                if current_step[0] == self.counter: 
                    exec('lis_ins.append( ' + current_step[1] + ' )') 
                    self.path_step += 1 
            self.counter += 1 

class protect_square(obj): 
    def __init__(self, sprite_image, x, y, window_to_draw, health): 
        obj.__init__(self, sprite_image, x, y, True, False, window_to_draw) 
        self.health = health 
        self.font_draw = pygame.font.Font("fontgame.ttf", 30) 
        self.inputarray = ["current_instance.instance_code(lis_ins);current_instance.instance_draw()"] 

    def instance_code(self, lis_ins): 
        if self.frozen != True: 
            #check for bullets 
            for i in lis_ins:   
                if i.name == "bullet": 
                    if i.enemy == False: 
                        if self.colliding(self.x, self.y, i) == True: 
                            lis_ins[0].points -= 500
                            self.health -= 1 
                            i.returnarray[1] = 1 
            #end life 
            if self.health <= 0: lis_ins[0].state = lis_ins[0].states[1]  

            #update collision 
            self.update_collision() 

    def instance_draw(self): 
        if self.visible == True:
            self.window_to_draw.blit(self.sprite, (self.x, self.y)) 
            health_draw = self.font_draw.render("SQUARE HP:  " + str(self.health), False, (255, 255, 255)) 
            self.window_to_draw.blit(health_draw, (450, 40)) 

class logic_controller(obj): 
    def __init__(self, window_to_draw): 
        obj.__init__(self, "bg.png", 0, 0, True, False, window_to_draw) 
        self.states = ["game", "lose", "how", "menu", "results", "win"] 
        self.state = self.states[3] 
        self.name = "manager" 
        self.points = 0 
        if os.path.exists("score"): 
            file = open("score", "r") 
            self.high_points = int(file.read())
            file.close() 
        else: 
            self.high_points = 0 
        self.counter = 60 * 120 #game length 
        self.font_draw = pygame.font.Font("fontgame.ttf", 30) 
        self.cursor = 10 
        self.release = [1, 1, 1] #down up Z 
        self.how = pygame.image.load("how.png") 
        self.inputarray = ["current_instance.instance_code(lis_ins, input_array);current_instance.instance_draw()"] 

    def instance_code(self, lis_ins, input_array): 
        #state machine 
        #menu 
        if self.state == self.states[3]: 
            #play 
            if self.cursor == 10 and input_array[4] and self.release[2] == 0:
                #load the map
                self.create_game_data(lis_ins, self.window_to_draw) 
                #swap state to game 
                self.state = self.states[0] 

            #how to play 
            elif self.cursor == 70 and input_array[4] and self.release[2] == 0: 
                self.state = self.states[2]
            #erase data 
            elif self.cursor == 130 and input_array[4] and self.release[2] == 0: 
                if os.path.exists("score"): 
                    os.remove("score") 
                self.high_points = 0 

            #move cursor
            if self.cursor >= 70 and input_array[3] and self.release[1] == 0: self.cursor -= 60 
            if self.cursor <= 70 and input_array[2] and self.release[0] == 0: self.cursor += 60 

            #release 
            #key Z 
            if input_array[4]: 
                self.release[2] = 1 
            else: 
                self.release[2] = 0 

            #key down 
            if input_array[2]: 
                self.release[0] = 1 
            else: 
                self.release[0] = 0 

            #key up 
            if input_array[3]: 
                self.release[1] = 1 
            else: 
                self.release[1] = 0 
        #game 
        elif self.state == self.states[0]: 
            self.counter -= 1 
            self.points += 1 
            if (self.points > self.high_points): self.high_points = self.points
            if self.counter <= 0: self.state = self.states[5]
        #loose 
        elif self.state == self.states[1]: 
            #loop through every instance and destroy them basically 
            while len(lis_ins) > 0: 
                lis_ins.pop(0) 

            #save the score 
            if os.path.exists("score"): 
                os.remove("score") 
                file = open("score", "x") 
                file.write(str(self.high_points)) 
                file.close() 
            else: 
                file = open("score", "x") 
                file.write(str(self.high_points)) 
                file.close() 

            #create results manager 
            lis_ins.append(results("loose.png", self.window_to_draw, self.points, self.high_points, False)) 
        #how to play 
        elif self.state == self.states[2]: 
            #swap state 
            if input_array[4] and self.release[2] == 0: self.state = self.states[3] 
            #release 
            #key Z 
            if input_array[4]: 
                self.release[2] = 1 
            else: 
                self.release[2] = 0 
        #win 
        elif self.state == self.states[5]: 
            #loop through every instance and destroy them basically 
            while len(lis_ins) > 0: 
                lis_ins.pop(0) 

            #save the high score 
            if os.path.exists("score"): 
                os.remove("score") 
                file = open("score", "x") 
                file.write(str(self.high_points)) 
                file.close() 
            else: 
                file = open("score", "x") 
                file.write(str(self.high_points)) 
                file.close() 

            #create results manager 
            lis_ins.append(results("win.png", self.window_to_draw, self.points, self.high_points, True)) 

    def instance_draw(self): 
        if self.visible == True: 
            #game 
            if self.state == self.states[0]: 
                self.window_to_draw.blit(self.sprite, (0, 0))
                score_draw = self.font_draw.render("HIGH SCORE: " + str(self.high_points), False, (255, 255, 255)) 
                self.window_to_draw.blit(score_draw, (10, 10)) 
                score_draw = self.font_draw.render("SCORE: " + str(self.points), False, (255, 255, 255)) 
                self.window_to_draw.blit(score_draw, (10, 40)) 
                score_draw = self.font_draw.render("TIME: " + str(self.counter // 60), False, (255, 255, 255)) 
                self.window_to_draw.blit(score_draw, (10, 70)) 
            #menu
            elif self.state == self.states[3]: 
                cursor_draw = self.font_draw.render("<", False, (255, 255, 255)) 
                self.window_to_draw.blit(cursor_draw, (200, self.cursor)) 
                menu_draw = self.font_draw.render("PLAY GAME", False, (255, 255, 255)) 
                self.window_to_draw.blit(menu_draw, (10, 10)) 
                menu_draw = self.font_draw.render("HOW TO PLAY", False, (255, 255, 255)) 
                self.window_to_draw.blit(menu_draw, (10, 70)) 
                menu_draw = self.font_draw.render("ERASE", False, (255, 255, 255)) 
                self.window_to_draw.blit(menu_draw, (10, 130)) 
                score_draw = self.font_draw.render("HIGH SCORE: " + str(self.high_points), False, (255, 255, 255)) 
                self.window_to_draw.blit(score_draw, (400, 10)) 
                controlls_z= self.font_draw.render("Z TO SELECT OPTION", False, (255, 255, 255)) 
                self.window_to_draw.blit(controlls_z, (400, 40)) 
                controlls_arrows = self.font_draw.render("ARROW KEYS TO SELECT OPTION", False, (255, 255, 255)) 
                self.window_to_draw.blit(controlls_arrows, (280, 70)) 
            #how to play 
            elif self.state == self.states[2]: 
                self.window_to_draw.blit(self.how, (0,0))
                

    #create game data 
    def create_game_data(self, lis_ins, window): 
        #array for the enemy path
        base_enemy_path = [ 
            [1, 'hm', 1], [60*2, 'attack' , 2]#right path
        ] 
        base_enemy_path_l = [ 
            [1, 'hm', -1], [60*2, 'attack' , -2] #left path
        ] 
        enemy_path_rush = [
            [1, 'hm', 5], [60*2, 'attack', 5]
        ] 
        enemy_path_rush_l = [
            [1, 'hm', -5], [60*2, 'attack', -5] 
        ]
        enemy_paths = [ 
            base_enemy_path, 
            base_enemy_path_l, 
            enemy_path_rush, 
            enemy_path_rush_l 
        ] 
        #array for the enmy spawner path 
        enemy_spawner_path = [ 
            [60*10, "enemy('wall.png', -64, 416, window, 5, self.extra_vars[0])"], #shoot right guy 
            [60*10+1, "enemy_sl('wall.png', 674, 416, window, 5, self.extra_vars[1])"], #shoot left guy 
            [60*25, "enemy('wall.png', -64, 416, window, 5, self.extra_vars[0])"], #wave
            [60*25+20, "enemy('wall.png', -64, 416, window, 5, self.extra_vars[0])"], 
            [60*25+50, "enemy('wall.png', -64, 416, window, 5, self.extra_vars[0])"],
            [60*25+90, "enemy_sl('wall.png', -64, 416, window, 5, self.extra_vars[1])"], 
            [60*29, "enemy_sl('wall.png', -64, 416, window, 5, self.extra_vars[2])"], 
            [60*40, "enemy('wall.png', 674, 416, window, 5, self.extra_vars[3])"], #wave 2 
            [60*41, "enemy_sl('wall.png', -64, 416, window, 5, self.extra_vars[2])"], 
            [60*42, "enemy('wall.png', 674, 416, window, 5, self.extra_vars[3])"], 
            [60*43, "enemy_sl('wall.png', -64, 416, window, 5, self.extra_vars[2])"],
            [60*44, "enemy('wall.png', 674, 416, window, 5, self.extra_vars[3])"], 
            [60*45, "enemy_sl('wall.png', -64, 416, window, 5, self.extra_vars[2])"], 
            [60*61, "enemy_sd('wall.png', -64, 64, window, 5, self.extra_vars[0])"], #minute 2 
            [60*62, "enemy_sl('wall.png', 674,  416, window, 5, self.extra_vars[1])"],
            [60*70, "enemy_sdl('wall.png', 674, 96, window, 5, self.extra_vars[1])"], 
            [60*85, "enemy('wall.png', 674, 416, window, 5, self.extra_vars[3])"], #wave 3 
            [60*86, "enemy_sl('wall.png', -64, 416, window, 5, self.extra_vars[2])"], 
            [60*87, "enemy('wall.png', 674, 416, window, 5, self.extra_vars[3])"], 
            [60*88, "enemy_sl('wall.png', -64, 416, window, 5, self.extra_vars[2])"],
            [60*89, "enemy('wall.png', 674, 416, window, 5, self.extra_vars[3])"], 
            [60*90, "enemy_sd('wall.png', -64, 64, window, 5, self.extra_vars[0])"], 
            [60*110, "enemy('wall.png', -64, 416, window, 5, self.extra_vars[0])"], 
            [60*100, "enemy_sl('wall.png', 674, 416, window, 5, self.extra_vars[1])"] 
        ] 
        #array for extra vars to get passed to the map handler 
        extra_vars = [enemy_spawner_path, enemy_paths]
        #actaul map to play on 
        battle_map = [ 
            #base platforms 
            "wall('wall.png', 0, 448, window)",
            "wall('wall.png', 32, 448, window)",
            "wall('wall.png', 64, 448, window)",
            "wall('wall.png', 96, 448, window)",
            "wall('wall.png', 128, 448, window)",
            "wall('wall.png', 160, 448, window)",
            "wall('wall.png', 192, 448, window)",
            "wall('wall.png', 224, 448, window)",
            "wall('wall.png', 256, 448, window)",
            "wall('wall.png', 288, 448, window)",
            "wall('wall.png', 320, 448, window)",
            "wall('wall.png', 352, 448, window)",
            "wall('wall.png', 384, 448, window)",
            "wall('wall.png', 416, 448, window)",
            "wall('wall.png', 448, 448, window)",
            "wall('wall.png', 480, 448, window)",
            "wall('wall.png', 512, 448, window)",
            "wall('wall.png', 544, 448, window)",
            "wall('wall.png', 576, 448, window)",
            "wall('wall.png', 608, 448, window)",
            "wall('wall.png', 640, 448, window)",
            "wall('wall.png', 672, 448, window)", 
            "wall('wall.png', 704, 0, window)",
            "wall('wall.png', 704, 32, window)",
            "wall('wall.png', 704, 64, window)",
            "wall('wall.png', 704, 96, window)",
            "wall('wall.png', 704, 128, window)",
            "wall('wall.png', 704, 160, window)",
            "wall('wall.png', 704, 192, window)",
            "wall('wall.png', 704, 224, window)",
            "wall('wall.png', 704, 256, window)",
            "wall('wall.png', 704, 288, window)",
            "wall('wall.png', 704, 320, window)",
            "wall('wall.png', 704, 352, window)",
            "wall('wall.png', 704, 384, window)",
            "wall('wall.png', 704, 416, window)",
            "wall('wall.png', 704, 448, window)", 
            "wall('wall.png', -32, 448, window)", 
            "wall('wall.png', -64, 0, window)",
            "wall('wall.png',-64, 32, window)",
            "wall('wall.png', -64, 64, window)",
            "wall('wall.png', -64, 96, window)",
            "wall('wall.png', -64, 128, window)",
            "wall('wall.png', -64, 160, window)",
            "wall('wall.png', -64, 192, window)",
            "wall('wall.png', -64, 224, window)",
            "wall('wall.png', -64, 256, window)",
            "wall('wall.png', -64, 288, window)",
            "wall('wall.png', -64, 320, window)",
            "wall('wall.png', -64, 352, window)",
            "wall('wall.png', -64, 384, window)",
            "wall('wall.png', -64, 416, window)",
            "wall('wall.png', -64, 448, window)", 
            #left platform 
            "wall('wall.png', 128, 288, window)", 
            "wall('wall.png', 96, 288, window)", 
            #right platform 
            "wall('wall.png', 512, 288, window)", 
            "wall('wall.png', 544, 288, window)", 
            #middle platform 
            "wall('wall.png', 320, 240, window)", 
            "wall('wall.png', 288, 240, window)", 
            #game play objects 
            "enemy_spawner(extra_vars[0], window, extra_vars[1])", 
            "protect_square('square.png', 272, 352, window, 15)", 
            "player('player.png', 0, 0, window)"
        ]
        map_use_player = map_game(battle_map) 
        map_use_player.read_map(lis_ins, window, extra_vars) #we pass in the extra variable as our extra var and stuff 
    
class results(obj): 
    def __init__(self, sprite_image,window_to_draw, points, high_points, win): 
        obj.__init__(self, sprite_image, 0, 0, True, False, window_to_draw) 
        self.points = points 
        self.high_points = high_points 
        self.font_draw = pygame.font.Font("fontgame.ttf", 50) 
        self.done = False 
        self.prompt_restart_game = False 
        self.release_z = False 
        self.grace = 30 
        self.win = win
        self.inputarray = ["current_instance.instance_code(lis_ins, input_array);current_instance.instance_draw()"] 

    def instance_code(self, lis_ins, inputs): 
        #check for Z being pressed down
        if inputs[4] == 1 and self.release_z and self.grace <= 0: 
            #restart game 
            if self.prompt_restart_game == True: 
                lis_ins.pop(0) #kill self 
                #re create logic controller 
                lis_ins.append(logic_controller(self.window_to_draw)) 
            #set the prompt restart flag to true basically 
            self.prompt_restart_game = True 

        if inputs[4]: 
            self.release_z = False 
        else: 
            self.release_z = True 

        if self.grace > 0: self.grace -= 1 

    def instance_draw(self): 
        if self.win: 
            colour = (0,0,0) 
        else: 
            colour = (255,255,255)
        self.window_to_draw.blit(self.sprite, (0, 0))
        score_draw = self.font_draw.render(str(self.high_points), False, colour) 
        self.window_to_draw.blit(score_draw, (500, 110)) 
        score_draw = self.font_draw.render(str(self.points), False, colour) 
        self.window_to_draw.blit(score_draw, (500, 30)) 
        if self.prompt_restart_game: 
            pygame.draw.rect(self.window_to_draw, (0, 0, 0), (0, 0, 640, 480)) 
            restart_message = self.font_draw.render("PRESS Z TO RETURN TO THE MENU", False, (255, 255, 255)) 
            self.window_to_draw.blit(restart_message, (5, 480 / 2)) 

class enemy(obj): 
    def __init__(self, sprite_image, x, y, window_to_draw, health, path): 
        obj.__init__(self, sprite_image, x, y, True, False, window_to_draw) 
        self.health = health * 2 #because we check for collsion 2 times and I am to lazy to edit the code 
        self.path = path 
        self.path_step = 0 
        self.counter = 0 
        self.last_executed = 0 
        self.new_step_frame = True 
        self.attack_counter = 0 #it should go to roughly 180 
        self.bullet_cool_down = 60 
        self.frame = 0
        self.frame_fps = 0 
        self.flip = False 
        self.name = "enemy" 
        self.inputarray = ["current_instance.instance_code(lis_ins);current_instance.instance_draw()"] 

    def instance_code(self, lis_ins): 
        if self.frozen != True: 
            #check for bullets 
            for i in lis_ins: 
                if i.name == "bullet": 
                    if i.enemy == True: 
                        if self.colliding(self.x, self.y, i) == True: 
                            self.health -= 1 
                            i.returnarray[1] = 1 

                        if self.colliding(self.x, self.y, i) == True: 
                            self.health -= 1 
                            i.returnarray[1] = 1

            #end life
            if self.health <= 0: 
                lis_ins[0].points += 100 
                self.returnarray[1] = 1 

            #path 
            if self.path_step + 1 <= len(self.path): 
                current_step = self.path[self.path_step] 
                if current_step[0] == self.counter: 
                    if current_step[1] == 'hm': 
                        self.last_executed = 1 
                        self.hmove(current_step[2]) 
                    elif current_step[1] == 'vm': 
                        self.last_executed = 2 
                        self.vmove(current_step[2]) 
                    elif current_step[1] == 'attack': 
                        self.last_executed = 3  
                        self.attack(lis_ins) 
                    self.path_step += 1 
                    self.new_step_frame = True 

            if self.new_step_frame == False: 
                if self.last_executed == 1: 
                    self.hmove(current_step[2]) 
                elif self.last_executed == 2: 
                    self.vmove(current_step[2]) 
                elif self.last_executed == 3: 
                    self.attack(lis_ins) 

            self.counter += 1 
            self.new_step_frame = False

            #animation 
            self.animate()

            #update collision 
            self.update_collision() 

    def instance_draw(self): 
        if self.visible == True: 
            self.window_to_draw.blit(pygame.transform.flip(self.sprite, self.flip, False), (self.x, self.y)) 

    def animate(self): 
        #60 / 30 = 2 
        if self.frame_fps >= 2: 
            if self.frame == 0: 
                #set next frame 
                self.frame = 1 
                #load sprite 
                self.sprite = pygame.image.load("en.png") 
            elif self.frame == 1: 
                self.frame = 0  
                self.sprite = pygame.image.load("enwalk.png") 
            #reset fps counter 
            self.frame_fps = -1 
        #add fps counter 
        self.frame_fps += 1 

    def hmove(self, speed): 
        self.x += int(speed)

    def vmove(self, speed): 
        self.y += int(speed) 

    def attack(self, lis_ins): 
        self.attack_counter += 1 
        #right move 
        if self.attack_counter <= 60: 
            self.x += 1 
        #left move 
        elif self.attack_counter > 60 and self.attack_counter <= 120: 
            self.x -= 1 
        #attack
        elif self.attack_counter > 120: 
            self.frame = 0
            self.bullet_cool_down -= 1 
            if self.bullet_cool_down == 30 or self.bullet_cool_down == 0: 
                lis_ins.append(fire(self.x, self.y, self.window_to_draw, 8, 0, ["wall"], False)) 
        
        #reset variables
        if self.attack_counter >= 180: 
            self.attack_counter = 0 
            self.bullet_cool_down = 60 

class enemy_sl(enemy): 
    def __init__(self, sprite_image, x, y, window_to_draw, health, path): 
        enemy.__init__(self, sprite_image, x, y, window_to_draw, health, path) 
        self.flip = True 
    
    def attack(self, lis_ins): 
        self.attack_counter += 1 
        #right move 
        if self.attack_counter <= 60:
            self.x += 1 
        #left move 
        elif self.attack_counter > 60 and self.attack_counter <= 120: 
            self.x -= 1 
        #attack
        elif self.attack_counter > 120: 
            self.frame = 0
            self.bullet_cool_down -= 1 
            if self.bullet_cool_down == 30 or self.bullet_cool_down == 0: 
                lis_ins.append(fire(self.x, self.y, self.window_to_draw, -8, 0, ["wall"], False)) 
        
        #reset variables
        if self.attack_counter >= 180: 
            self.attack_counter = 0 
            self.bullet_cool_down = 60 

class enemy_sd(enemy): 
    def __init__(self, sprite_image, x, y, window_to_draw, health, path): 
        enemy.__init__(self, sprite_image, x, y, window_to_draw, health, path)
    
    def attack(self, lis_ins): 
        self.attack_counter += 1 
        #right move 
        if self.attack_counter <= 60:
            self.x += 1 
        #left move 
        elif self.attack_counter > 60 and self.attack_counter <= 120: 
            self.x -= 1 
        #attack
        elif self.attack_counter > 120: 
            self.bullet_cool_down -= 1 
            if self.bullet_cool_down == 30 or self.bullet_cool_down == 0: 
                lis_ins.append(fire(self.x, self.y, self.window_to_draw, 5, 13, ["wall"], False)) 
        
        #reset variables
        if self.attack_counter >= 180: 
            self.attack_counter = 0 
            self.bullet_cool_down = 60 

    def animate(self): 
        #60 / 30 = 2 
        if self.frame_fps >= 2: 
            if self.frame == 0: 
                #set next frame 
                self.frame = 1 
                #load sprite 
                self.sprite = pygame.image.load("flyen.png") 
            elif self.frame == 1: 
                self.frame = 0  
                self.sprite = pygame.image.load("flyenup.png") 
            #reset fps counter 
            self.frame_fps = -1 
        #add fps counter 
        self.frame_fps += 1 

class enemy_sdl(enemy): 
    def __init__(self, sprite_image, x, y, window_to_draw, health, path): 
        enemy.__init__(self, sprite_image, x, y, window_to_draw, health, path) 
        self.flip = True
    
    def attack(self, lis_ins): 
        self.attack_counter += 1 
        #right move 
        if self.attack_counter <= 60:
            self.x += 1 
        #left move 
        elif self.attack_counter > 60 and self.attack_counter <= 120: 
            self.x -= 1 
        #attack
        elif self.attack_counter > 120: 
            self.bullet_cool_down -= 1 
            if self.bullet_cool_down == 30 or self.bullet_cool_down == 0: 
                lis_ins.append(fire(self.x, self.y, self.window_to_draw, -5, 13, ["wall"], False)) 
        
        #reset variables
        if self.attack_counter >= 180: 
            self.attack_counter = 0 
            self.bullet_cool_down = 60 

    def animate(self): 
        #60 / 30 = 2 
        if self.frame_fps >= 2: 
            if self.frame == 0: 
                #set next frame 
                self.frame = 1 
                #load sprite 
                self.sprite = pygame.image.load("flyen.png") 
            elif self.frame == 1: 
                self.frame = 0  
                self.sprite = pygame.image.load("flyenup.png") 
            #reset fps counter 
            self.frame_fps = -1 
        #add fps counter 
        self.frame_fps += 1 