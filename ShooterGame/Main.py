#Next Project- chess engine
#Website
#implement boss
#implement difficulty
#implement pause
import pygame
class player:
    def __init__(self, y, health, image):
        self.mode=1
        self.reload=0
        self.health=health
        self.image=image
        self.reload=0
        self.reloadSpeed=5
        self.rect=self.image.get_rect(topleft=(0, y))
    def fire(self): #Depending on the mode, the player changes what they shoots out.
        if self.mode==1:
            Projectiles.add(projectile(True, 100, self.rect.y+10, 5, 10, Bulletimg))
            if level>1:
                Projectiles.add(projectile(True, 100, self.rect.y+30, 5, 10, Bulletimg))
                Projectiles.add(projectile(True, 100, self.rect.y+50, 5, 10, Bulletimg))
        elif self.mode==2:
            if level==1:
                Projectiles.add(projectile(True,100, self.rect.y+10, 10, 20, Rocketimg))
            else:
                Projectiles.add(projectile(True,100, self.rect.y+10, 10, 30, Rocketimg))
    def move(self, mouseCursor): #depending on where the cursor is, the character moves up or down
        if mouseCursor[1]> self.rect.y+50 and self.rect.y<500:
            self.rect.y+=2
        elif mouseCursor[1]< self.rect.y+50 and self.rect.y>0:
            self.rect.y-=2
            
class enemy: #this is unwieldy, but all of these variables makes it posisble to share the same methods and class
    def __init__(self, x, y, health, damage,projspeed, up, speed,tracking, forward,floor, reload, reloadSpeed, proj,mode, image):
        self.health=health
        self.floor=floor
        self.damage=damage
        self.projspeed=projspeed
        self.up=up
        self.speed=speed
        self.tracking=tracking
        self.forward=forward
        self.image=image
        self.reload=reload
        self.reloadSpeed=reloadSpeed
        self.proj=proj
        self.mode=mode
        self.rect=self.image.get_rect(topleft=(x, y))
    def move(self): #needs to check if the character is tracking the player, moving forward, or coming out of the floor
        if self.health<=0:
            EnemyRemoved.add(self)
            if self.image==Boss1img:
                Enemies.append(enemy(300, 300,1000, 40, 3,True, 1, True, False,False, 50, 200,5,0,Boss2img))
                Protag.health+=50
        if self.floor:
            if self.up:
                self.rect.y-=self.speed
            else:
                self.rect.y+=self.speed
            if self.rect.y<450:
                self.up=False
            if self.rect.colliderect(Protag.rect):
                EnemyRemoved.add(self)
                Protag.health-=self.damage
            if self.rect.y>600:
                EnemyRemoved.add(self)
        else:
            if not self.tracking:
                if self.up:
                    self.rect.y-=self.speed
                else:
                    self.rect.y+=self.speed
                if self.rect.y<=0 or self.rect.y>=500:
                    self.up=not self.up
            else:
                if Protag.rect.y>self.rect.y:
                    self.rect.y+=self.speed
                elif Protag.rect.y<self.rect.y:
                    self.rect.y-=self.speed
            if self.forward:
                self.rect.x-=self.speed
                if self.rect.x<-50:
                    EnemyRemoved.add(self)
                if self.rect.colliderect(Protag.rect):
                    EnemyRemoved.add(self)
                    Protag.health-=self.damage
        
    def fire(self): #The three projectiles of the enemies-- bullets for snipers, ninja stars for ninjas, and firebolts for the mage
        if self.proj==1:
            Projectiles.add(projectile(False, self.rect.x, self.rect.y+10, self.projspeed, self.damage, Bulletimg))
        elif self.proj==2:
            Projectiles.add(projectile(False, self.rect.x, self.rect.y+50, self.projspeed, self.damage, NinjaStarimg))
        elif self.proj==3:
            Projectiles.add(projectile(False, self.rect.x, Protag.rect.y+50, self.projspeed, self.damage, FireBoltimg))
        elif self.proj==4:
            if self.mode==5:
                Projectiles.add(projectile(False, 50, 200, 0, self.damage, BlackHoleimg))
                Projectiles.add(projectile(False, 50, 400, 0, self.damage, BlackHoleimg))
                self.mode=-2
            if self.mode<0:
                self.mode+=1
            elif self.mode%2==1:
                Projectiles.add(projectile(False, self.rect.x, Protag.rect.y+40, self.projspeed, self.damage, MagicAttackimg))
                Projectiles.add(projectile(False, self.rect.x, Protag.rect.y-60, self.projspeed, self.damage, MagicAttackimg))
                for i in Projectiles:
                    if i.image==BlackHoleimg:
                        ProjRemoved.add(i)
                self.mode+=1
            else:
                Projectiles.add(projectile(False, self.rect.x, Protag.rect.y+80, self.projspeed, self.damage, MagicAttackimg))
                Projectiles.add(projectile(False, self.rect.x, Protag.rect.y-20, self.projspeed, self.damage, MagicAttackimg))
                self.mode+=1
        elif self.proj==5:
            for i in Projectiles:
                if i.image==Fireimg or i.image==BlackHoleimg:
                    ProjRemoved.add(i)
            Projectiles.add(projectile(False, self.rect.x-100, self.rect.y, self.projspeed, self.damage, Fireimg))
