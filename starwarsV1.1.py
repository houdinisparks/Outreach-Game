#batman is the best
from collections import deque
import pygame, ezpztext
import time
import random
import threading
import traceback
import pygame
import os
import sys
from pygame import *
from pygame.locals import *

from Movement import Movement
from Hole import Hole
from Timer import Timer
import ParserThread

pygame.init()

level = 6
numOfLevels = 9
rebelScore = 0

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0, 255, 0)
yellow = (255, 255, 0)
grey = (96, 125, 139)
orange = (255,87,34)

# default colour for text editor font
txtfont_default = white
txtfont_focus = green

# Global settings
control_mode = 'TYPE' # 'KEYPRESS' or 'TYPE'
time_limit = 50 # Time limit that affects Time Bar and Duration countdown

# Use a timer
timer = Timer()

# Use the Movement class to keep track of movements
movement = Movement(1)

# Game state
game_state = 'idle'
parsing = False

#textbox
txtbx = ezpztext.Textbox(lines=14, default_color=txtfont_default,
            focus_color=txtfont_focus, maxlength=28, y=60, x=840)

for i in range(len(txtbx.txtbx)):
    txtbx.txtbx[i].prompt = "{:>2}: ".format(i + 1)

# Use ParserThread to create a separate thread for parsing user code
parser_thread = ParserThread.Thread()

map_width = 800
map_height = 600
status_bar = 40
display_width = map_width +400
display_height = map_height + status_bar

lead_x = 750
lead_y = 540
lead_direction = 'down'
blueprintCollected = False
rebelScore = 0

BlueprintThickness = 30
block_size = 10
FPS = 30
gameDisplay = pygame.display.set_mode((display_width,display_height),RESIZABLE)
pygame.display.set_caption('Star Wars: A programming education game')

wallpaper_img = 'wallpaper/Wallpaper.png'
text_editor_img = 'pictures/right panel/Text editor.png'

map_img = ['pictures/Map/warm_up.png',
           'pictures/Map/Map_0.png','pictures/Map/Map_4.png','pictures/Map/Balcony_map.png',
           'pictures/Map/Map_1.png','pictures/Map/Map_2.png','pictures/Map/Map_3.png',
           'pictures/Map/Map_5.png','pictures/Map/docking_bay.png']

lukeUpStationary = pygame.image.load('pictures/lukeMove/Luke_up_stationary.png')
lukeUpWalk1 = pygame.image.load('pictures/lukeMove/Luke_up_walk_1.png')
lukeUpWalk2 = pygame.image.load('pictures/lukeMove/Luke_up_walk_2.png')
lukeDownStationary = pygame.image.load('pictures/lukeMove/Luke_down_stationary.png')
lukeDownWalk1 = pygame.image.load('pictures/lukeMove/Luke_down_walk_1.png')
lukeDownWalk2 = pygame.image.load('pictures/lukeMove/Luke_down_walk_2.png')
lukeRightStationary = pygame.image.load('pictures/lukeMove/Luke_right_stationary.png')
lukeRightWalk = pygame.image.load('pictures/lukeMove/Luke_right_walk_1.png')
lukeLeftStationary = pygame.image.load('pictures/lukeMove/Luke_left_stationary.png')
lukeLeftWalk = pygame.image.load('pictures/lukeMove/Luke_left_walk_1.png')

reyUpStationary = pygame.image.load('pictures/reyMove/Rey_up_stationary.png')
reyUpWalk1 = pygame.image.load('pictures/reyMove/Rey_up_walk_1.png')
reyUpWalk2 = pygame.image.load('pictures/reyMove/Rey_up_walk_2.png')
reyDownStationary = pygame.image.load('pictures/reyMove/Rey_down_stationary.png')
reyDownWalk1 = pygame.image.load('pictures/reyMove/Rey_down_walk_1.png')
reyDownWalk2 = pygame.image.load('pictures/reyMove/Rey_down_walk_2.png')
reyRightStationary = pygame.image.load('pictures/reyMove/Rey_right_stationary.png')
reyRightWalk1 = pygame.image.load('pictures/reyMove/Rey_right_walk_1.png')
reyRightWalk2 = pygame.image.load('pictures/reyMove/Rey_right_walk_2.png')
reyLeftStationary = pygame.image.load('pictures/reyMove/Rey_left_walk_1.png')
reyLeftWalk1 = pygame.image.load('pictures/reyMove/Rey_left_walk_1.png')
reyLeftWalk2 = pygame.image.load('pictures/reyMove/Rey_left_walk_2.png')

