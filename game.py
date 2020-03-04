import pygame
from pygame.locals import *
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.color import Color
import queue
import os
def init(scr=None):
    global defimg,hasShield,hasnShield,kl,kr,ku,kd,BLACK,WHITE,BLUE,GREEN,RED,size,screen,clock,arrowgroup,arrowimg,playerimg,shieldimg,font,backgroundColor,ongroundColor,levelName,levelAuthor,levelDifficulty,levelTime,level,gameEnd,nowTick,nextTick,nowEvent
    # Initialize the game engine
    pygame.font.init()
    BLACK= ( 0,  0,  0)
    WHITE= (255,255,255)
    BLUE = ( 0,  0,255)
    GREEN= ( 0,255,  0)
    RED  = (255,  0,  0)
    # make variables
    kr,kl,ku,kd=False,False,False,False
    size  = [1024,720]
    clock = pygame.time.Clock()
    #load
    defimg=[]
    for x in range(4):
        defimg.append(pygame.image.load('images/defPoint_'+str(x)+'.png').convert_alpha())
    arrowgroup = pygame.sprite.Group()
    arrowimg=[]
    for x in range(10):
        arrowimg.append(pygame.image.load('images/arrow_'+str(x+1)+'.png').convert_alpha())
    playerimg=[]
    for x in range(4):
        playerimg.append(pygame.image.load('images/player_'+str(x+1)+'.png'))
    shieldimg=[]
    shieldimg.append(pygame.image.load('images/shield_1.png').convert_alpha())
    shieldimg.append(pygame.image.load('images/shield_2.png').convert_alpha())
    shieldimg.append(pygame.image.load('images/shield_3.png').convert_alpha())
    hasShield=pygame.image.load('images/has_shield.png').convert_alpha()
    hasnShield=pygame.image.load('images/hasn_shield.png').convert_alpha()
    # Initialize
    font=pygame.font.Font('./NanumGothic.ttf',30)
    backgroundColor=WHITE
    ongroundColor=BLACK
    levelName="Level"
    levelAuthor="Troll"
    levelDifficulty=1
    levelTime=0
    level=queue.Queue()
    nowTick=0
    gameEnd=-1
    nowEvent=queue.Queue()
def endGame(lvn,Invulnerable):
    global screen
    TERMINATE=False
    mPc=0
    while not TERMINATE:
        print("sdfkj")
        init()
        loadLevel(lvn)
        percent=rungame(lvn,Invulnerable)
        print(percent)
        Terminate=False
        font=pygame.font.Font('./NanumGothic.ttf',60)
        font2=pygame.font.Font('./NanumGothic.ttf',30)
        text=None
        if percent>mPc:
            mPc=percent
        if percent == 100:
            text=font.render("CLEAR",True,(0,255,0))
        else:
            text=font.render("GAME OVER",True,(255,255,255))
        while not Terminate:
            for event in pygame.event.get(): 
                if event.type==pygame.QUIT:
                    Terminate=True
                    TERMINATE=True
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        Terminate=True
                        TERMINATE=True
                    if event.key==pygame.K_r:
                        print("Restart")
                        Terminate=True
            if percent==100:
                screen.fill(WHITE)
            else:
                screen.fill(BLACK)
            screen.blit(text,(350,300))
            screen.blit(font2.render("ESC를 눌러 돌아가기,R을 눌러 다시하기",True,(255,255,0)),(10,10))
            pygame.display.flip()
    print(mPc)
    return mPc
def loadLevel(levelfilename):
    global levelName,levelAuthor,levelDifficulty,levelTime,level
    #level load
    lvl = open("levels/"+levelfilename+"/level",'r')
    levelName = lvl.readline()
    levelAuthor=lvl.readline()
    levelDifficulty=int(lvl.readline())
    levelTime = int(lvl.readline())
    if(os.path.exists('levels/'+levelfilename+'/music.wav')):
        pygame.mixer.music.load('levels/'+levelfilename+'/music.wav')
        pygame.mixer.music.play(-1)
    #level load
    for nowsec in range(levelTime): # as 1 second
        oneline=lvl.readline().strip().split()# 1 line
        for x in range(len(oneline)):
            level.put(int(oneline[x]))
    lvl.close()