class projectile:
    def __init__(self, yours, x, y, speed, damage, image):
        self.yours=yours
        self.speed=speed
        self.damage=damage
        self.image=image
        self.rect=self.image.get_rect(topleft=(x, y))
    def move(self): # moves projectiles along and checks if it has hit, or is off screen
        if self.yours:
            self.rect.x+=self.speed
            for Enemy in Enemies:
                if self.rect.colliderect(Enemy.rect):
                    ProjRemoved.add(self)
                    Enemy.health-=self.damage
            if self.rect.x>600:
                ProjRemoved.add(self)
        else:
            self.rect.x-=self.speed
            if self.rect.colliderect(Protag.rect):
                Protag.health-=self.damage
                ProjRemoved.add(self)
            if self.rect.x<0:
                ProjRemoved.add(self)
class button:
    def __init__(self, x, y, image):
        self.image=image
        self.rect=self.image.get_rect(topleft=(x,y))
if __name__=='__main__':
    pygame.init()
    w=600
    h=600
    level=1
    screen=pygame.display.set_mode((w,h))
    pygame.display.set_caption("Shooter Game")
    #load images and set sizes
    Background=pygame.transform.scale(pygame.image.load('SkyBackground.jpeg'), (600,600))
    Background1=pygame.transform.scale(pygame.image.load('Background1.jpeg'), (600,600))
    Background2=pygame.transform.scale(pygame.image.load('Background2.jpeg'), (600,600))
    Protagimg=pygame.transform.scale(pygame.image.load('MainCharacter.png'), (100,100))
    Sniperimg=pygame.transform.scale(pygame.image.load('Sniper.png'), (100,100))
    Bulletimg=pygame.transform.scale(pygame.image.load('bullet.jpeg'), (10,10))
    ChargingSoldierimg=pygame.transform.scale(pygame.image.load('ChargingSoldier.png'),(100,100))
    StartButtonimg=pygame.transform.scale(pygame.image.load('StartButton.png'), (100,100))
    NextButtonimg=pygame.transform.scale(pygame.image.load('NextButton.png'), (100,100))
    Rocketimg=pygame.transform.scale(pygame.image.load('rocket.png'), (50,50))
    Protag1img=pygame.transform.scale(pygame.image.load('MainCharacter2.jpeg'), (100,100))
    Ninjaimg=pygame.transform.scale(pygame.image.load('ninja.png'), (100,100))
    NinjaStarimg=pygame.transform.scale(pygame.image.load('NinjaStar.png'), (20,20))
    LavaMonsterimg=pygame.transform.scale(pygame.image.load('LavaMonster.png'), (150,150))
    Mageimg=pygame.transform.scale(pygame.image.load('Mage.png'), (50,50))
    FireBoltimg=pygame.transform.scale(pygame.image.load('Firebolt.png'), (20,20))
    Boss1img=pygame.transform.scale(pygame.image.load('Boss1.png'), (150,150))
    Boss2img=pygame.transform.scale(pygame.image.load('Boss2.png'), (150,150))
    Fireimg=pygame.transform.scale(pygame.image.load('Fire.png'), (100,100))
    MagicAttackimg=pygame.transform.scale(pygame.image.load('MagicBolt.png'), (30,30))
    BlackHoleimg=pygame.transform.scale(pygame.image.load('blackHole.jpeg'), (80,80))
    Level1Button=pygame.transform.scale(pygame.image.load('level1.png'), (80,80))
    Level2Button=pygame.transform.scale(pygame.image.load('level2.png'), (80,80))
    Level3Button=pygame.transform.scale(pygame.image.load('level3.png'), (80,80))
    Protag=player(0, 100, Protagimg)
    Enemies=[]
    # the five enemies created,snipers for long range damage, charging soldier for shielding, ninja for damage, lava monster to discourage camping at the bottom, and the mage for preventing the player from staying in one place.
    #Sniper=enemy(500, 300,20, 15, 10,True, 1, False, False,False, 50, 50,1, Sniperimg)
    #ChargingSoldier=enemy(500,100, 50, 40, 0, True,1,True,True,False, 1000,1000,1,ChargingSoldierimg)
    #Ninja=enemy(300, 300, 30, 10, 20, True, 1.5, True, False,False, 30, 30,2, Ninjaimg)
    #LavaMonster=enemy(0,600, 100, 20, 0, True, 1, False, False, True, 1000,1000, 1, LavaMonsterimg)
    #Mage=enemy(500, 300,30, 15, 3,True, 1, False, False,False, 200, 50,3, Mageimg)