finnUpStationary = pygame.image.load('pictures/finnMove/Finn_up_stationary.png')
finnUpWalk1 = pygame.image.load('pictures/finnMove/Finn_up_walk_1.png')
finnUpWalk2 = pygame.image.load('pictures/finnMove/Finn_up_walk_2.png')
finnDownStationary = pygame.image.load('pictures/finnMove/Finn_down_stationary.png')
finnDownWalk1 = pygame.image.load('pictures/finnMove/Finn_down_walk_1.png')
finnDownWalk2 = pygame.image.load('pictures/finnMove/Finn_down_walk_2.png')
finnRightStationary = pygame.image.load('pictures/finnMove/Finn_right_stationary.png')
finnRightWalk1 = pygame.image.load('pictures/finnMove/Finn_right_walk_1.png')
finnRightWalk2 = pygame.image.load('pictures/finnMove/Finn_right_walk_2.png')
finnLeftStationary = pygame.image.load('pictures/finnMove/Finn_left_stationary.png')
finnLeftWalk1 = pygame.image.load('pictures/finnMove/Finn_left_walk_1.png')
finnLeftWalk2 = pygame.image.load('pictures/finnMove/Finn_left_walk_2.png')

darthUpStationary = pygame.image.load('pictures/darthMove/Darth_up.png')
darthDownStationary = pygame.image.load('pictures/darthMove/Darth_down.png')
darthRightStationary = pygame.image.load('pictures/darthMove/Darth_right.png')
darthLeftStationary = pygame.image.load('pictures/darthMove/Darth_left.png')

mFalconStationary = pygame.image.load('pictures/milleniumFalcon/mFalcon_stationary.png')
mFalconThrusterSmall = pygame.image.load('pictures/milleniumFalcon/mFalcon_thruster_small.png')
mFalconThrusterBig = pygame.image.load('pictures/milleniumFalcon/mFalcon_thruster_big.png')

reyMoveUp = [reyUpWalk1, reyUpWalk2, reyUpStationary]
reyMoveDown = [reyDownWalk1, reyDownWalk2, reyDownStationary]
reyMoveRight = [reyRightWalk1, reyRightWalk2, reyRightStationary]
reyMoveLeft = [reyLeftWalk1, reyLeftWalk2, reyLeftStationary]

lukeMoveUp = [lukeUpWalk1, lukeUpWalk2, lukeUpStationary]
lukeMoveDown = [lukeDownWalk1, lukeDownWalk2, lukeDownStationary]
lukeMoveRight = [lukeRightStationary, lukeRightWalk, lukeRightStationary]
lukeMoveLeft = [lukeLeftStationary, lukeLeftWalk, lukeLeftStationary]

finnMoveUp = [finnUpWalk1, finnUpWalk2, finnUpStationary]
finnMoveDown = [finnDownWalk1, finnDownWalk2, finnDownStationary]
finnMoveRight = [finnRightWalk1, finnRightWalk2, finnRightStationary]
finnMoveLeft = [finnLeftWalk1, finnLeftWalk2, finnLeftStationary]

mFalconFireUp = [mFalconStationary, mFalconThrusterSmall, mFalconStationary, mFalconThrusterSmall,
                 mFalconThrusterBig, mFalconStationary, mFalconThrusterSmall, mFalconThrusterBig,
                 mFalconThrusterSmall, mFalconThrusterBig, mFalconThrusterBig, mFalconThrusterBig]
blueprint_img = pygame.image.load('pictures/Blueprint.png')

# holes
holes = [Hole(gameDisplay, (750, 420)),
         Hole(gameDisplay, (630, 420))]

# for run button
btnimg = pygame.image.load('pictures/runbtn.png').convert_alpha()
btn_rect = pygame.Rect(1075, 590, *btnimg.get_rect().size)

clock = pygame.time.Clock()

smallfont = pygame.font.Font('diehund.ttf', 28)
medfont = pygame.font.Font('diehund.ttf', 50)
largefont = pygame.font.Font('diehund.ttf', 80)

#sound fxps
#---BGM
bgm1 = "sounds/bgm1-throneroom.ogg"
bgm1loop = "sounds/bgm1-throneroomloop.ogg"
bgm2 = "sounds/bgm2-intothetrap.ogg"
bgm2loop = "sounds/bgm2-intothetraploop.ogg"
bgm3 = "sounds/bgm3-countdooku.ogg"
bgm3loop = "sounds/bgm3-countdookuloop.ogg"
bgm4 = "sounds/bgm4-duelofthefates.ogg"
bgm4loop = "sounds/bgm4-duelofthefatesloop.ogg"

fall = pygame.mixer.Sound("sounds/fall1.ogg")
bangwall = pygame.mixer.Sound("sounds/bangwall1.ogg")    #done
collectblueprint= pygame.mixer.Sound("sounds/collectblueprint1.ogg")
jump1 = pygame.mixer.Sound("sounds/jump1.ogg")
startGame = pygame.mixer.Sound("sounds/start.ogg")
wallbang = pygame.mixer.Sound("sounds/bang1.ogg")
dvlist = ["sounds/darth vader - die1.wav","sounds/darth vader - i have you now.wav","sounds/darth vaer - breath.wav","sounds/darth vader - thisistheend.wav"]


