import cv2
from bsdqntester import DQN
import numpy as np
from PIL import ImageGrab
import pygame
import pyautogui
import time
import random

pygame.init()


toffsetx,toffsety = 35,85
ts = 22
##34 84 56 107
##22 22
##158 820 33 elxr
def nothing(x):
    pass
    

elc = [155,820]
avc = [150,805]

agent = DQN(5,21)

screen = np.array(ImageGrab.grab(bbox = (0,40,480,894)))
cv2.namedWindow('output')
cv2.createTrackbar('threshold','output',80,100,nothing)

template_def = cv2.imread('template.jpg')
template = template_def[:,:,2]
w, h = template.shape[::-1]



#set color with rgb
white,black,red,blue,green = (255,255,255),(0,0,0),(255,0,0),(0,0,255),(0,255,0)
g1,g2 = (162,182,74),(174,186,91)
road,water = (222,184,121),(0,158,202)

#block types

G = {'Air':True,'Ground':True,'color':g1,'color2':g2,}
R = {'Air':True,'Ground':True,'color':road}
V = {'Air':False,'Ground':False,'color':white}
W = {'Air':True,'Ground':False,'color':water}

#unit types

archer = {'Cost':3,'HP':252,'Attack':89,'HSpeed':1.2,'DeployTime':1,'DPS':74,'Range':5,'TargetAir':True,'TravelAir':False,'Speed':3,'EnemyUnit':False}
minion = {'Cost':3,'HP':190,'Attack':84,'HSpeed':1,'DeployTime':1,'DPS':84,'Range':1.6,'TargetAir':True,'TravelAir':True,'Speed':4,'EnemyUnit':False}
hog = {'Cost':4,'HP':1408,'Attack':264,'HSpeed':1.6,'DeployTime':1,'DPS':165,'Range':0.8,'TargetAir':False,'TravelAir':False,'Speed':3,'EnemyUnit':False}
goblin = {'Cost':2,'HP':167,'Attack':99,'HSpeed':1.1,'DeployTime':1,'DPS':90,'Range':0.5,'TargetAir':False,'TravelAir':False,'Speed':4,'EnemyUnit':False}
wizard = {'Cost':5,'HP':598,'Attack':234,'HSpeed':1.4,'DeployTime':1,'DPS':167,'Range':5.5,'TargetAir':True,'TravelAir':False,'Speed':2,'EnemyUnit':False}
knight = {'Cost':3,'HP':1452,'Attack':167,'HSpeed':1.2,'DeployTime':1,'DPS':139,'Range':1.2,'TargetAir':False,'TravelAir':False,'Speed':2,'EnemyUnit':False}
giant = {'Cost':5,'HP':3275,'Attack':211,'HSpeed':1.5,'DeployTime':1,'DPS':140,'Range':1.2,'TargetAir':False,'TravelAir':False,'Speed':1.5,'EnemyUnit':False}


#text handeling
font = pygame.font.Font('freesansbold.ttf', 32)
myfont = pygame.font.SysFont('Segoe UI', 20)
text_elixir = myfont.render('ELIXIR: ', True, (0, 0, 0))

#set display
gameDisplay = pygame.display.set_mode((400,800))

#BG
arena = np.array([[V,V,V,V,V,V,G,G,G,G,G,G,V,V,V,V,V,V],
         [G,G,G,G,G,G,G,R,R,R,R,G,G,G,G,G,G,G],
         [G,G,G,G,G,G,G,R,R,R,R,G,G,G,G,G,G,G],
         [G,G,G,R,R,R,R,R,R,R,R,R,R,R,R,G,G,G],
         [G,G,G,R,G,G,G,R,R,R,R,G,G,G,R,G,G,G],
         [G,G,R,R,R,G,G,G,G,G,G,G,G,R,R,R,G,G],
         [G,G,R,R,R,G,G,G,G,G,G,G,G,R,R,R,G,G],
         [G,G,R,R,R,G,G,G,G,G,G,G,G,R,R,R,G,G],
         [G,G,G,R,G,G,G,G,G,G,G,G,G,G,R,G,G,G],
         [G,G,G,R,G,G,G,G,G,G,G,G,G,G,R,G,G,G],
         [G,G,G,R,G,G,G,G,G,G,G,G,G,G,R,G,G,G],
         [G,G,G,R,G,G,G,G,G,G,G,G,G,G,R,G,G,G],
         [G,G,G,R,G,G,G,G,G,G,G,G,G,G,R,G,G,G],
         [G,G,G,R,G,G,G,G,G,G,G,G,G,G,R,G,G,G],
         [V,G,G,R,G,G,G,G,G,G,G,G,G,G,R,G,G,V],
         [W,W,R,R,R,W,W,W,W,W,W,W,W,R,R,R,W,W],
         [W,W,R,R,R,W,W,W,W,W,W,W,W,R,R,R,W,W],
         [V,G,G,R,G,G,G,G,G,G,G,G,G,G,R,G,G,V],
         [G,G,G,R,G,G,G,G,G,G,G,G,G,G,R,G,G,G],
         [G,G,G,R,G,G,G,G,G,G,G,G,G,G,R,G,G,G],
         [G,G,G,R,G,G,G,G,G,G,G,G,G,G,R,G,G,G],
         [G,G,G,R,G,G,G,G,G,G,G,G,G,G,R,G,G,G],
         [G,G,G,R,G,G,G,G,G,G,G,G,G,G,R,G,G,G],
         [G,G,G,R,G,G,G,G,G,G,G,G,G,G,R,G,G,G],
         [G,G,R,R,R,G,G,G,G,G,G,G,G,R,R,R,G,G],
         [G,G,R,R,R,G,G,G,G,G,G,G,G,R,R,R,G,G],
         [G,G,R,R,R,G,G,G,G,G,G,G,G,R,R,R,G,G],
         [G,G,G,R,G,G,G,R,R,R,R,G,G,G,R,G,G,G],
         [G,G,G,R,R,R,R,R,R,R,R,R,R,R,R,G,G,G],
         [G,G,G,G,G,G,G,R,R,R,R,G,G,G,G,G,G,G],
         [G,G,G,G,G,G,G,R,R,R,R,G,G,G,G,G,G,G],
         [V,V,V,V,V,V,G,G,G,G,G,G,V,V,V,V,V,V]
         ])