def levelEvent():
    global level,player,backgroundColor,ongroundColor
    # 1 tick
    if level.empty():
        return
    event=level.get()
    for e in range(event):# 1 event
        eventType=level.get()
        if eventType==1:
            ak=level.get()
            bk=level.get()
            ck=level.get()
            backgroundColor=(ak,bk,ck)
            ongroundColor=(255-ak,255-bk,255-ck)
        elif eventType==2:
            arrowType=level.get()
            arrowPos=level.get()
            arrowSpeed=level.get()
            newarrow(arrowPos,arrowSpeed,arrowType)
        elif eventType==3:
            t=level.get()
            if t==1:
                player.chmod(level.get())
            elif t==2:
                player.damage(level.get())
            elif t==3:
                player.SH=level.get()
            elif t==4:
                player.DEF+=level.get()
            elif t==5:
                player.DEF=level.get()
            elif t==6:
                player.IDEF+=level.get()
            elif t==7:
                player.IDEF=level.get()
            elif t==8:
                player.HP+=level.get()
            elif t==9:
                player.HP=level.get()
            elif t==10:
                player.SPEED+=level.get()
            elif t==11:
                player.SPEED=level.get()
            elif t==12:
                player.MHP+=level.get()
            elif t==13:
                player.MHP=level.get()
    if player.SPEED>200:
        player.SPEED=200
    elif player.SPEED<20:
        player.SPEED=20
    player.speed=int((player.SPEED*15)/100)# SPEED is Percent(%), speed is real one
    if player.HP>player.MHP:
        player.HP=player.MHP
    if player.DEF>3:
        player.DEF=3
    if player.SH>1:
        player.SH=1
    if player.HP<=0:
        player.HP=0
def rotate(image, rect, angle):
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image,rot_rect
class Player(Sprite):#(212,60),(812,660)
    def __init__(self):
        Sprite.__init__(self)
        self.sprite_width=64
        self.sprite_height=64
        self.mode=0
        self.image = playerimg[self.mode]
        self.image.blit(self.image,(0,0))
        self.rect = self.image.get_rect()
        self.rect.x=480
        self.rect.y=328
        self.moveDown=False
        self.moveUp=False
        self.moveLeft=False
        self.moveRight=False
        self.speed=15
        self.SPEED=100
        self.HP=10
        self.MHP=10
        self.DEF=0
        self.SH=0
        self.IDEF=0
        self.Invulnerable=False
    def update(self):
        global arrowgroup
        #move variable
        if self.moveDown ==True and self.rect.y < 592:
            if self.moveLeft==True or self.moveRight==True:
                self.rect.y=self.rect.y+int(self.speed*0.7)
            else:
                self.rect.y=self.rect.y+int(self.speed)
        if self.moveUp==True and self.rect.y > 60:
            if self.moveLeft==True or self.moveRight==True:
                self.rect.y=self.rect.y-int(self.speed*0.7)
            else:
                self.rect.y=self.rect.y-int(self.speed)
        if self.moveLeft ==True and self.rect.x > 212:
            if self.moveUp==True or self.moveDown==True:
                self.rect.x = self.rect.x-int(self.speed*0.7)
            else:
                self.rect.x = self.rect.x-int(self.speed)
        if self.moveRight==True and self.rect.x < 744:
            if self.moveUp==True or self.moveDown==True:
                self.rect.x=self.rect.x+int(self.speed*0.7)
            else:
                self.rect.x=self.rect.x+int(self.speed)
        
        #Fix out of Field
        if self.rect.y> 592:
            self.rect.y=592
        if self.rect.y<60:
            self.rect.y=60
        if self.rect.x<212:
            self.rect.x=212
        if self.rect.x>744:
            self.rect.x=744
        for ar in arrowgroup: #player was hit by arrow
            if self.rect.colliderect(ar.rect):
                #TODO make things
                m=ar.mode
                if m==0:
                    self.damage(2)
                elif m==1:
                    self.damage(2)
                    self.MHP+=1
                elif m==2:
                    self.damage(1)
                    self.MHP-=1
                elif m==3:
                    self.damage(3)
                elif m==4:
                    self.damage(3)
                    self.SPEED+=2
                elif m==5:
                    self.damage(3)
                    self.SPEED-=2
                elif m==6:
                    self.damage(1)
                    self.DEF+=1
                elif m==7:
                    self.damage(1)
                elif m==8:
                    self.damage(5)
                elif m==9:
                    self.damage(2)
                    self.SPEED-=2
                ar.kill()
                del ar
    def damage(self,d):
        global backgroundColor,bgci
        if self.SH==1:
            self.SH=0
            return
        if self.DEF<d:
            d-=self.DEF
            self.DEF=0
        else:
            self.DEF-=d
            d=0
        if self.Invulnerable==False:
            self.HP-=d
        bgci=10
        return
    def draw():
        screen.blit(self.image,[self.rect.x,self.rect.y])
    def chmod(self,mode):
        global shield
        self.mode = mode
        self.image=playerimg[mode]
        shield.time=0
        shield.rot=0