BEGIN_LOOP = pygame.USEREVENT + 1

def loadLevel(level):
    position=[[360,570],[180,180],[0,450],[30,270],[750,540],[360,30],[420,30],[60,330],[30,270]]
    levelXList = [[510,0,0],[0,180,360,180,360,600,360,450],[0,120,270,420,690,540,390,240,0],
                  [0,0,0,30,780,780],[0,30,780,0,420,180,510,180,300,420,510,30,180,510,630],[0,0,60,390],
             [0,0,270,330,360,450,450,450,450,450,750],
             [0,0,360,600,240,480,720,0,0],[0,0,0,30]]
    levelYList = [[360,0,180],[0,0,120,450,390,0,240,0],[0,0,0,0,0,150,270,390,510],[0,30,300,570,30,300],
                  [0,570,0,0,0,480,480,30,30,60,60,210,180,180,210],
                  [0,90,270,0],
                  [0,90,120,120,240,0,120,270,420,540,60],
                  [0,180,180,180,270,270,240,390,300],[0,60,300,570]]
    widthlist = [[300,810,270],[180,240,60,630,450,210,240,150],
                 [120,150,150,150,120,150,150,150,240],[600,30,30,780,30,30],
                 [30,780,30,390,780,120,120,120,90,90,120,150,120,120,180],
                 [360,60,300,420],
                 [420,240,60,90,60,360,270,180,270,360,60],
                 [810,180,60,60,60,60,90,810,60],[810,30,30,780]]
    heightlist=[[240,180,420],[600,120,60,150,60,390,90,180],
                [420,300,180,60,600,450,330,210,90],[60,240,270,30,240,270],
                [600,30,570,60,60,90,90,120,90,60,90,120,210,210,120],
                [90,510,330,600],
                [90,390,360,90,360,90,90,90,90,60,480],
                [180,120,120,120,120,120,150,210,90],[60,210,300,30]]
    win_width = [30,30,120,30,30,30,30,30,30]
    win_height = [240,30,30,30,30,30,30,60,510]
    win_xyCoordinates = [[780,180],[420,0],[570,0],[780,270],[390,0],[360,570],
                         [420,570],[780,180],[780,60]]
    holeCoords = [[],[[570,180],[570,210]],[],[[390,0],[390,30],[390,60],[390,90],[390,120],[390,150],[390,180],[390,210],[390,240],[390,270]
                                               ,[390,300],[390,330],[390,360],[390,390],[390,420],[390,450],[390,480],[390,510],[390,540],[390,570]]
                  ,[],[[260,150]],[],[],[[180,210],[180,240],[210,450],[210,480],[210,510],[360,270],[360,270],[360,270],[360,300],[360,330],[570,150],
                                [570,180],[570,210],[510,390],[510,420]]]
    vader_face = [0,0,1,0,0,0,1,1] # 0-Down, 1-Left, 2- Up, 3-Right
    return [position[level][0],position[level][1],levelXList[level],levelYList[level],widthlist[level],heightlist[level],win_width[level],win_height[level], win_xyCoordinates[level][0],win_xyCoordinates[level][1],holeCoords[level], vader_face[level]]

def done_moving():
    if movement.get_next_move() == 'stationary':
        return True
    return False

def move(direction, steps):
    global game_state
    game_state = direction

    while True:
        if game_state == 'gameover':
            game_state = 'idle' # reset game_state
        if game_state == 'idle':
            steps -= 1
            if steps <= 0: break
            game_state = direction

moveUp = lambda steps = 1: move('move_up', steps)
moveDown = lambda steps = 1: move('move_down', steps)
moveLeft = lambda steps = 1: move('move_left', steps)
moveRight = lambda steps = 1: move('move_right', steps)

jumpUp = lambda steps = 1: move('jump_up', steps)
jumpDown = lambda steps = 1: move('jump_down', steps)
jumpLeft = lambda steps = 1: move('jump_left', steps)
jumpRight = lambda steps = 1: move('jump_right', steps)

def holeInFront():
    for hole in holes:
        player_rect = pygame.Rect(lead_x, lead_y, 30, 30)
        collide_direction = hole.collides(player_rect)
        print (player_rect)
        print 'psuedo_holes', collide_direction
        print 'lead_direction', lead_direction
        # if lead_direction == collide_direction: return True
        if lead_direction == collide_direction:
            print True
            return True
    print False
    return False

def parser_func(code):
    global game_state
    try:
        exec(code)
    except SystemExit:
        print "exit from loop."
    except:
        traceback.print_exc()
        game_state = 'error'
    finally:
        parsing = False

