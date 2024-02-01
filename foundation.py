try: 
    import pygame 
except: 
    print("ERROR YOU NEED PYGAME INSTALL") 
    exit(1)

try: 
    from classes import logic_controller 
except: 
    print('ERROR "classes.py" IS CORRUPTED OR MISSING') 
    exit(1) 

### BEGINING ### 

#init base requirements 
def init_window(): 
    pygame.init() 
    pygame.display.set_caption("Protector") 
    global window 
    window = pygame.display.set_mode((640, 480)) 
    global run 
    run = True 
    global lis_ins 
    lis_ins = [] 

#set the fps 
def set_fps(frames_per_second): 
    global fps 
    fps = frames_per_second 
    global fpsclock 
    fpsclock = pygame.time.Clock() 

#initalize input stuff 
def init_input_vars(): 
    global input_array 
    input_array = [0, 0, 0, 0, 0] 
    #left right up down Z  

### FINALIZE INITALIZING ### 

#begin the game 
def initalize(): 
    #initialize the window and global varibles 
    init_window() 
    set_fps(60) 
    init_input_vars()
    lis_ins.append(logic_controller(window)) 

### GAME LOOP FUNCTIONS ### 

#get input from the user 

def input_obtain(ce):  
    global input_array 
    if ce.type == pygame.KEYDOWN: 
        if ce.key == pygame.K_LEFT: input_array[0] = 1
        if ce.key == pygame.K_RIGHT: input_array[1] = 1 
        if ce.key == pygame.K_DOWN: input_array[2] = 1
        if ce.key == pygame.K_UP: input_array[3] = 1 
        if ce.key == pygame.K_z: input_array[4] = 1  
    if ce.type == pygame.KEYUP: 
        if ce.key == pygame.K_LEFT: input_array[0] = 0
        if ce.key == pygame.K_RIGHT: input_array[1] = 0 
        if ce.key == pygame.K_DOWN: input_array[2] = 0
        if ce.key == pygame.K_UP: input_array[3] = 0 
        if ce.key == pygame.K_z: input_array[4] = 0 

#manage instances
def instance_manager(): 
    global lis_ins 
    for current_instance in lis_ins: 
        #save every thing which is needed 
        before_return = current_instance.instance_pre() 

        #execute what the object passes us 
        exec(before_return[0]) 

        #save all the extra data 
        after_return = current_instance.instance_done() 

        #execute what the object passes us again 
        exec(after_return[0])

        #act based on every thing given 
        if after_return[1] == 1: 
            lis_ins.remove(current_instance) #destroy 


### UPDATE THE GAME ### 

#update the game 
def update_game(): 
    #basic game logic updates 
    for cur_ev in pygame.event.get(): 
        #quiting 
        if cur_ev.type == pygame.QUIT: 
            global run 
            run = False 
        #input checking 
        input_obtain(cur_ev) 
    #update the window and go tick foward the fps 
    instance_manager() 
    pygame.display.update() 
    global fps 
    fpsclock.tick(fps) 
    window.fill([0, 0, 100]) 

### BEGIN GAME ### 

initalize() 

while run == True: 
    update_game() 

pygame.quit() 