class Shield(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image=shieldimg[0]
        self.rect=self.image.get_rect()
        self.mode=0
        self.time=0
        self.rot=0
    def update(self):
        if gameEnd>=0:
            return
        global arrowgroup
        if self.time >0:
            self.time-=1
        if self.time==0:
            self.mode = 0
        if player.mode == 3:
            self.time=10000
            self.mode=10
            if kl==True:
                self.rot+=6
            if kr == True:
                self.rot-=6
            self.image=shieldimg[2]
            self.image,self.rect=rotate(self.image,self.rect,self.rot)
        self.rect.x=player.rect.x-32
        self.rect.y=player.rect.y-32
        if player.mode==3:
            self.rect.x-=10
            self.rect.y-=10
        self.mask=pygame.mask.from_surface(self.image)
        for ar in arrowgroup:
            if pygame.sprite.collide_mask(self,ar): # On Defend
                m=ar.mode
                if m==1:
                    player.damage(5)
                    player.MHP+=1
                elif m==2:
                    player.HP+=5
                    player.MHP-=1
                elif m==4:
                    player.damage(1)
                    player.SPEED+=4
                elif m==5:
                    player.damage(2)
                    player.SH=1
                elif m==6:
                    player.DEF+=2
                elif m==8:
                    player.damage(30)
                elif m==9:
                    player.damage(1)
                ar.kill()
                del ar
        
    def defense(self,mod): # On arrow key
        if gameEnd>=0:
            return
        if player.mode == 0 or player.mode == 4:
            self.mode=mod
            self.time=20
            self.image = shieldimg[0]
            if self.mode==2:
                self.image,self.rect=rotate(self.image,self.rect,90)
            elif self.mode ==3:
                self.image,self.rect=rotate(self.image,self.rect,180)
            elif self.mode == 4:
                self.image,self.rect=rotate(self.image,self.rect,270)
        elif player.mode == 2:
            self.mode=mod
            self.time=10000
            self.image = shieldimg[0]
            if self.mode==2:
                self.image,self.rect=rotate(self.image,self.rect,90)
            elif self.mode ==3:
                self.image,self.rect=rotate(self.image,self.rect,180)
            elif self.mode == 4:
                self.image,self.rect=rotate(self.image,self.rect,270)
        elif player.mode == 1: # kl=LEFT,kr=RIGHT,ku=UP,kd=DOWN
            self.image=shieldimg[1]
            self.mode=5
            self.time=20
            if ku==True and kl==True and kr==False and kd==False: #left up
                self.image,self.rect=rotate(self.image,self.rect,0)
            elif ku==True and kr==True and kd==False and kl==False: #right up
                self.image,self.rect=rotate(self.image,self.rect,270)
            elif kr==True and kd==True and kl == False and ku == False: #right down
                self.image,self.rect=rotate(self.image,self.rect,180)
            elif kl==True and kd==True and kr == False and ku == False: #left down
                self.image,self.rect=rotate(self.image,self.rect,90)
            else :
                self.mode=0
                self.time=0
    def draw(self,screen):
        if self.mode !=0 and self.time!=0:
            screen.blit(self.image,(self.rect.x,self.rect.y))
class Arrow(Sprite):
    def __init__(self,pos,speed,mode):
        Sprite.__init__(self)
        self.sprite_width=31
        self.sprite_height=64
        self.speed=speed
        self.mode=mode
        self.image = arrowimg[self.mode]
        self.image.set_colorkey([255,0,255])
        self.image.blit(self.image,(0,0))
        self.rect = self.image.get_rect()
        self.pos=pos
        if (self.pos>=0 and self.pos<100):
            self.image,self.rect=rotate(self.image,self.rect,180)
            self.rect.x=pos*6+212
            self.rect.y=-4
        elif (self.pos>=100 and self.pos<200):
            self.rect.x=812
            self.rect.y=60+(pos-100)*6
            self.image,self.rect=rotate(self.image,self.rect,90)
        elif (self.pos>=200 and self.pos<300):
            self.rect.x=812-(pos-200)*6
            self.rect.y=660
        elif (self.pos>=300 and self.pos<400):
            self.rect.x=212-64
            self.rect.y=660-(pos-300)*6
            self.image,self.rect=rotate(self.image,self.rect,270)
    def update(self):
        global player
        self.mask=pygame.mask.from_surface(self.image)
        if self.pos>=0 and self.pos<100:
            self.rect.y=self.rect.y + self.speed
        elif self.pos>=100 and self.pos<200:
            self.rect.x = self.rect.x - self.speed
        elif self.pos>=200 and self.pos<300:
            self.rect.y=self.rect.y-self.speed
        elif self.pos>=300 and self.pos<400:
            self.rect.x=self.rect.x+self.speed
        if (self.rect.y >= 660 and (self.pos>=0 and self.pos<100)) or (self.rect.x<=212 and(self.pos>=100 and self.pos<200)) or (self.rect.y<=60 and (self.pos>=200 and self.pos<300)) or (self.rect.x>=812 and(self.pos>=300 and self.pos<400)):
            #TODO Event when Purple and pink and gray arrow
            if self.mode == 3:
                player.damage(5)
            elif self.mode == 7:
                player.damage(1)
            elif self.mode==9:
                player.SPEED-=2
            self.kill()
            del self
        
    def draw():
        screen.blit(self.image,[self.rect.x,self.rect.y])

def newarrow(pos,speed,mode):
    global arrowgroup
    ar = Arrow(pos,speed,mode)
    arrowgroup.add(ar)
def rungame(lvlname,Invulnerable): #returns percentage
    
    global player_mode,player,nowTick,gameEnd,shield,bgci,kl,kr,ku,kd
    print("Run Game")
    loadLevel(lvlname)
    #init
    player = Player()
    player.Invulnerable=Invulnerable
    playergroup=pygame.sprite.Group()
    playergroup.add(player)
    shield=Shield()
    nextTick=0
    bgci=0
    ld=['TUTORIAL','EASY','MEDIUM','HARD','INSANE','EXTREME','CHAOS']
    levelInfo1=font.render(levelName+' BY '+levelAuthor,True,(0,0,0))
    levelInfo2=font.render(ld[levelDifficulty],True,(0,0,0))
    while True:
        #set 60FPS
        clock.tick(60)
        #event get
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return int((float(nowTick)/float(levelTime)*float(100)))
            #WASD key input
            if event.type ==pygame.KEYDOWN:
                if event.key==pygame.K_w:
                    player.moveUp=True
                if event.key ==pygame.K_s:
                    player.moveDown=True
                if event.key ==pygame.K_a:
                    player.moveLeft=True
                if event.key ==pygame.K_d:
                    player.moveRight=True
                if event.key == pygame.K_UP:
                    ku=True
                    shield.defense(1)
                if event.key == pygame.K_DOWN:
                    kd=True
                    shield.defense(3)
                if event.key == pygame.K_LEFT:
                    kl=True
                    shield.defense(2)
                if event.key == pygame.K_RIGHT:
                    kr=True
                    shield.defense(4)
            if event.type ==pygame.KEYUP:
                if event.key==pygame.K_w:
                    player.moveUp=False
                if event.key ==pygame.K_s:
                    player.moveDown=False
                if event.key ==pygame.K_a:
                    player.moveLeft=False
                if event.key ==pygame.K_d:
                    player.moveRight=False
                if event.key == pygame.K_UP:
                    ku=False
                if event.key == pygame.K_DOWN:
                    kd=False
                if event.key == pygame.K_LEFT:
                    kl=False
                if event.key == pygame.K_RIGHT:
                    kr=False
        #update
        
        player.update()
        for ar in arrowgroup:
            ar.update()
        shield.update()
        # events
        if nextTick==0: #once per tick
            if gameEnd==-1:
                levelEvent()
            if player.HP==0 and gameEnd==-1: # game over
                arrowgroup.empty()
                gameEnd=10
            if nowTick==levelTime and gameEnd==-1: # level clear
                gameEnd=20
            if gameEnd==0:
                return int((float(nowTick)/float(levelTime)*float(100)))
            elif gameEnd>0:
                gameEnd-=1
            elif gameEnd == -1:
                nowTick+=1 # Now time (tick)
            nextTick=6 # Frames before next tick
        nextTick-=1
        if bgci==0:
            screen.fill(backgroundColor)
        elif bgci >=1:
            screen.fill((int(((10-bgci)*255+bgci*backgroundColor[0])/10),int((10-bgci)*backgroundColor[1]/10),int((10-bgci)*backgroundColor[2])/10))
            bgci-=1
        #draw after here
        arrowgroup.draw(screen)
        playergroup.draw(screen)
        shield.draw(screen)
        pygame.draw.rect(screen,ongroundColor,[212,60,600,600],5)# game box
        # UI
        hpText=font.render('HP '+str(player.HP),True,(0,0,0))
        mhpText=font.render('/ '+str(player.MHP),True,(0,0,0))
        pygame.draw.rect(screen,RED,[190,10,player.MHP*20,40],3)
        pygame.draw.rect(screen,RED,[190,10,player.HP*20,40])
        screen.blit(hpText,(200,10))
        screen.blit(mhpText,(300,10))
        screen.blit(defimg[player.DEF],(600,10))
        screen.blit(levelInfo1,(200,670))
        screen.blit(levelInfo2,(20,20))
        if player.SH==0:
            screen.blit(hasnShield,(700,10))
        else:
            screen.blit(hasShield,(700,10))
        #draw before here
        pygame.display.flip()
def run(lvn,Invulnerable=False):
    global screen
    pygame.init()
    screen= pygame.display.set_mode([1024,720],DOUBLEBUF)
    pygame.display.set_caption("Aroid InDev 0.0.5")
    pygame.display.set_icon(pygame.image.load('images/icon.png'))
    init()
    endGame(lvn,Invulnerable)
    pygame.quit()