def display_error():
    global game_state
    paused = True
    message_to_screen("Your code has an error.", red, -100, size = "medium")
    message_to_screen("Press c to restart", red, 0, size = "medium")
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

    clock.tick(5)
    game_state = 'idle'
    gameLoop()


def barrier(xlocation,ylocation, barrier_width, barrier_height):
    pygame.draw.rect(gameDisplay,black, [xlocation, ylocation, barrier_width, barrier_height])

def pause():
    paused = True
    message_to_screen("Paused", black, -100, size = "large")
    message_to_screen("Press c to continue", black, 25, size = "small")
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        clock.tick(5)

def helpInstructions(level):
    csmallfont = pygame.font.Font('diehund.ttf', 15)
    csmallfont.set_italic(True);
    
    xsmallfont = pygame.font.Font('diehund.ttf', 15)
    xsmallfont.set_underline(True)
    xsmallfont.set_bold(True)
    gameDisplay.blit(xsmallfont.render("Tips:", True, white),\
                         [835, 375])
    xsmallfont.set_underline(False)
    xsmallfont.set_bold(False)

    # 9 Lines max
    helpMessage = {0 : ["Commands to move your player", # Learn move
                        "c      self.moveUp()",
                        "c      self.moveRight()",
                        "c      self.moveDown()",
                        "c      self.moveLeft()",
                        "",
                        "What happens if you try",
                        "c      n = 15",
                        "c      self.moveRight(n)"],
                   1 : ["Loops can ease your pain of coding", # Learn basic loop
                        "lines of the same thing.",
                        "       x = 0",
                        "       while x < 5 :",
                        "           self.moveRight()",
                        "           self.moveLeft()",
                        "           x = x + 1",
                        "'self' represents the object you are",
                        " controling, in this case the player."],
                   2 : ["The Blue Map earns you points",
                        "",
                        "Here are some useful actions to use", # Learn condition check
                        "       if self.holeInFront() :",
                        "           self.jumpRight()",
                        "",
                        "Don't forget how to use the loops!",
                        "       while x < 5 :",
                        "           self.jumpUp()"],
                   3 : ["If you didn't realize, If and While", # Example conditions 1
                        "statements require conditions.",
                        "",
                        "       x = 0",
                        "       while x < 5 :",
                        "           self.moveUp()",
                        "           if x == 3",
                        "               self.moveLeft()",
                        ""],
                   4 : ["I doubt you can jump over laser",
                        "",
                        "Use less than(<), more than(>) or" # Example conditions 2
                        "equal to(==), within a condition",
                        "check.",
                        "c      while <condtion> :",
                        "c          <do stuff>",
                        "c      if <condition> :",
                        "c          <do stuff>"],
                   5 : ["Let's see how quickly you can get", # Test!
                        "this over and done with",
                        "",
                        "c      x = <value>",
                        "c      while <condtion> :",
                        "c          <do stuff>",
                        "c      if <condition> :",
                        "c          <do stuff>",
                        ""],
                   6 : ["Condtitions result in either True",
                        "or False.",
                        "Try assigning 'True' as the x value",
                        "",
                        "c      x = <value>",
                        "c      while <condtion> :",
                        "c          <do stuff>",
                        "c      if <condition> :",
                        "c          <do stuff>"],
                   7 : ["You may have heard of an infinite",
                        "loop. 'break' is your friend, but",
                        "where is it used?",
                        "",
                        "c      x = <value>",
                        "c      while <condtion> :",
                        "c          <do stuff>",
                        "c      if <condition> :",
                        "c          <do stuff>"]}
    for lineNumber in range(len(helpMessage[level])):
        isCode = False
        if len(helpMessage[level][lineNumber]) > 0:
            if helpMessage[level][lineNumber][0] == 'c':
                helpMessage[level][lineNumber] = helpMessage[level][lineNumber][1:];
                isCode = True;

        if isCode:
            gameDisplay.blit(csmallfont.render(helpMessage[level][lineNumber], True, grey),\
                             [835, 395+lineNumber*xsmallfont.get_linesize()])
        else:
            gameDisplay.blit(xsmallfont.render(helpMessage[level][lineNumber], True, white),\
                             [835, 395+lineNumber*xsmallfont.get_linesize()])


def status(score,set_time,elapse_time):
    text = smallfont.render("Score: " + str(score), True, black)
    gameDisplay.blit(text,[15,map_height])

    if(elapse_time>set_time):
        elapse_time=set_time
    pygame.draw.rect(gameDisplay,red, [map_width/2, map_height+2, map_width*(set_time-elapse_time)/(2*set_time), status_bar])
    pygame.draw.line(gameDisplay,black,(map_width/2-2,map_height),(map_width/2-2,display_height), 4)
    text2 = smallfont.render("Time left", True, black)
    gameDisplay.blit(text2,[3*map_width/4-15,map_height])

def randBlueprintGen():
    randBlueprintX = 120
    randBlueprintY = 150
    return randBlueprintX, randBlueprintY

