#!/usr/bin/env python2.7
"""
*Project done by :Jishnu V.K.(IMT201833)
                  Harshvardhan Kumar(IMT2018027)
                  Shubhayu Das(IMT2018523)

Project based on the android game Dan the Man by Halfbrick Studios.

Project done for Python assignment for First semester of iMtech 2018.

"""
#importing the necessary header files
import pygame
import random
import math
import time

pygame.init()        #starting the pygame module
pygame.mixer.init()         #start playing the background music




window = pygame.display.set_mode((1200,700))
pygame.display.set_caption("DAN THE MAN")

#getting the necessary file paths for the resources from the folder
soundPath = "./resources/Audio/"
digitsPath = "./resources/Digits/"
danPath = "./resources/Characters/dan/"
enemyPath = "./resources/Characters/enemy/"
miscPath = "./resources/Characters/misc/"

pygame.mixer.Channel(0).play(pygame.mixer.Sound(soundPath+"backy.wav"), -1)

#loading the abstract miscelllaneous images for the background
digits = [pygame.image.load(digitsPath+"0.png"),pygame.image.load(digitsPath+"1.png"),pygame.image.load(digitsPath+"2.png"),pygame.image.load(digitsPath+"3.png"),pygame.image.load(digitsPath+"4.png"),pygame.image.load(digitsPath+"5.png"),pygame.image.load(digitsPath+"6.png"),pygame.image.load(digitsPath+"7.png"),pygame.image.load(digitsPath+"8.png"),pygame.image.load(digitsPath+"9.png")]
gunLogo = pygame.image.load(miscPath+"gunLogo.png")
danHead = pygame.image.load(miscPath+"danHead.png")

#loading the image for the platforms on which the character stands
platform1 = pygame.image.load(miscPath+"platform1.png")
platform2 = pygame.image.load(miscPath+"platform2.png")
platform3 = pygame.image.load(miscPath+"platform3.png")

#Importing all the sprites for dan
runLeft = [pygame.image.load(danPath+"running1.png"),pygame.image.load(danPath+"running2.png"),pygame.image.load(danPath+"running3.png"),pygame.image.load(danPath+"running2.png"),pygame.image.load(danPath+"running1.png")]
runRight = [pygame.transform.flip(x,True,False) for x in runLeft]
jumpLeft = pygame.image.load(danPath+"running6.png")
jumpRight = pygame.transform.flip(jumpLeft, True, False)
standLeft = pygame.image.load(danPath+"stand.png")
standRight = pygame.transform.flip(standLeft,True,False)
punchLeft = [pygame.image.load(danPath+"punching1.png"),pygame.image.load(danPath+"punching2.png"),pygame.image.load(danPath+"punching3.png"),pygame.image.load(danPath+"punching3.png")]
punchRight = [pygame.transform.flip(x,True,False) for x in punchLeft]
danDie =  [pygame.image.load(danPath+"danDie.png"),pygame.image.load(danPath+"danDie2.png"),pygame.image.load(danPath+"danDie.png"),pygame.image.load(danPath+"danDie3.png")]
bulletLeft = pygame.image.load(danPath+"bullet.png")
bulletRight = pygame.transform.flip(bulletLeft, True, False) 
shootLeft = pygame.image.load(danPath+"danGun.png")
shootRight = pygame.transform.flip(shootLeft, True, False)