print (arena.shape)
#caption
pygame.display.set_caption("CRAI")

size = 20
#beginning of logic
gameExit = False

lead_x = 20
lead_y = 20

gameDisplay.fill(white)
Start = False
while not Start:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                Start = True


while not gameExit:
    avcard = [False,False,False,False]
    elcount = 0
    elch = 0
    enemies = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
                
    screen = np.array(ImageGrab.grab(bbox = (0,40,480,894)))
    img_rgb=cv2.cvtColor(screen,cv2.COLOR_BGR2RGB)
    img_r=screen[:,:,2]

    while(img_r[elc[1]][elc[0]+elch]>100 and elch < 290):
        elcount+=1
        elch+=32

    for i in range(0,4):
        if(img_r[avc[1]][avc[0]+i*90]>100):
            avcard[i]=True
    
    res = cv2.matchTemplate(img_r,template,cv2.TM_CCOEFF_NORMED)
    threshold = cv2.getTrackbarPos('threshold','output')*0.01
    loc = np.where( res >= threshold)

    
    for pt in zip(*loc[::-1]):
        fpt = ((pt[0]- toffsetx)//ts,(pt[1]- toffsety)//ts+3)
        enemies.append(fpt)
        cv2.rectangle(img_rgb, (fpt[0]*ts +toffsetx,fpt[1]*ts +toffsety), (fpt[0]*ts +toffsetx + ts, fpt[1]*ts +toffsety + ts), (0,255,255), 2)
        #cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)
        

    cv2.imshow('output',img_rgb)


    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

#Size of squares



    gameDisplay.fill(white)
    
    cnt = 0
    for i in range(0,arena.shape[0]):
        for z in range(0,arena.shape[1]):
            if(arena[i][z]==G):
                if(cnt%2==0):
                    pygame.draw.rect(gameDisplay, arena[i][z]['color2'], [size*z,size*i,size,size])
                else:
                    pygame.draw.rect(gameDisplay, arena[i][z]['color'], [size*z,size*i,size,size])
            else:
                pygame.draw.rect(gameDisplay, arena[i][z]['color'], [size*z,size*i,size,size])
            cnt +=1
        #since theres an even number of squares go back one value
        cnt-=1

    state = [elcount,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
    cnt=1
    for enemy in enemies :
        if(cnt<20):
            state[cnt] = enemy[0]
            state[cnt+1] = enemy[1]
            cnt+=2
        pygame.draw.rect(gameDisplay, red, [size*enemy[0],size*(enemy[1]+1),size,size])
    #pygame.draw.circle(gameDisplay, thing[1], (thing[0][0]*size+size/2,thing[0][1]*size+size/2),10)
    
    for i in range(0,4):
        if(avcard[i]):
            pygame.draw.rect(gameDisplay, green, [200+i*32,700,16,32])
        else:
            pygame.draw.rect(gameDisplay, red, [200+i*32,700,16,32])
        
    
    state = np.reshape(state, (1, 21))
    action =  (agent.act(state))

    if(action==1):
        pyautogui.press(str(random.randint(1,5)))
        pyautogui.click(50,580)
    if(action==2):
        pyautogui.press(str(random.randint(1,5)))
        pyautogui.click(430,580)
    if(action==3):
        pyautogui.press(str(random.randint(1,5)))
        pyautogui.click(210,500)
    if(action==4):
        pyautogui.press(str(random.randint(1,5)))
        pyautogui.click(250,500)


    text_elixir_number = myfont.render(str(elcount), True, (0, 0, 0))

    gameDisplay.blit(text_elixir, (45, 700))
    gameDisplay.blit(text_elixir_number, (120, 700))
    
    pygame.display.update()


#quit from pygame & python
pygame.quit()
cv2.destroyAllWindows()