#----Sounds method for choosing which bgm to load-----------#
def loadBGM(level):
    loadList = []
    
    if level == 1 or level == 2 or level == 0:
        loadList = [bgm1,bgm1loop]
        
    elif level == 3 or level == 4:
        loadList = [bgm2,bgm2loop]

    elif level == 5 or level == 6 or level == 7:
        loadList = [bgm3, bgm3loop]
        
    elif level == 8 or level == 9:
        loadList = [bgm4, bgm4loop]
        
    else:
        print "no sound loaded."

    return loadList

def game_intro():
    global characterMove
    pygame.mixer.music.load("sounds/intro - star wars main theme.ogg")
    pygame.mixer.music.play(0)
    intro = True

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    startGame.play()
                    characterMove = [lukeMoveUp, lukeMoveDown, lukeMoveRight, lukeMoveLeft]
                    intro=False
                if event.key == pygame.K_f:
                    startGame.play()
                    characterMove = [reyMoveUp, reyMoveDown, reyMoveRight, reyMoveLeft]
                    intro=False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(white)
        wp = pygame.image.load(wallpaper_img)
        wp = pygame.transform.scale(wp,(display_width,display_height))
        gameDisplay.blit(wp, (0,0))
        pygame.display.update()
        clock.tick(5)


def rebel_move(direction, playerX, playerY, xChange, yChange, rebelScore, time_limit, seconds, xlocation, ylocation, barrier_width,barrier_height,randBlueprintX, randBlueprintY):

    global game_map
    image = None
    for img in characterMove[direction]:

        playerX += xChange
        playerY += yChange

        gameDisplay.fill(white)
        gameDisplay.blit(game_map, (0,0))
        gameDisplay.blit(text_editor, (map_width,0))
        pygame.draw.line(gameDisplay,black,(map_width,display_height),(map_width,0), 2)#draw boundary for user to type code
        pygame.draw.line(gameDisplay,black,(0,map_height),(map_width,map_height), 2)#draw boundary for status bar
        status(rebelScore, time_limit,seconds)
        #if level one
        game_map=pygame.image.load(map_img[level]);

        if blueprintCollected == False:
            #barrier(xlocation, randomHeight, barrier_width)
            gameDisplay.blit(blueprint_img, (randBlueprintX, randBlueprintY))


##            holes[0].draw()
##            holes[1].draw()
        gameDisplay.blit(btnimg, btn_rect)
        gameDisplay.blit(img, (playerX, playerY))
        draw_holes()


        image = img

        txtbx.draw(gameDisplay)
        helpInstructions(level)
        pygame.display.update()
        clock.tick(10)

    return playerX, playerY, image


def rebel_jump(direction, playerX, playerY, xChange, yChange, rebelScore, time_limit, seconds, xlocation, ylocation, barrier_width,barrier_height,randBlueprintX, randBlueprintY):

    global game_map
    image = None

    img = characterMove[direction][-1] # get stationary img

    for j in range(6):

        playerX += xChange

        if direction == 2 or direction == 3:
            if j < 3:
                playerY -= abs(xChange)
            else:
                playerY += abs(xChange)
        elif direction == 0:
            if j < 4:
                playerY -= int(1.7*abs(yChange))
            else:
                playerY += int(0.4*abs(yChange))
        elif direction == 1:
            if j < 2:
                playerY -= int(0.4*abs(yChange))
            else:
                playerY += int(1.7*abs(yChange))

        gameDisplay.fill(white)
        gameDisplay.blit(game_map, (0,0))
        gameDisplay.blit(text_editor, (map_width,0))
        pygame.draw.line(gameDisplay,black,(map_width,display_height),(map_width,0), 2)#draw boundary for user to type code
        pygame.draw.line(gameDisplay,black,(0,map_height),(map_width,map_height), 2)#draw boundary for status bar
        status(rebelScore, time_limit,seconds)
        #if level one
        game_map=pygame.image.load(map_img[level]);

        if blueprintCollected == False:
            #barrier(xlocation, randomHeight, barrier_width)
            gameDisplay.blit(blueprint_img, (randBlueprintX, randBlueprintY))

        #for checking hole position
##            for hole in holes:
##                hole.draw()
        gameDisplay.blit(btnimg, btn_rect)
        gameDisplay.blit(img, (playerX, playerY))
        draw_holes()

        image = img

        txtbx.draw(gameDisplay)
        helpInstructions(level)
        pygame.display.update()
        clock.tick(15)

    return playerX, playerY, image