#Importing all the sprites for the enemy sprites
enemyRunLeft=[pygame.image.load(enemyPath+"enemyrun1.png"),pygame.image.load(enemyPath+"enemyrun2.png"),pygame.image.load(enemyPath+"enemyrun3.png"),pygame.image.load(enemyPath+"enemyrun2.png"),pygame.image.load(enemyPath+"enemyrun1.png")]
enemyRunRight = [pygame.transform.flip(x,True,False) for x in enemyRunLeft]
enemyStandLeft=pygame.image.load(enemyPath+"enemystand.png")
enemyStandRight=pygame.transform.flip(enemyStandLeft,True,False)
enemyHit=[pygame.image.load(enemyPath+"enemyhit1.png"),pygame.image.load(enemyPath+"enemyhit2.png"),pygame.image.load(enemyPath+"enemyhit3.png"),pygame.image.load(enemyPath+"enemyhit3.png"),pygame.image.load(enemyPath+"enemyhit2.png"),pygame.image.load(enemyPath+"enemyhit1.png")]
enemyPunchLeft=[pygame.image.load(enemyPath+"enemyhitting1.png"),pygame.image.load(enemyPath+"enemyhitting2.png"),pygame.image.load(enemyPath+"enemyhitting3.png"),pygame.image.load(enemyPath+"enemyhitting4.png"),pygame.image.load(enemyPath+"enemyhitting4.png"),pygame.image.load(enemyPath+"enemyhitting3.png"),pygame.image.load(enemyPath+"enemyhitting2.png"),pygame.image.load(enemyPath+"enemyhitting1.png")]
enemyPunchRight=[pygame.transform.flip(x,True,False) for x in enemyPunchLeft]
enemyDie=[pygame.image.load(enemyPath+"enemydie1.png"),pygame.image.load(enemyPath+"enemydie2.png"),pygame.image.load(enemyPath+"enemydie3.png"),pygame.image.load(enemyPath+"enemydie4.png"),pygame.image.load(enemyPath+"enemydie5.png")]
enemyTimePass=[pygame.image.load(enemyPath+"enemyTimePass1.png"),pygame.image.load(enemyPath+"enemyTimePass2.png"),pygame.image.load(enemyPath+"enemyTimePass3.png"),pygame.image.load(enemyPath+"enemyTimePass4.png"),pygame.image.load(enemyPath+"enemyTimePass4.png"),pygame.image.load(enemyPath+"enemyTimePass3.png"),pygame.image.load(enemyPath+"enemyTimePass2.png"),pygame.image.load(enemyPath+"enemyTimePass1.png")]
background = pygame.image.load(miscPath+"danback.jpg")

#Initializing some of the global variables necessry for the functioning of the program
enemies = []
numberOfEnemies = 3
ammoLimit = (int)( 2 * numberOfEnemies)

#Defining the class of bullets  which will be used for the ranged attacks
class bullet:
     
    #The constructor for the class to initialize variables like the position, speed, direction etc.
    def __init__(self, x, y, direction):

        self.x = x
        self.y = y
        self.direction = direction
        self.vel = 35
        self.width = 35

    #Function to draw the sprite on the screen
    def draw(self,window):

        if self.direction == 'l':
            window.blit(bulletLeft,(self.x - self.width,self.y)) 

        elif self.direction == 'r':
            window.blit(bulletRight,(self.x,self.y))

    #The function to update the position of the bullet as it moves along
    def update(self, enemies):

        flag = 0

        if self.direction == 'r':   #getting the direction

            self.x += self.vel
            sign = 1

        elif self.direction == 'l':

            self.x -= self.vel
            sign = -1

        if self.x > 1300 or self.x < -100:
                bullets.remove(self)

        for Enemy in  enemies:          #Detecting the enemy

            if Enemy.setVisible == False:
                        continue

            if ((self.x + sign * self.vel) - Enemy.x) * (self.x - Enemy.x) <= 0:
                
                for Enemy in  enemies:

                    
                    if (self.direction == 'l' and Enemy.x <= self.x) or (self.direction == 'r' and Enemy.x >= self.x):
                        
                        closest = Enemy
                        break


                for Enemy in  enemies:

                    

                    if ((self.direction == 'l' and Enemy.x <= self.x) or (self.direction == 'r' and Enemy.x >= self.x)) and math.fabs(self.x - Enemy.x) < (self.x - closest.x):

                        closest = Enemy
                    

                closest.gunHit = True       #If the bullet hits the enemy it turns true
                bullets.remove(self)
                break