#   #first number corresponds to an enemy, second to the time spent in the stage
    Level1=[(1, 0),(3, 0),(3, 500),(4,500),(1,1000), (2, 1000),(1,1500), (2,1500), (3,1500), (4,1500), (1, 1600), (2,1600), (3,1600), (4,1600)]
    Level2=[(1,0), (3,0), (5,0), (7,0), (3,500), (4,500), (5,500),(6,500), (2,1000), (1,1000), (5, 1000), (6,1500),(7,1500),(2,1500), (1,1500), (3,1500), (4,1500), (5,1600), (5, 1700)]
    Level3=[(8,0)]
    LevelList=[]
    LevelList.append(Level1)
    LevelList.append(Level2)
    LevelList.append(Level3)
    LevelStage=LevelList[0]
    Projectiles=set() #contains the projectiles
    #Modes to determine what appears on the screen
    running=True
    startScreen=True
    Game=False
    LevelScreen=False
    VictoryScreen=False
    delay=0
    stageTime=0
    font=pygame.font.SysFont('arial', 30)
    victoryfont=pygame.font.SysFont('cambria',70)
    while(running):
        if VictoryScreen: #when the second level is cleared
            screen.fill((255,255,255))
            screen.blit(Background2,(0,0))
            text=victoryfont.render('VICTORY!',True, (255,255,255))
            textrect=text.get_rect()
            textrect.center=(300,300)
            screen.blit(text, textrect)
            for event in pygame.event.get():
                if event.type== pygame.QUIT:
                    running=False
            pygame.display.update()
        elif startScreen:# for the start of the game
            Protag.health=100+level*30
            StartButton=button(250,250,StartButtonimg)
            screen.fill((255,255,255))
            screen.blit(Background, (0,0))
            screen.blit(StartButton.image, (250,250))
            mousePos=pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type==pygame.MOUSEBUTTONUP:
                    if StartButton.rect.collidepoint(mousePos):
                        startScreen=False
                        Game=True
                if event.type== pygame.QUIT:
                    running=False
            pygame.display.update()
        elif LevelScreen: #for the end of a level
            #reset everything
            Enemies=[]
            Projectiles=set()
            Protag.health=100+level*30
            screen.fill((255,255,255))
            NextButton=button(250,250, NextButtonimg)
            
            text=font.render('Level '+str(level)+' Completed!', True, (0,0,0))
            textrect=text.get_rect()
            textrect.center=(300,25)
            
            screen.blit(Background,(0,0))
            text.blit(text,textrect)
            screen.blit(NextButton.image,(250,250))
            mousePos=pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type==pygame.MOUSEBUTTONUP:
                    if NextButton.rect.collidepoint(mousePos):
                        LevelScreen=False
                        Game=True
                        LevelStage=LevelList[level-1]
                        stageTime=0
                        Rocketimg=pygame.transform.scale(pygame.image.load('rocket.png'), (75,75))
                if event.type== pygame.QUIT:
                    running=False
            pygame.display.update()
        elif Game: #for during the level
            if delay==0:
                delay=100000
                ProjRemoved=set()
                EnemyRemoved=set()
                #what objects need to be removed from the list
                for Enemy in LevelStage:
                    if Enemy[1]==stageTime:
                        if Enemy[0]==1:
                            Enemies.append(enemy(500, 500,20, 15, 10,True, 1, False, False,False, 50, 50,1,1,Sniperimg))
                        elif Enemy[0]==2:
                            Enemies.append(enemy(500, 10,20, 15, 10,True, 1, False, False,False, 50, 50,1,1, Sniperimg))
                        elif Enemy[0]==3:
                            Enemies.append(enemy(500,100, 50, 40, 0, True,1,True,True,False, 1000,1000,1,1,ChargingSoldierimg))
                        elif Enemy[0]==4:
                            Enemies.append(enemy(500,400, 50, 40, 0, True,1,True,True,False, 1000,1000,1,1,ChargingSoldierimg))
                        elif Enemy[0]==5:
                            Enemies.append(enemy(300, 500, 30, 10, 5, True, 1.5, True, False,False,  30, 30,2,1,Ninjaimg))
                        elif Enemy[0]==6:
                            Enemies.append(enemy(0,600, 100, 20, 0, True, 1, False, False, True, 1000,1000, 1,1,LavaMonsterimg))
                        elif Enemy[0]==7:
                            Enemies.append(enemy(500, 300,30, 15, 3,True, 1, False, False,False, 50, 150,3,1,Mageimg))
                        elif Enemy[0]==8:
                            Enemies.append(enemy(500, 300,1000, 20, 3,True, 1, True, False,False, 50, 100,4,0,Boss1img))
                if not Enemies and stageTime>1700: #when the level is completed
                    Game=False
                    LevelScreen=True
                    if level<3:
                        level+=1
                    else:
                        VictoryScreen=True
                
                screen.fill((255,255,255))
                screen.blit(Background1, (0,0))
                screen.blit(Protag.image, (0,Protag.rect.y))
                pygame.draw.rect(screen, (0,0,255), pygame.Rect(50, 10, 1.5*Protag.health,20)) #health bar
                text=font.render('Level '+str(level), True, (0,0,0))
                textrect=text.get_rect()
                textrect.center=(400,25)
                screen.blit(text,textrect) #level text during level
                
                for Enemy in Enemies: #every enemy moves and checks if it can fire
                #charging soldier and lava monster just have very high reload speed so they never shoot
                    screen.blit(Enemy.image, (Enemy.rect.x, Enemy.rect.y))
                    Enemy.move()
                    Enemy.reload-=1
                    if Enemy.reload==0:
                        Enemy.reload=Enemy.reloadSpeed
                        Enemy.fire()
                for ammo in Projectiles:
                    screen.blit(ammo.image, (ammo.rect.x, ammo.rect.y))
                    ammo.move() #Projectiles all move
                
                for ammo in ProjRemoved: #removes what needs to be removed
                    Projectiles.remove(ammo)
                for Enemy in EnemyRemoved:
                    Enemies.remove(Enemy)
                mousePos=pygame.mouse.get_pos()
                Protag.move(mousePos)
                if Protag.health<=0: #game ends if the protag runs out of health
                    Game=False
                    LevelScreen=True
                    
                if Protag.reload>0:
                    Protag.reload-=1
                    
                for event in pygame.event.get():
                    if event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_SPACE: #changes mode
                            if Protag.mode==1:
                                Protag.mode=2
                                Protag.image=Protag1img
                                Protag.reloadSpeed=30
                            elif Protag.mode==2:
                                Protag.mode=1
                                Protag.image=Protagimg
                                Protag.reloadSpeed=5
                    if event.type== pygame.QUIT:
                        running=False
                    if event.type==pygame.MOUSEBUTTONUP:# tries to fire
                        if Protag.reload<=0:
                                Protag.fire()
                                Protag.reload=Protag.reloadSpeed
                pygame.display.update()
                stageTime+=1
            delay-=1
    pygame.quit()