def mfalcon_fly(mFalconX, mFalconY, rebelScore, time_limit, seconds, randBlueprintX, randBlueprintY):

    global game_map

    # millenium falcon initial coordinates: 570, 225

    for i in range(len(mFalconFireUp) + 25):

        if i > 11:
            index = 11
            mFalconX += 10
        else:
            index = i

        for j in range(2):
            gameDisplay.fill(white)
            gameDisplay.blit(game_map, (0,0))
            gameDisplay.blit(mFalconFireUp[index], (mFalconX, mFalconY))
            gameDisplay.blit(text_editor, (map_width,0))
            pygame.draw.line(gameDisplay,black,(map_width,display_height),(map_width,0), 2)#draw boundary for user to type code
            pygame.draw.line(gameDisplay,black,(0,map_height),(map_width,map_height), 2)#draw boundary for status bar
            status(rebelScore, time_limit,seconds)
            helpInstructions(level)
            #if level one
            game_map=pygame.image.load(map_img[level])

            if not blueprintCollected:
                gameDisplay.blit(blueprint_img, (randBlueprintX, randBlueprintY))
                
            gameDisplay.blit(btnimg, btn_rect)
            draw_holes()

            txtbx.draw(gameDisplay)
            helpInstructions(level)
            pygame.display.update()

            if index != 11:
                clock.tick(10)

def place_random_holes():
    del holes[:]
    possible_locs = range(3, 25, 2)
    vertical_locs = random.randint(6, 12)
    for i in range (8): # number of columns of holes
        x = possible_locs.pop(random.randrange(len(possible_locs)))
        y = random.choice(xrange(6, 12))
        make_hole_columns(x * 30, y * 30, random.choice((2, 3)))

def make_hole_columns(x, y, height):
    for i in range(height):
        holes.append(Hole(gameDisplay, (x, y + (i * 30))))

def draw_holes():
    if level == numOfLevels - 1:
        for hole in holes:
            hole.draw()

def crashed_into_wall(lead_x, lead_y, xlist, ylist, widthlist, heightlist):
    player_rect = pygame.Rect(lead_x, lead_y, 30, 30)
    for i in range(len(xlist)):
        wall = pygame.Rect(xlist[i], ylist[i], widthlist[i], heightlist[i])
        if wall.colliderect(player_rect): return True
        
    return False

def linecount_to_score(n):
    return txtbx.lines - n