# The super class of all the sprites
class sprite:

    def __init__(self, x, y, width, height,direction):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.isJump = False
        self.counter = 0
        self.isWalk = False
        self.direction = direction
        self.isPunch = False
        self.idle = False
        self.vely=0
        self.Range = 300

#The class of platforms which blits the sprites onto the screen and also gets the positions for the sprites to jump
class platform:

    def __init__(self,x,y,width,height):

        self.x = x
        self.y = y
        self.width = width
        self.height = height

    # Blits the platforms onto the screen
    def draw(self,window):

        #Blits the base
        if (self.width == 1600):
           
            window.blit(platform3,(0,660))
            window.blit(platform3,(401,660))
            window.blit(platform3,(801,660))

        #Blits the left and right upper platforms
        elif(self.width == 300):
            
            window.blit(platform2,(100,400))
            window.blit(platform2,(800,400))

        #Blit the middle upper platform
        elif(self.width == 400):
            
            window.blit(platform1,(400,500))

#The class which takes care of the dan, the user controlled sprite in the game
#Subclass of the sprite class
class player(sprite):

    #Initialize all the variables of the player such as the health, location coordinates, velocity etc which dont belong to the superclass
    def __init__(self, x, y, width, height):
        
        sprite.__init__(self,x,y,width,height,'l')
        self.vel = 15
        self.hit = False
        self.health = 10
        self.setVisible = True
        self.isShoot = False
        self.kills = 0

    #Function to control all blitting of the player onto the screen according to the object's status
    def draw(self,window):

        #For the health bar
        window.blit(danHead, (10,25))

        if self.setVisible:
            
            pygame.draw.rect(window,(0,255,0),(65,30,self.health*10,30)) 
            
            if self.health == 0:
                self.setVisible = False
                pygame.mixer.Channel(1).play(pygame.mixer.Sound(soundPath+"danDie.ogg"), 0)   
            
            #While the sprite is walking
            if self.isWalk:

                if self.counter + 1  >= 2 * len(runLeft):
                    self.counter = 0
                
                #Determine the direction of walking
                if self.direction == 'l':
                    
                    window.blit(runLeft[self.counter/2],(self.x,self.y))
                    self.counter += 1
            
                elif self.direction == 'r':

                    window.blit(runRight[self.counter/2],(self.x,self.y))
                    self.counter += 1
            
            #Determine of the player is punching or not and accordingly draw the sprite
            elif self.isPunch:
                    
                    if self.direction == 'l':
                        window.blit(punchLeft[self.counter/2],(self.x,self.y))
                    else:    
                        window.blit(punchRight[self.counter/2],(self.x,self.y))                  
                    
                    if self.counter > 6:

                        self.counter = 0
                        self.isPunch = False

                    else:
                        self.counter += 1    

            #Jumping animations for the player
            elif self.isJump:
            
                if self.direction == 'l':
                        window.blit(jumpLeft,(self.x,self.y))
                
                else:
                        window.blit(jumpRight,(self.x,self.y))    
            
            #Shooting animations for the player
            elif self.isShoot:

                if dan.counter >= 4:

                    self.isShoot = False
                    self.counter = 0

                else :
                    self.counter += 1

                if self.direction == 'l':
                    window.blit(shootLeft,(self.x,self.y + 10))

                else:
                    window.blit(shootRight,(self.x,self.y + 10))
        

            else:

                if self.direction == 'l':
                    window.blit(standLeft,(self.x,self.y))
                
                else:
                    window.blit(standRight,(self.x,self.y))

        else:

            #Dying animations for the player

            if self.counter < 6*len(danDie):
                
                
                window.blit(danDie[int(self.counter/6)], (self.x,self.y))                    
                self.counter += 1
            if self.counter == 24:
                time.sleep(2)
                pygame.quit() 
                quit()              


#Making the object of the player class for further usage
dan = player(550, 0, 50, 80 )

#The class of the enemy sprites for controlling all their actions
#Sub class of the sprite class
class enemy(sprite):
        
    #The constructor which initializes the variables apart from the inherit ones
    def __init__(self):

        sprite.__init__(self,self.placeAtX(dan.x), 0, 0,0, 'l')
        self.health = 3
        self.setVisible = True
        self.vel = 5
        self.hitControl = 0
        self.gunHit = False
        self.vely = 0
        self.acc = 4
        self.height = 80
        self.width = 76
        self.isJump = True

    #Function to spawn more enemies as the ones alive die
    def spawnMore(self):

        numberOfEnemies = 3 + (int)(dan.kills/10)
        if len(enemies) < numberOfEnemies:

            enemies.append(enemy())

    #Function to place the enemies in a valid location
    def placeAtX(self,restrict):

        location = (random.randint(100, 1100)/5)*5
        for Enemy in enemies:
            if math.fabs(Enemy.x - location) <= 50:
                return self.placeAtX(restrict)
        
        if math.fabs( location - restrict ) <= 100: 
            return self.placeAtX(restrict)
        
        for Enemy in enemies:
            if math.fabs( location - Enemy.x ) <= 100 :
                return self.placeAtX(restrict)

        else:
            return location

    #Function to control the movement of the of the enemies as per requirement
    #This is the brain of the project, where the software determines what to do according to a set of parameters
    def move(self):
        
        #Normal walking
        if math.fabs(self.x-dan.x) <= self.Range and self.y > dan.y and not self.isJump:
            self.vely = -40
            self.y -= 1
            self.isJump = True

        if self.x < (dan.x-50) and math.fabs(self.x-dan.x) <= self.Range : 

            self.direction = 'r'
            self.x += self.vel
            self.isWalk = True
            self.idle = False
        
        elif self.x > (dan.x+50) and math.fabs(self.x-dan.x) <= self.Range  :

            self.direction = 'l'
            self.x -= self.vel
            self.isWalk = True
            self.idle = False
        
        elif (math.fabs(self.x-dan.x) > self.Range):

            self.idle = True
            self.isWalk = False
        
        if (math.fabs(self.x-dan.x) < self.Range) :

            self.Range = 1200

        else:
             
            self.isWalk = False

        #If the player is within range then he/she gets hit 
        if self.x >= dan.x-50 and self.x <= dan.x+50 and self.y == dan.y:

            self.hitControl += 1
            if self.hitControl == 20:
                
                pygame.mixer.Channel(1).play(pygame.mixer.Sound(soundPath+"danHit.wav"), 0)
                pygame.mixer.Channel(2).play(pygame.mixer.Sound(soundPath+"enemyAttack.ogg"), 0)
                self.isPunch = True
                self.hitControl = 0

            self.isWalk = False
            self.idle = False

        self.draw(window)

    #Function to implement the damage done on the enemies by the player
    def damage(self):
        
        flag = False            

        if self.x >= dan.x-50 and self.x <= dan.x+50 and self.y == dan.y:

            if dan.hit:
                self.health -= 1
                dan.hit = False
                if self.health == 0:
                    dan.kills += 1
                    self.counter = 0
                flag = True
                

        if self.gunHit:

            self.health -= 1
            self.gunHit = False
            if self.health == 0:
                    dan.kills += 1
                    self.counter = 0
            flag = True


        if self.health <= 0:

            self.setVisible = False
            self.Range = -1

            if self.counter == len(enemyDie):

                pygame.mixer.Channel(2).play(pygame.mixer.Sound(soundPath+"enemyDeath.ogg"), 0)

            if self.counter == 6 * len(enemyDie) - 1:
        
                enemies.remove(self)

        return flag    

    #Function to display anything like score or ammo as per the value passed to it
    def showValue(self,x,xpos):
        copy = x
        score = []
        if copy == 0:
            window.blit(digits[0], (xpos ,30))
            return 

        while copy > 0:
            score.append(copy%10)
            copy =(int)(copy / 10)
        
        copy = 0
        
        for digit in score:
            window.blit(digits[digit], (xpos - 30*copy,30))
            copy += 1
    # A function to draw the enemies onto the screen
    def draw(self, window):

        hit=self.damage()
        
        textStyle = pygame.font.SysFont('comicsans',50,True,True)
        
        text1 = textStyle.render('Score', 1,(255,0,0))

        window.blit(text1, (950,17))
        self.showValue(dan.kills,1100)
        window.blit(gunLogo, (490,25))
        self.showValue(ammoLimit,580)
        
        if self.setVisible:
            
            if dan.health == 0:
                        
                self.isPunch = False
                hit = False
                self.isJump = False                
                
            elif self.isJump:
            
                if self.direction == 'l':
                        window.blit(enemyTimePass[0],(self.x,self.y))
                        
                
                else:
                        window.blit(enemyTimePass[0],(self.x,self.y))
                        

            if self.isWalk and not hit and not self.isJump:

                if self.counter + 1 >= 5 * len(enemyRunLeft):

                    self.counter = 0

                if self.direction == 'l':
                
                    window.blit(enemyRunLeft[int(self.counter/5)],(self.x, self.y))
                    self.counter += 1 

                if self.direction == 'r':
                    
                    window.blit(enemyRunRight[int(self.counter/5)], (self.x, self.y))
                    self.counter += 1 
            
            
            elif self.isPunch and self.y == dan.y and not hit and self.y == dan.y:

                if self.counter == len(enemyPunchLeft)-1:
                    dan.health -= 1

                if self.direction == 'l':

                    if self.counter < 4*len(enemyPunchRight):

                        window.blit(enemyPunchLeft[int(self.counter/4)], (self.x,self.y))
                        self.counter += 1

                else:    

                    if self.counter < 4*len(enemyPunchRight):

                        window.blit(enemyPunchRight[int(self.counter/4)], (self.x,self.y))
                        self.counter += 1

                if self.counter > 4*len(enemyPunchLeft)-1:

                    self.counter = 0
                    self.isPunch = False
    
            elif hit and self.y == dan.y:
                
                if self.counter < len(enemyHit):
                    window.blit(enemyHit[int(self.counter)], (self.x, self.y))
                    self.counter+=1

                if self.counter > 4*len(enemyHit):
                    self.counter = 0
            

            elif self.idle and not self.isWalk:
                if self.counter < 4*len(enemyTimePass):

                    window.blit(enemyTimePass[int(self.counter/4)], (self.x,self.y))
                    
                    self.counter += 1

                if self.counter > 4*len(enemyPunchLeft)-1:

                    self.counter = 0
            else:

                if self.direction == 'l':
                    
                    window.blit(enemyStandLeft,(self.x,self.y))

                else:
                    
                    window.blit(enemyStandRight,(self.x,self.y))
        
        else:
            
            
            if self.counter < 6*len(enemyDie):

                window.blit(enemyDie[int(self.counter/6)], (self.x,self.y))                    
                self.counter += 1
           