def text_objects(text,color,size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg,color, y_displace = 0, size = "small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (map_width / 2), (map_height / 2) + y_displace
    gameDisplay.blit(textSurf, textRect)



def gameLoop():

    global parsing, game_state, text_editor, elemNumber, level,txtbx, game_map, blueprintCollected, characterMove,numOfLevels, rebelScore
    global lead_x, lead_y, lead_direction,holes

    gameWon = False
    gameExit = False
    gameOver = False
    leftCollision = False
    rightCollision = False
    topCollision = False
    bottomCollision = False
    player = characterMove[1][2]

    [lead_x,lead_y,xlist,ylist,widthlist,heightlist,win_width,win_height,win_xlocation,win_ylocation,holeCoords,vadarOrientation] = loadLevel(level)
    
    lead_x_change = 0
    lead_y_change = 0
    randBlueprintX, randBlueprintY = randBlueprintGen()
    step_count = 0
    pause_duration = 0
    code_lines = 0
    movement.reset()

    timerStart=False
    seconds=0

    # use get_ticks to time
    #timer.reset()

    barrier_width = 30
    barrier_height = 30
    xlocation = (map_width/2)+ random.randint(-0.2*map_width, 0.2*map_width)
    ylocation = random.randrange(map_height*0.1,map_height*0.6)

    #----------LOAD BGM-----------#
    beginloop = False
    bgmlist = loadBGM(level)
    print len(bgmlist)
    print bgmlist[0]
    print bgmlist[1]
    pygame.mixer.music.stop() # make sure theres no music playing.
    pygame.mixer.music.load(bgmlist[0])
    pygame.mixer.music.play(0)
    pygame.mixer.music.set_endevent(BEGIN_LOOP)
    
    while not gameExit:
        #Check if bgm has finish playing
               
        event = pygame.mixer.music.get_endevent()
        pygame.mixer.music.queue(bgmlist[1])
                
##        if event == BEGIN_LOOP and beginloop == False:
##                beginloop = True
##                print "loop begins"
##                pygame.mixer.music.load(bgmlist[1]) #load music loop
##                #pygame.mixer.music.play(-1)         #play indefinitely

        if gameWon == True:
            #-----sounds
            pygame.mixer.music.stop()
            pygame.mixer.music.load("sounds/victorybgm.ogg")
            pygame.mixer.music.play(-1)
            #-----sounds
            level = (level+1)%numOfLevels
            message_to_screen("Level cleared!", red,
                              y_displace=-50, size = "large")
            message_to_screen("Press C to proceed", grey,
                              50, size = "small")
            message_to_screen("or Q to quit", grey,
                              100, size = "small")

            rebelScore += linecount_to_score(code_lines)

            pygame.display.update()

        elif gameOver == True:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("sounds/lose - imperial march.ogg")
            pygame.mixer.music.play(-1)
            message_to_screen("Game over", red,
                              y_displace=-50, size = "large")

            message_to_screen("Press C to play again", orange,
                              50, size = "medium")
            message_to_screen("or Q to quit", orange,
                              100, size = "medium")
            #----- displays
            if vadarOrientation == 0:
                gameDisplay.blit(darthDownStationary, (win_xlocation, win_ylocation))
            else:
                gameDisplay.blit(darthLeftStationary, (win_xlocation, win_ylocation))

            pygame.display.update()

        while gameOver == True or gameWon == True:
            game_state = 'gameover'
            parser_thread.stop()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameWon = False
                    gameOver = False
                    gameExit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameWon = False
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        game_state = 'idle'
                        gameWon= False
                        pygame.mixer.music.stop()
                        gameLoop()
                        

    ############## timer ##########################
        if timerStart:
            timer.update()
            seconds = timer.get_time() #calculate how many seconds
            if (time_limit - seconds)<=0:
                randnumb = random.randint(0,len(dvlist)-1)
                #-----sounds
                pygame.mixer.Sound(dvlist[randnumb]).play()
                #-----sounds
                gameOver=True
            #print (seconds) #print how many seconds

###################### WIN GAME CONDITIONS: Lands on the exit grid ###########################
        win_rect = pygame.Rect(win_xlocation, win_ylocation, win_width, win_height)
        player_rect = pygame.Rect(lead_x, lead_y, 30, 30)
        if win_rect.colliderect(player_rect):
            gameWon = True

###################### END GAME CONDITIONS: Out of bound detection, Timelimit ###########################
        if lead_x > map_width - block_size or lead_x < 0 or lead_y > map_height - block_size \
            or lead_y<0:
            gameOver = True

        if game_state == 'error':
            display_error()


####################### UPDATES PLAYER LOCATION ################################
        # lead_x += lead_x_change
        # lead_y += lead_y_change

####################### displaying it on screen ################################
        gameDisplay.fill(white)
        game_map=pygame.image.load(map_img[level])
        text_editor=pygame.image.load(text_editor_img)
        gameDisplay.blit(game_map, (0,0))
        gameDisplay.blit(text_editor, (map_width,0))
        pygame.draw.line(gameDisplay,black,(map_width,display_height),(map_width,0), 2) #draw boundary for user to type code
        pygame.draw.line(gameDisplay,black,(0,map_height),(map_width,map_height), 2) #draw boundary for status bar
        gameDisplay.blit(player, (lead_x, lead_y))
        status(rebelScore, time_limit,seconds)
        helpInstructions(level)


####################### barrier collision detection #############################

        for i in range(0,len(xlist)):
            ylocation = ylist[i]
            xlocation = xlist[i]
            barrier_height = heightlist[i]
            barrier_width = widthlist[i]
            #for debugging:
            #pygame.draw.rect(gameDisplay,red,[xlocation,ylocation,barrier_width,barrier_height])
            if ylocation + barrier_height > lead_y and lead_y + block_size > ylocation:
                if lead_x - (block_size/2) < xlocation + barrier_width and lead_x > xlocation + barrier_width/2:
                    leftCollision = True
                if lead_x + (4*block_size) > xlocation and lead_x < xlocation + barrier_width/2:
                    rightCollision = True
            elif xlocation + barrier_width > lead_x and lead_x + block_size > xlocation:
                if lead_y - (block_size/2) < ylocation + barrier_height and lead_y > ylocation + barrier_height/2:
                    topCollision = True
                if lead_y + (4*block_size) > ylocation and lead_y < ylocation + barrier_height/2:
                    bottomCollision = True




######################## when apple have been collected ###########################
        if blueprintCollected == False:
            gameDisplay.blit(blueprint_img, (randBlueprintX, randBlueprintY))
            if lead_x >= randBlueprintX and lead_x <= randBlueprintX + BlueprintThickness or lead_x + block_size >= randBlueprintX and lead_x + block_size <= randBlueprintX + BlueprintThickness:
                if lead_y >= randBlueprintY and lead_y <= randBlueprintY + BlueprintThickness:
                    randBlueprintX, randBlueprintY = randBlueprintGen()
                    rebelScore+=1
                    blueprintCollected = True

                elif lead_y + block_size >= randBlueprintY and lead_y + block_size <= randBlueprintY + BlueprintThickness:
                    randBlueprintX, randBlueprintY = randBlueprintGen()
                    rebelScore+=1
                    blueprintCollected = True

        clock.tick(30)

        holes[0].draw()
        holes[1].draw()

    ######################### Player controls - Keypress or Typed text #########################

        events = pygame.event.get()

        # to quit game
        for event in events:
            if event.type == pygame.QUIT:
                gameExit = True

        # Use the Movement class to keep track of moves.
        if control_mode == 'TYPE':
            next_move = movement.get_next_move()
            # print "next_move", next_move
            # print "left collision", leftCollision
            # print "right collision", rightCollision
            # print "top collision", topCollision
            # print "btm collision", bottomCollision

            # 0: up, 1: down, 2: right, 3: left
            if next_move == 'stationary':
                lead_x_change = 0
                lead_y_change = 0
            elif next_move == 'move_up':
                if topCollision:
                    bangwall.play()
                    lead_x, lead_y, player = rebel_move(0, lead_x, lead_y, 0, 0, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)
                    # topCollision = False
                else:
                    lead_x, lead_y, player = rebel_move(0, lead_x, lead_y, 0, -10, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)

            elif next_move == 'move_down':
                if bottomCollision:
                    bangwall.play()
                    lead_x, lead_y, player = rebel_move(1, lead_x, lead_y, 0, 0, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)
                    # bottomCollision = False
                else:
                    lead_x, lead_y, player = rebel_move(1, lead_x, lead_y, 0, 10, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)

            elif next_move == 'move_left':
                if leftCollision:
                    bangwall.play()
                    lead_x, lead_y, player = rebel_move(3, lead_x, lead_y, 0, 0, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)
                    # leftCollision = False
                else:
                    lead_x, lead_y, player = rebel_move(3, lead_x, lead_y, -10, 0, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)

            elif next_move == 'move_right':

                if rightCollision:
                    bangwall.play()
                    lead_x, lead_y, player = rebel_move(2, lead_x, lead_y, 0, 0, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)
                    # rightCollision = False
                else:
                    lead_x, lead_y, player = rebel_move(2, lead_x, lead_y, 10, 0, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)

            elif next_move == 'jump_up':
                jump1.play()
                if topCollision:
                    bangwall.play()
                    lead_x, lead_y, player = rebel_jump(0, lead_x, lead_y, 0, 0, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)
                    # topCollision = False
                else:
                    lead_x, lead_y, player = rebel_jump(0, lead_x, lead_y, 0, -10, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)

            elif next_move == 'jump_down':
                jump1.play()
                if bottomCollision:
                    bangwall.play()
                    lead_x, lead_y, player = rebel_jump(1, lead_x, lead_y, 0, 0, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)
                    # bottomCollision = False
                else:
                    lead_x, lead_y, player = rebel_jump(1, lead_x, lead_y, 0, 10, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)

            elif next_move == 'jump_left':
                jump1.play()
                if leftCollision:
                    bangwall.play()
                    lead_x, lead_y, player = rebel_jump(3, lead_x, lead_y, 0, 0, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)
                    # leftCollision = False
                else:
                    lead_x, lead_y, player = rebel_jump(3, lead_x, lead_y, -10, 0, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)

            elif next_move == 'jump_right':
                jump1.play()
                if rightCollision:
                    bangwall.play()
                    lead_x, lead_y, player = rebel_jump(2, lead_x, lead_y, 0, 0, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)
                    # rightCollision = False
                else:
                    lead_x, lead_y, player = rebel_jump(2, lead_x, lead_y, 10, 0, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)

            # reset all collision state after moving (although right now it resets even when not moving)
            topCollision = False
            bottomCollision = False
            leftCollision = False
            rightCollision = False

        if crashed_into_wall(lead_x, lead_y, xlist, ylist, widthlist, heightlist):
            bangwall.play()
            gameOver = True
                    
        # check if player is on a hole
        for hole in holes:
            
            player_rect = pygame.Rect(lead_x, lead_y, 30, 30)
            collide_direction = hole.collides(player_rect)
            if collide_direction == 'exact':
                fall.play()
                gameOver = True

        if parsing:
            movement_state = game_state[:4]
            direction = game_state[5:]
            if movement_state == 'jump' or movement_state == 'move':
                movement.add_move(game_state)
                lead_direction = direction
                game_state = 'moving'
            elif game_state == 'moving' and done_moving():
                game_state = 'idle'

        # run code button
        gameDisplay.blit(btnimg, btn_rect)
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if btn_rect.collidepoint(pygame.mouse.get_pos()):
                    if timerStart==False:
                        timer.set_ticks_func(pygame.time.get_ticks)
                        timer.reset()
                        timerStart=True

                    if level == numOfLevels - 1:
                        place_random_holes()

                    parsing = True

                    code = txtbx.get_text()
                    code = code.replace('self.', '')
                    code_lines += txtbx.get_linecount()
                    parser_thread.start(parser_func, code)
                    txtbx.clear()

        if level == numOfLevels - 1:
            draw_holes()
        
        txtbx.update(events)
        txtbx.draw(gameDisplay)
        pygame.display.update()


    parser_thread.stop()
    pygame.quit()
    quit()

game_intro()
gameLoop()