#List of enemies to store their attributes and control them accordingly
enemies=[enemy(), enemy(), enemy()]

#A custom defined function to get the sign of any variable passed to it
def signum(x):
    
    if x == 0:
        return 1
    else:
        return x/math.fabs(x)

#A list to store the objects of the bullet sprites shot by the player
bullets = []

#Master draw function to draw everything else required as well
def draw():
    

    window.blit(background,(0,0))

    

    for p in platforms:    
        p.draw(window)

    dan.draw(window)

    for Enemy in enemies:
        Enemy.draw(window)
    
    #Drawing the bullets
    for b in bullets:
        b.draw(window)    

    #Updating the location of the bullets as they move
    distance = []
    for b in bullets:

            b.update(enemies)

    pygame.display.update()

#Calling the main function
if __name__ =="__main__":
    
    #Runs while the flag is true
    flag = True
    clock = pygame.time.Clock()
    
    #List to store the positions of the platforms
    platforms = [platform(0,660,1600,40), platform(400,500,400,40), platform(100,400,300,40), platform(800, 400,300,40)]
    
    #While the execution is required to run
    while flag:
        
        clock.tick(15)          #The frames per second at which the screen refreshes
        dan.acc = 4
        for e in enemies:
            e.acc = 4

        #Get the keys pressed on the keyboard
        keys = pygame.key.get_pressed()
            
        

              
                  
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                flag = False
            
            if event.type == pygame.KEYDOWN:    
            
                if event.key == pygame.K_a and not dan.isJump and not dan.isPunch and not dan.isShoot and dan.setVisible:
                    
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound(soundPath+"danPunch.ogg"),0)
                    dan.isWalk = False
                    dan.counter = 0
                    dan.isPunch = True   
                    dan.hit = True
                
                if event.key == pygame.K_UP and not dan.isJump and not dan.isPunch and not dan.isShoot and dan.setVisible:

                    dan.isJump = True
                    dan.vely = -40
                    dan.y -= 1
                    dan.counter = 10
                    dan.isWalk = False
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound(soundPath+"danJump.ogg"), 0)

                if event.key == pygame.K_s and not dan.isJump and not dan.isPunch and not dan.isShoot and not dan.isWalk and dan.setVisible:
                    
                    if dan.kills % 10 == 0 and dan.kills > 0:
                        ammoLimit += (int)(2 * numberOfEnemies)

                    if ammoLimit > 0:
                        dan.isShoot = True    
                        dan.isWalk = False
                        dan.counter = 0
                        ammoLimit -= 1
                        bullets.append(bullet(dan.x,dan.y + 40, dan.direction))
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound(soundPath+"danGun.ogg"), 0)
                    else:
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound(soundPath+"outOfAmmo.wav"), 0)

        
        if not dan.isPunch:

            if keys[pygame.K_LEFT] and dan.x>dan.vel and dan.setVisible:
                
                if dan.kills % 10 == 0 and dan.kills > 0:
                        ammoLimit += (int)(1.5 * numberOfEnemies)

                dan.x -= dan.vel
                dan.direction = 'l'
                
                if not dan.isJump:
                    dan.isWalk = True
                
                for Enemy in enemies:
                    if math.fabs(dan.x - Enemy.x) < 10 +dan.width  and dan.y == Enemy.y:
                        if signum(dan.x - Enemy.x) >= 0:
                            dan.x+=dan.vel
                            dan.isWalk = False

            elif keys[pygame.K_RIGHT] and dan.x< 1200 - dan.width - dan.vel and dan.setVisible :

                dan.x += dan.vel
                dan.direction = 'r'
                
                if not dan.isJump:
                    dan.isWalk = True

                for Enemy in enemies:
                    if math.fabs(dan.x - Enemy.x)< 10 + dan.width and dan.y == Enemy.y:
                        if signum(dan.x - Enemy.x) < 0:
                            dan.x-=dan.vel
                            dan.isWalk = False
                
        if not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
            
            dan.isWalk = False


        for p in platforms:

            if (((dan.y + dan.height) < p.y and (dan.y + dan.height + dan.vely + dan.acc) > p.y) or (dan.y + dan.height) == p.y) and ((dan.x + dan.width/2) > p.x and (dan.x + dan.width/2) < (p.x + p.width)):

                dan.vely = 0
                dan.acc = 0
                dan.y = p.y - dan.height 
                dan.isJump = False

            for e in enemies:

                if (((e.y + e.height) < p.y and (e.y + e.height + e.vely + e.acc) > p.y) or (e.y + e.height) == p.y) and ((e.x + e.width/2) > p.x and (e.x + e.width/2) < (p.x + p.width)):

                    e.vely = 0
                    e.acc = 0
                    e.y = p.y - e.height 
                    e.isJump = False



        

                 
             
        dan.vely += dan.acc
        dan.y += dan.vely     

        for Enemy in enemies:

            Enemy.vely += Enemy.acc
            Enemy.y += Enemy.vely

            if Enemy.health > 0:
                Enemy.spawnMore()
        
        #As long as the player is alive
        if dan.health > 0:
            
            for Enemy in  enemies:
                
                Enemy.move()
          
        draw()        