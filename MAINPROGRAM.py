
'''
From: Hongjun Han
For: Ms. Wun
Date: May 23, 2014
Program Purpose: Displaying a multiplayer game to entertain the user
'''
#Import & initialize the pygame module
import pygame
from pygame.locals import *  #This is not necessary for most games, but can simplify some things
pygame.init()


class map():

    mapchoice1=0    #Choose of each map
    playerremain=0  #Number of player remained in the game
    maptxt=[]       #The position of wall and space
    walllist=[]     #List of wall in the map
    bomb=[]         #List of bomb in the map
    playeringame=[] #List of character in the map
    banana=[]

    '''
    Pre: choice of map and player number get inputted
    Post: Initialize the map
    Purpose: To start the map
    '''
    def __init__(self,choice,play):
        self.mapchoice1=0
        self.playerremain=0
        self.maptxt=[]
        self.walllist=[]                #Clear everything as empty
        self.bomb=[]
        self.playeringame=[]
        self.banana=[]

        self.playerremain=play          #Add the information user inputted to class
        self.mapchoice1=choice
        mappp=open(maptxtfile[choice],"r")
        for i in range (8):
            self.maptxt.append(mappp.readline())    #Append the shape of the map from the txtfile

        for i in range (play):
            self.playeringame.append(character(playerchoice[i],i+1))    #Initialize the character class assigned to each player


        for i in range (8):
            for r in range (12):
                if self.maptxt[i][r]=="1":                                          #Assume map is first at 8x12 grids with 75x75 pixel per grids
                    self.walllist.append(wall(75*(r+1)-15,82+75*(i-1)))             #If the wall type is one create and append the wall class
                if self.maptxt[i][r]=="2":
                    self.walllist.append(destructablewall(75*(r+1)-15,82+75*(i-1))) #If it's 2 create and append the destrucable wall class


    '''
    Pre: The map is initialized
    Post: Elements of the map posted on screen
    Purpose: To output the map
    '''
    def printmap(self):
        background1 = pygame.Surface(size)
        background1 = background1.convert()             #Place a black background at the back
        background1.fill((0, 0, 0))
        screen.blit(background1, (0,0))

        waitbomb1=pygame.image.load("waitbomb1.png")    #Load image of bomb at waiting
        waitbomb2=pygame.image.load("waitbomb2.png")


        mapbackground= pygame.image.load(actualmap[self.mapchoice1]) #load an image as a Surface
        mapbackground = mapbackground.convert()





        wallpic= pygame.image.load(mapwall[self.mapchoice1]) #load an image of wall

        badwall= pygame.image.load(mapbadwall[self.mapchoice1]) #load an image of desctructable wall

        bananapic = pygame.image.load("banana.png") #load an image as the banana

        screen.blit(mapbackground, (62,0))  #Paste the map background on


        for i in range (len(self.bomb)):    #For each bomb avaiable:
            if self.bomb[i].state==0:
                screen.blit(waitbomb1, (self.bomb[i].x,self.bomb[i].y)) #if the bomb is waiting and it's state 1 post state 1 picture
            if self.bomb[i].state==1:
                screen.blit(waitbomb2, (self.bomb[i].x,self.bomb[i].y)) #if the bomb is waiting and it's state 2 post state 2 picture
            if self.bomb[i].state==2:
                screen.blit(explodeimage[self.bomb[i].explodestate], (self.bomb[i].x,self.bomb[i].y))   #If bomb is exploding put explosion image depending on the state of explosion at 3x3 grid
                screen.blit(explodeimage[self.bomb[i].explodestate], (self.bomb[i].x-75,self.bomb[i].y))
                screen.blit(explodeimage[self.bomb[i].explodestate], (self.bomb[i].x+75,self.bomb[i].y))
                screen.blit(explodeimage[self.bomb[i].explodestate], (self.bomb[i].x,self.bomb[i].y-75))
                screen.blit(explodeimage[self.bomb[i].explodestate], (self.bomb[i].x,self.bomb[i].y+75))

        for i in range (len(self.walllist)):    #For each wall avaiable
            if self.walllist[i].destructable==False:
                screen.blit(wallpic, (self.walllist[i].x,(self.walllist[i].y)))     #If wall is not destructable blit the non-destrucablt wall
            else:
                screen.blit(badwall, (self.walllist[i].x,(self.walllist[i].y)))     #Else blitz the normal wall

        for r in range (len(self.banana)):
            screen.blit(bananapic, (self.banana[r].x,(self.banana[r].y)))

        for m in range(len(self.playeringame)):     #For each character class avaiable:
             facingdirection=""
             if self.playeringame[m].facing==1:
                facingdirection="front"
             elif self.playeringame[m].facing==2:           #Blitz the image base on the direction and character type of the character
                facingdirection="back"
             elif self.playeringame[m].facing==3:
                facingdirection="left"
             elif self.playeringame[m].facing==4:
                facingdirection="right"
             screen.blit(pygame.image.load("c"+str(self.playeringame[m].charactertype)+facingdirection+str(self.playeringame[m].walkstyle)+".png"), (self.playeringame[m].x,(self.playeringame[m].y)))

        for i in range (len(self.playeringame)):                #Output the health for each player on specific position
            my_font = pygame.font.SysFont("comicsansms", 20)
            label2 = my_font.render("HP:"+str(self.playeringame[i].life), True, (255,255, 255))
            screen.blit(label2, lifeposition[i])
        pygame.display.flip()



class character():
    dead=False      #if he is dead
    x=0
    y=0             #Position
    walkstyle=1     #State of walking
    facing=1        #Facing direction
    life=0          #Life of the character
    speed=0         #Walking speed
    bombnumber=0    #Bomb placed
    charactertype=0 #character type
    playernumber=0  #playernumber
    numberofbanana=0
    numberofgernade=0
    bombradius=0            #radius of bomb
    '''
    Pre: character type and player number is inputtd
    Post: class in created
    Purpose: to open up a class
    '''
    def __init__(self,charactertype,playernumber):
        self.life=life
        self.charactertype=charactertype    #Intialize the variables
        self.playernumber=playernumber
        if (charactertype==1):              #Type 1 walks faster
            self.speed=1.875
        else:
            self.speed=1.25
        if (charactertype==2):              #Type 2 has bigger bomb radius
            self.bombradius=300
        else:
            self.bombradius=225
        if (charactertype==3):
            self.numberofbanana=4
            self.numberofgernade=4
        else:
            self.numberofbanana=3
            self.numberofgernade=3
        if playernumber==1:                 #Initialize start position and facing direction according to their player number
            self.x=62
            self.y=0
            self.facing=1
        elif playernumber==2:
            self.x=887
            self.y=0
            self.facing=1
        elif playernumber==3:
            self.x=62
            self.y=525
            self.facing=2
        elif playernumber==4:
            self.x=887
            self.y=525
            self.facing=2


   # def setbomb():




class bomb():
    by=-1
    cycle=0             #Cycle of the bomb, After 2 cycles it will explode
    x=0                 #Position of the bomb
    y=0
    state=0             #When waiting period, how the bomb will look like
    explodestate=0      #When exploding, how the bomb will look like
    '''
    Pre: Input x y position as well as who put it
    Post: Class created for bomb
    Purpose:Create the class for bomb
    '''
    def __init__(self,first,second,person):
        self.x=first
        self.y=second       #Assign the value to the attributes
        self.by=person
    '''
class gernade(bomb):
    target=0
    speed=0
    def fly(self):
        flyover()
    '''

class banana():
    x=0
    y=0
    def __init__(self,length,width):    #not used
        self.x=length
        self.y=width


class wall():
    x=0
    y=0     #Position
    destructable=False  #If the wall can be destroyed or not
    '''
    Pre: The x and y are inputted
    Post: Class is created
    Purpose:Create the class
    '''
    def __init__(self,length,width):
        self.x=length       #Assign the value to attributes
        self.y=width

#Inheritance and polymorphism on wall class
class destructablewall(wall):
    destructable=True   #Change this attribute to true others remain the same


#Map: iceworld, ocean, dessert and railroad
inmainmenu=True
inpregame=False
instructionmenu=False   #The boolean that shows which page the program is on
controlmenu=False
inselection=False
ingame=False
gamestart=False
instructionposition=100     #Start position for the instruction
preview=["snowpreview.png","oceanpreview.png","woodpreview.png"]
actualmap=["snowbackground.png","oceanbackground.png","woodbackground.jpg"] #Map preview on pregame setting, wall and background for each different map
maptxtfile=["snow.txt","ocean.txt","wood.txt"]
mapwall=["snowwall.png","oceanwall.png","woodwall.png"]
mapbadwall=["snowbadwall.png","oceanbadwall.png","woodbadwall.png"]
characterlist=["1","2","3"]                                                 #Character selection avaiable
playerchoice=[]                                                             #What player chooses
playercharacteroutput=[(144,219),(750,218),(150,408),(747,407)]             #Where character should start
lifeposition=[(8,14),(977,15),(9,545),(977,545)]                            #Where hp should be outputted



'''
pre:    The character moving that direction shown
post:   Return a boolean that shows if it touches anything
purpose: Check if character can move or not depending on if he collides with other things
'''
def checkcollision(charactername,direction):
    fail=False      #Assume it can move at first
    try:
        if direction=="left":
            if newmap.playeringame[charactername].x-1<62:   #Cannot walk outside of the map else return True
                fail=True
            for i in range (len(newmap.playeringame)):
                if i!=charactername:

                    if ((newmap.playeringame[i].x)>=(newmap.playeringame[charactername].x-newmap.playeringame[charactername].speed*10-50)) and ((newmap.playeringame[i].x)<=(newmap.playeringame[charactername].x-50)) and (newmap.playeringame[i].y<=newmap.playeringame[charactername].y) and (newmap.playeringame[i].y>=newmap.playeringame[charactername].y-50):
                        fail=True
                    if ((newmap.playeringame[i].x)>=(newmap.playeringame[charactername].x-newmap.playeringame[charactername].speed*10-50)) and ((newmap.playeringame[i].x)<=(newmap.playeringame[charactername].x-50)) and (newmap.playeringame[i].y>=newmap.playeringame[charactername].y) and (newmap.playeringame[i].y<=newmap.playeringame[charactername].y+50):
                        fail=True                           #Cannot go through other character else return True
                                                            #-If next step of character will walk into others
            for i in range (len(newmap.walllist)):


                if ((newmap.walllist[i].x)>=(newmap.playeringame[charactername].x-newmap.playeringame[charactername].speed*10-50)) and ((newmap.walllist[i].x)<=(newmap.playeringame[charactername].x-50)) and (newmap.walllist[i].y<=newmap.playeringame[charactername].y) and (newmap.walllist[i].y>=newmap.playeringame[charactername].y-50):
                        fail=True
                if ((newmap.walllist[i].x)>=(newmap.playeringame[charactername].x-newmap.playeringame[charactername].speed*10-50)) and ((newmap.walllist[i].x)<=(newmap.playeringame[charactername].x-50)) and (newmap.walllist[i].y>=newmap.playeringame[charactername].y) and (newmap.walllist[i].y<=newmap.playeringame[charactername].y+50):
                        fail=True
                                                            #Cannot go through other walls else return True
                                                            #-If next step of character will walk into other walls
            for i in range (len(newmap.bomb)):


                if ((newmap.bomb[i].x)>=(newmap.playeringame[charactername].x-newmap.playeringame[charactername].speed*10-50)) and ((newmap.bomb[i].x)<=(newmap.playeringame[charactername].x-50)) and (newmap.bomb[i].y<=newmap.playeringame[charactername].y) and (newmap.bomb[i].y>=newmap.playeringame[charactername].y-50):
                        fail=True
                if ((newmap.bomb[i].x)>=(newmap.playeringame[charactername].x-newmap.playeringame[charactername].speed*10-50)) and ((newmap.bomb[i].x)<=(newmap.playeringame[charactername].x-50)) and (newmap.bomb[i].y>=newmap.playeringame[charactername].y) and (newmap.bomb[i].y<=newmap.playeringame[charactername].y+50):
                        fail=True
                                                            #Cannot go through other bombs else return True
                                                            #-If next step of character will walk into other bombs
        if direction=="right":
            if newmap.playeringame[charactername].x+1>887:
                fail=True
            for i in range (len(newmap.playeringame)):
                if i!=charactername:
                    if ((newmap.playeringame[i].x)<=(newmap.playeringame[charactername].x+newmap.playeringame[charactername].speed*10+50)) and ((newmap.playeringame[i].x)>=(newmap.playeringame[charactername].x+50)) and (newmap.playeringame[i].y<=newmap.playeringame[charactername].y) and (newmap.playeringame[i].y>=newmap.playeringame[charactername].y-50):
                        fail=True
                    if ((newmap.playeringame[i].x)<=(newmap.playeringame[charactername].x+newmap.playeringame[charactername].speed*10+50)) and ((newmap.playeringame[i].x)>=(newmap.playeringame[charactername].x+50)) and (newmap.playeringame[i].y>=newmap.playeringame[charactername].y) and (newmap.playeringame[i].y<=newmap.playeringame[charactername].y+50):
                        fail=True
            for i in range (len(newmap.walllist)):


                if ((newmap.walllist[i].x)<=(newmap.playeringame[charactername].x+newmap.playeringame[charactername].speed*10+50)) and ((newmap.walllist[i].x)>=(newmap.playeringame[charactername].x+50)) and (newmap.walllist[i].y<=newmap.playeringame[charactername].y) and (newmap.walllist[i].y>=newmap.playeringame[charactername].y-50):
                        fail=True
                if ((newmap.walllist[i].x)<=(newmap.playeringame[charactername].x+newmap.playeringame[charactername].speed*10+50)) and ((newmap.walllist[i].x)>=(newmap.playeringame[charactername].x+50)) and (newmap.walllist[i].y>=newmap.playeringame[charactername].y) and (newmap.walllist[i].y<=newmap.playeringame[charactername].y+50):
                        fail=True
    #
            for i in range (len(newmap.bomb)):                  #same as the above


                if ((newmap.bomb[i].x)<=(newmap.playeringame[charactername].x+newmap.playeringame[charactername].speed*10+50)) and ((newmap.bomb[i].x)>=(newmap.playeringame[charactername].x+50)) and (newmap.bomb[i].y<=newmap.playeringame[charactername].y) and (newmap.bomb[i].y>=newmap.playeringame[charactername].y-50):
                        fail=True
                if ((newmap.bomb[i].x)<=(newmap.playeringame[charactername].x+newmap.playeringame[charactername].speed*10+50)) and ((newmap.bomb[i].x)>=(newmap.playeringame[charactername].x+50)) and (newmap.bomb[i].y>=newmap.playeringame[charactername].y) and (newmap.bomb[i].y<=newmap.playeringame[charactername].y+50):
                        fail=True


        if direction=="up":
            if newmap.playeringame[charactername].y-1<0:        #same as the above
                fail=True
            for i in range (len(newmap.playeringame)):
                if i!=charactername:

                    if ((newmap.playeringame[i].y)>=(newmap.playeringame[charactername].y-newmap.playeringame[charactername].speed*10-50)) and ((newmap.playeringame[i].y)<=(newmap.playeringame[charactername].y-50)) and (newmap.playeringame[i].x<=newmap.playeringame[charactername].x) and (newmap.playeringame[i].x>=newmap.playeringame[charactername].x-50):
                        fail=True
                    if ((newmap.playeringame[i].y)>=(newmap.playeringame[charactername].y-newmap.playeringame[charactername].speed*10-50)) and ((newmap.playeringame[i].y)<=(newmap.playeringame[charactername].y-50)) and (newmap.playeringame[i].x>=newmap.playeringame[charactername].x) and (newmap.playeringame[i].x<=newmap.playeringame[charactername].x+50):
                        fail=True
            for i in range (len(newmap.walllist)):


                if ((newmap.walllist[i].y)>=(newmap.playeringame[charactername].y-newmap.playeringame[charactername].speed*10-50)) and ((newmap.walllist[i].y)<=(newmap.playeringame[charactername].y-50)) and (newmap.walllist[i].x<=newmap.playeringame[charactername].x) and (newmap.walllist[i].x>=newmap.playeringame[charactername].x-50):
                        fail=True
                if ((newmap.walllist[i].y)>=(newmap.playeringame[charactername].y-newmap.playeringame[charactername].speed*10-50)) and ((newmap.walllist[i].y)<=(newmap.playeringame[charactername].y-50)) and (newmap.walllist[i].x>=newmap.playeringame[charactername].x) and (newmap.walllist[i].x<=newmap.playeringame[charactername].x+50):
                        fail=True
            for i in range (len(newmap.bomb)):
                                                                            #same as the above

                if ((newmap.bomb[i].y)>=(newmap.playeringame[charactername].y-newmap.playeringame[charactername].speed*10-50)) and ((newmap.bomb[i].y)<=(newmap.playeringame[charactername].y-50)) and (newmap.bomb[i].x<=newmap.playeringame[charactername].x) and (newmap.bomb[i].x>=newmap.playeringame[charactername].x-50):
                        fail=True
                if ((newmap.bomb[i].y)>=(newmap.playeringame[charactername].y-newmap.playeringame[charactername].speed*10-50)) and ((newmap.bomb[i].y)<=(newmap.playeringame[charactername].y-50)) and (newmap.bomb[i].x>=newmap.playeringame[charactername].x) and (newmap.bomb[i].x<=newmap.playeringame[charactername].x+50):
                        fail=True
        if direction=="down":
            if newmap.playeringame[charactername].y+1+75>600:
                fail=True
            for i in range (len(newmap.playeringame)):
                if i!=charactername:
                    if ((newmap.playeringame[i].y)<=(newmap.playeringame[charactername].y+newmap.playeringame[charactername].speed*10+50)) and ((newmap.playeringame[i].y)>=(newmap.playeringame[charactername].y+50)) and (newmap.playeringame[i].x<=newmap.playeringame[charactername].x) and (newmap.playeringame[i].x>=newmap.playeringame[charactername].x-50):
                        fail=True
                    if ((newmap.playeringame[i].y)<=(newmap.playeringame[charactername].y+newmap.playeringame[charactername].speed*10+50)) and ((newmap.playeringame[i].y)>=(newmap.playeringame[charactername].y+50)) and (newmap.playeringame[i].x>=newmap.playeringame[charactername].x) and (newmap.playeringame[i].x<=newmap.playeringame[charactername].x+50):
                        fail=True
            for i in range (len(newmap.walllist)):

                                                    #same as the above
                if ((newmap.walllist[i].y)<=(newmap.playeringame[charactername].y+newmap.playeringame[charactername].speed*10+50)) and ((newmap.walllist[i].y)>=(newmap.playeringame[charactername].y+50)) and (newmap.walllist[i].x<=newmap.playeringame[charactername].x) and (newmap.walllist[i].x>=newmap.playeringame[charactername].x-50):
                        fail=True
                if ((newmap.walllist[i].y)<=(newmap.playeringame[charactername].y+newmap.playeringame[charactername].speed*10+50)) and ((newmap.walllist[i].y)>=(newmap.playeringame[charactername].y+50)) and (newmap.walllist[i].x>=newmap.playeringame[charactername].x) and (newmap.walllist[i].x<=newmap.playeringame[charactername].x+50):
                        fail=True
    #
            for i in range (len(newmap.bomb)):


                if ((newmap.bomb[i].y)<=(newmap.playeringame[charactername].y+newmap.playeringame[charactername].speed*10+50)) and ((newmap.bomb[i].y)>=(newmap.playeringame[charactername].y+50)) and (newmap.bomb[i].x<=newmap.playeringame[charactername].x) and (newmap.bomb[i].x>=newmap.playeringame[charactername].x-50):
                        fail=True
                if ((newmap.bomb[i].y)<=(newmap.playeringame[charactername].y+newmap.playeringame[charactername].speed*10+50)) and ((newmap.bomb[i].y)>=(newmap.playeringame[charactername].y+50)) and (newmap.bomb[i].x>=newmap.playeringame[charactername].x) and (newmap.bomb[i].x<=newmap.playeringame[charactername].x+50):
                        fail=True
    except:
        none
    return (fail)   #Return the result of the collision calculation
    '''
    pre: map class initialized
    post: characters are selected from players
    purpose: allow character to select player
    '''
def characterselect():

    for i in range (player):
        playerchoice.append(1)
    while len(playerchoice)<4:
        playerchoice.append(0)
    characterselection= pygame.image.load("characterselect.png")    #blit the background page
    characterselection = characterselection.convert()
    screen.blit(characterselection, (0,0))
    pygame.display.flip()

    for r in range (len(playercharacteroutput)):
        if playerchoice[r]==0:
            screen.blit(pygame.image.load("disable.png"), playercharacteroutput[r])     #If there is no such character make it diabled for select
            pygame.display.flip()

        if playerchoice[r]==1:
            screen.blit(pygame.image.load("character1.png"), playercharacteroutput[r])  #The chatacter type is outputted with the selection
            pygame.display.flip()
        if playerchoice[r]==2:
            screen.blit(pygame.image.load("character2.png"), playercharacteroutput[r])
            pygame.display.flip()
        if playerchoice[r]==3:
            screen.blit(pygame.image.load("character3.png"), playercharacteroutput[r])
            pygame.display.flip()





'''
Pre: Map is initialized
post: control page outputted
purpose: output control page
'''
def controlpage():
    control= pygame.image.load("controlpage.png") #load an image as a Surface
    control = control.convert()
    screen.blit(control, (0,0))
    pygame.display.flip()


'''
Pre: Map is initialized
post: instruction page outputted
purpose: output instruction page
'''
def instructionpage():
    instruction= pygame.image.load("instructionpage.png")   #Load in the background
    instruction = instruction.convert()
    screen.blit(instruction, (0,0))

    instructionword = pygame.image.load("instructionword.png")  #Load in the word


    colorkey = instructionword.get_at((1,1))
    instructionword.set_colorkey(colorkey, pygame.RLEACCEL)

    screen.blit(instructionword, (0,instructionposition))

    instructioncover = pygame.image.load("instructioncover.png") #Load top of the background


    colorkey = instructioncover.get_at((200,200))
    instructioncover.set_colorkey(colorkey, pygame.RLEACCEL)        #Output with orders

    screen.blit(instructioncover, (0,0))
    pygame.display.flip()



'''
Pre: Play button is pressed
post: game setting is selected
purpose: select setting of the game
'''
def pregame():
    pregamemenu= pygame.image.load("pregame.png") #load an image as a Surface   #Output background
    pregamemenu = pregamemenu.convert()
    screen.blit(pregamemenu, (0,0))


    my_font = pygame.font.SysFont("georgia", 50)        #Set the font
    lifepoint = my_font.render(str(life), False, (0,0,0))
    playernumber = my_font.render(str(player), False, (0,0,0))

    screen.blit(lifepoint, (563,218))                   #Output lifepoint and playernumber
    screen.blit(playernumber, (505,340))


    pregamemenu= pygame.image.load(preview[mapchoice-1]) #Output map input
    pregamemenu = pregamemenu.convert()
    screen.blit(pregamemenu, (475,489))

    pygame.display.flip()


'''
Pre: the music file the there and map is initialized
post: sound is outputted
purpose: output the sound
'''
def bouncesound():
    pygame.mixer.music.load("bounce.mp3") #used for a sound effect
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play()


'''
Pre: the music file the there and map is initialized
post: sound is outputted
purpose: output the sound
'''
def flashsound():
    pygame.mixer.music.load("flash.mp3") #used for a sound effect
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play()



'''
Pre: the music file the there and map is initialized
post: sound is outputted
purpose: output the sound
'''
def buttonsound():
    pygame.mixer.music.load("button.mp3") #used for a sound effect
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play()

'''
pre: program is started
post: animation is performed
purpose: to post an animation depending on acceleration, velocity and displacement
'''
def bounce(img,accelerationx,accelerationy,velocityx,velocityy,positionx,positiony):


    for i in range (20):
        screen.blit(img,(positionx,positiony))

        pygame.display.flip()
        clock.tick(30)
        screen.blit(background, (positionx, positiony), pygame.Rect(positionx, positiony,440,80))   #Bounce once
        pygame.display.flip()
        positionx=positionx+velocityx
        positiony=positiony+velocityy
        velocityx=velocityx+accelerationx
        velocityy=velocityy+accelerationy


    velocityy=-20
    accelerationy=2
    bouncesound()
    for i in range (20):
        screen.blit(img,(positionx,positiony))

        pygame.display.flip()
        clock.tick(30)
        screen.blit(background, (positionx, positiony), pygame.Rect(positionx, positiony,440,80))   #Bounce another times
        pygame.display.flip()
        positionx=positionx+velocityx
        positiony=positiony+velocityy
        velocityx=velocityx+accelerationx
        velocityy=velocityy+accelerationy
    bouncesound()

    velocityy=-18
    accelerationy=2
    for i in range (20):
        screen.blit(img,(positionx,positiony))

        pygame.display.flip()
        clock.tick(30)
        screen.blit(background, (positionx, positiony), pygame.Rect(positionx, positiony,440,80))   #Bounce another times
        pygame.display.flip()
        positionx=positionx+velocityx
        positiony=positiony+velocityy
        velocityx=velocityx+accelerationx
        velocityy=velocityy+accelerationy

    bouncesound()
    velocityy=-10
    for i in range (11):
        screen.blit(img,(positionx,positiony))

        pygame.display.flip()
        clock.tick(30)
        screen.blit(background, (positionx, positiony), pygame.Rect(positionx, positiony,440,80))   #Bounce
        pygame.display.flip()
        positionx=positionx+velocityx
        positiony=positiony+velocityy
        velocityx=velocityx+accelerationx
        velocityy=velocityy+accelerationy
    bouncesound()
    screen.blit(img,(positionx,positiony))
    pygame.display.flip()

    line=pygame.image.load("line1.png")
    line=line.convert()
    colorkey = line.get_at((1,1))
    line.set_colorkey(colorkey, pygame.RLEACCEL)

    currenty=200
    currentx=300

    for i in range (12):
        currentx=currentx+10
        screen.blit(line,(currentx,currenty))

        pygame.display.flip()
        clock.tick(100)
        screen.blit(background, (currentx,currenty), pygame.Rect(currentx,currenty,440,80))     #Move a line under it
        pygame.display.flip()
    flashsound()
    screen.blit(line,(currentx,currenty))
    pygame.display.flip()







#Set-up the main display window and the background
size = (1024,600)  #<-- that is a tuple (just like a list) for width & height
screen = pygame.display.set_mode(size) #<-- screen is now a Surface type object
pygame.display.set_caption("Bomberman") #<-- caption appears in the title bar
pygame.display.flip()

#The game loop
clock = pygame.time.Clock() #<-- used to control the frame rate
keep_going = True 	        #<-- a 'flag' variable for the game loop condition
pygame.display.flip()


#440,80

background = pygame.image.load("gamepagebackground.png") #load an image as a background
background = background.convert() #need to convert it after we have set-up the scree


selectbackground= pygame.image.load("gamepagebackgroundselect.jpg") #load a background for the map
selectbackground = selectbackground.convert()


word=pygame.image.load("gamepagefont.png")
word=word.convert()

'''
pre:main menu is selected
post: initialize everything
purpose: output main menu and reinitialize everything
'''
def mainmenustuff():

    inmainmenu=True
    inpregame=False
    instructionmenu=False
    controlmenu=False
    inselection=False
    ingame=False
    gamestart=False
    instructionposition=100
    preview=["snowpreview.png","oceanpreview.png","woodpreview.png"]
    actualmap=["snowbackground.png","oceanbackground.png","woodbackgroundw.png"]    #Reinitialize everything
    maptxtfile=["snow.txt","ocean.txt","wood.txt"]
    mapwall=["snowwall.png","oceanwall.png","woodwall.png"]
    mapbadwall=["snowbadwall.png","oceanbadwall.png","woodbadwall.png"]
    characterlist=["1","2","3"]
    playerchoice=[]
    playercharacteroutput=[(144,219),(750,218),(150,408),(747,407)]
    lifeposition=[(8,14),(977,15),(9,545),(977,545)]

    life=1
    player=2
    currentmap=-1
    mapchoice=1
    screen.blit(background, (0,0))
    pygame.display.flip()

    colorkey = word.get_at((1,1))
    word.set_colorkey(colorkey, pygame.RLEACCEL)


    pygame.display.flip()

    bounce(word,0,0.5,4,0,150,30)


mainmenustuff() #Enter main menu

life=1
player=2            #Intialize variables for change
currentmap=-1
mapchoice=1


onbutton=False      #See if the mouse is on button



bomb1 = pygame.image.load("bomb1.png")          #Load the animation picture of bomb 1-10
bomb1 = bomb1.convert()
colorkey = bomb1.get_at((1,1))
bomb1.set_colorkey(colorkey, pygame.RLEACCEL)


bomb2 = pygame.image.load("bomb2.png") #load an image as a Surface
bomb2 = bomb2.convert() #need to convert it after we have set-up the screen
colorkey = bomb2.get_at((1,1))
bomb2.set_colorkey(colorkey, pygame.RLEACCEL)


bomb4 = pygame.image.load("bomb4.png") #load an image as a Surface
bomb4 = bomb4.convert() #need to convert it after we have set-up the screen
colorkey = bomb4.get_at((1,1))
bomb4.set_colorkey(colorkey, pygame.RLEACCEL)


bomb5 = pygame.image.load("bomb5.png") #load an image as a Surface
bomb5 = bomb5.convert() #need to convert it after we have set-up the screen
colorkey = bomb5.get_at((1,1))
bomb5.set_colorkey(colorkey, pygame.RLEACCEL)


bomb6 = pygame.image.load("bomb6.png") #load an image as a Surface
bomb6 = bomb6.convert() #need to convert it after we have set-up the screen
colorkey = bomb6.get_at((1,1))
bomb6.set_colorkey(colorkey, pygame.RLEACCEL)

bomb7 = pygame.image.load("bomb7.png") #load an image as a Surface
bomb7 = bomb7.convert() #need to convert it after we have set-up the screen
colorkey = bomb7.get_at((1,1))
bomb7.set_colorkey(colorkey, pygame.RLEACCEL)


bomb8 = pygame.image.load("bomb8.png") #load an image as a Surface
bomb8 = bomb8.convert() #need to convert it after we have set-up the screen
colorkey = bomb8.get_at((1,1))
bomb8.set_colorkey(colorkey, pygame.RLEACCEL)

bomb9 = pygame.image.load("bomb9.png") #load an image as a Surface
bomb9 = bomb9.convert() #need to convert it after we have set-up the screen
colorkey = bomb9.get_at((1,1))
bomb9.set_colorkey(colorkey, pygame.RLEACCEL)

bomb10 = pygame.image.load("bomb10.png") #load an image as a Surface
bomb10 = bomb10.convert() #need to convert it after we have set-up the screen
colorkey = bomb10.get_at((1,1))
bomb10.set_colorkey(colorkey, pygame.RLEACCEL)

explodeimage=[bomb1,bomb2,bomb4,bomb5,bomb6,bomb7,bomb8,bomb9,bomb10]   #Add the pictures into a list for use


dot=0







while keep_going:

    clock.tick(1000) #<-- Set a constant frame rate, argument is frames per second

    choose=0









    dot=dot+1
    if gamestart==True and dot%10==0:   #If it's in game and for 10 clocktick passes

        for x in range (len(newmap.bomb)):      #Bomb state changes by 1
            if newmap.bomb[x].state==0:
                newmap.bomb[x].state=1
            elif newmap.bomb[x].state==1:
                newmap.bomb[x].state=0
                newmap.bomb[x].cycle=newmap.bomb[x].cycle+1     #If a cycle is finished add one cycle

    if gamestart==True:
        if len(newmap.bomb)!=0:
            if newmap.bomb[0].cycle==2:         #If 2 cycle has finished let it enter explode mode
                newmap.bomb[0].state=2

        if len(newmap.bomb)!=0:
            for i in range (len(newmap.bomb)):      #If there is more than 1 bomb, let bomb state increase by1
                if newmap.bomb[i].state==2:
                    newmap.bomb[i].explodestate=newmap.bomb[i].explodestate+1
        if len(newmap.bomb)!=0:
            if newmap.bomb[0].explodestate==8:
                newmap.playeringame[newmap.bomb[0].by].bombnumber=newmap.playeringame[newmap.bomb[0].by].bombnumber-1       #If bomb explodes calculate:
                pygame.mixer.music.load("bombsound.mp3") #used for a sound effect
                pygame.mixer.music.set_volume(0.4)
                pygame.mixer.music.play()

                for i in range (len(newmap.playeringame)):
                    if ( newmap.bomb[0].x-75<=newmap.playeringame[i].x) and (newmap.bomb[0].x+150>=newmap.playeringame[i].x) and (newmap.bomb[0].y<=newmap.playeringame[i].y) and (newmap.bomb[0].y+75>=newmap.playeringame[i].y) :
                        newmap.playeringame[i].life=newmap.playeringame[i].life-1
                    elif ( newmap.bomb[0].x-75<=newmap.playeringame[i].x) and (newmap.bomb[0].x+150>=newmap.playeringame[i].x) and (newmap.bomb[0].y<=newmap.playeringame[i].y+75) and (newmap.bomb[0].y+75>=newmap.playeringame[i].y+75) :
                        newmap.playeringame[i].life=newmap.playeringame[i].life-1
                    elif ( newmap.bomb[0].x-75<=newmap.playeringame[i].x+75) and (newmap.bomb[0].x+150>=newmap.playeringame[i].x+75) and (newmap.bomb[0].y<=newmap.playeringame[i].y+75) and (newmap.bomb[0].y+75>=newmap.playeringame[i].y+75) :
                        newmap.playeringame[i].life=newmap.playeringame[i].life-1
                    elif (newmap.bomb[0].x-75<=newmap.playeringame[i].x+75) and (newmap.bomb[0].x+150>=newmap.playeringame[i].x+75) and (newmap.bomb[0].y<=newmap.playeringame[i].y) and (newmap.bomb[0].y+75>=newmap.playeringame[i].y):
                        newmap.playeringame[i].life=newmap.playeringame[i].life-1
                    elif  ( newmap.bomb[0].y-75<=newmap.playeringame[i].y) and (newmap.bomb[0].y+150>=newmap.playeringame[i].y) and (newmap.bomb[0].x<=newmap.playeringame[i].x) and (newmap.bomb[0].x+75>=newmap.playeringame[i].x) :
                        newmap.playeringame[i].life=newmap.playeringame[i].life-1

                    elif  ( newmap.bomb[0].y-75<=newmap.playeringame[i].y) and (newmap.bomb[0].y+150>=newmap.playeringame[i].y) and (newmap.bomb[0].x<=newmap.playeringame[i].x+75) and (newmap.bomb[0].x+75>=newmap.playeringame[i].x+75) :
                        newmap.playeringame[i].life=newmap.playeringame[i].life-1
                    elif  ( newmap.bomb[0].y-75<=newmap.playeringame[i].y+75) and (newmap.bomb[0].y+150>=newmap.playeringame[i].y+75) and (newmap.bomb[0].x<=newmap.playeringame[i].x+75) and (newmap.bomb[0].x+75>=newmap.playeringame[i].x+75) :
                        newmap.playeringame[i].life=newmap.playeringame[i].life-1
                    elif  ( newmap.bomb[0].y-75<=newmap.playeringame[i].y+75) and (newmap.bomb[0].y+150>=newmap.playeringame[i].y+75) and (newmap.bomb[0].x<=newmap.playeringame[i].x) and (newmap.bomb[0].x+75>=newmap.playeringame[i].x) :
                        newmap.playeringame[i].life=newmap.playeringame[i].life-1

                    '''
                    If the four edges of any are inside the horizontal and vertical explosion range then life decreases by 1
                    '''


                for i in range (len(newmap.walllist)-1,-1,-1):
                    if ( newmap.bomb[0].x-75<newmap.walllist[i].x) and (newmap.bomb[0].x+150>newmap.walllist[i].x) and (newmap.bomb[0].y<newmap.walllist[i].y) and (newmap.bomb[0].y+75>newmap.walllist[i].y) :
                        if newmap.walllist[i].destructable==True:
                            newmap.walllist.pop(i)

                    if ( newmap.bomb[0].x-75<newmap.walllist[i].x) and (newmap.bomb[0].x+150>newmap.walllist[i].x) and (newmap.bomb[0].y<newmap.walllist[i].y+75) and (newmap.bomb[0].y+75>newmap.walllist[i].y+75) :

                        if newmap.walllist[i].destructable==True:
                            newmap.walllist.pop(i)
                    if ( newmap.bomb[0].x-75<newmap.walllist[i].x+75) and (newmap.bomb[0].x+150>newmap.walllist[i].x+75) and (newmap.bomb[0].y<newmap.walllist[i].y+75) and (newmap.bomb[0].y+75>newmap.walllist[i].y+75) :
                        if newmap.walllist[i].destructable==True:
                            newmap.walllist.pop(i)
                    if (newmap.bomb[0].x-75<newmap.walllist[i].x+75) and (newmap.bomb[0].x+150>newmap.walllist[i].x+75) and (newmap.bomb[0].y<newmap.walllist[i].y) and (newmap.bomb[0].y+75>newmap.walllist[i].y):
                        if newmap.walllist[i].destructable==True:
                            newmap.walllist.pop(i)
                    if  ( newmap.bomb[0].y-75<newmap.walllist[i].y) and (newmap.bomb[0].y+150>newmap.walllist[i].y) and (newmap.bomb[0].x<newmap.walllist[i].x) and (newmap.bomb[0].x+75>newmap.walllist[i].x) :
                        if newmap.walllist[i].destructable==True:
                            newmap.walllist.pop(i)

                    if  ( newmap.bomb[0].y-75<newmap.walllist[i].y) and (newmap.bomb[0].y+150>newmap.walllist[i].y) and (newmap.bomb[0].x<newmap.walllist[i].x+75) and (newmap.bomb[0].x+75>newmap.walllist[i].x+75) :
                        if newmap.walllist[i].destructable==True:
                            newmap.walllist.pop(i)
                    if  ( newmap.bomb[0].y-75<newmap.walllist[i].y+75) and (newmap.bomb[0].y+150>newmap.walllist[i].y+75) and (newmap.bomb[0].x<newmap.walllist[i].x+75) and (newmap.bomb[0].x+75>newmap.walllist[i].x+75) :
                        if newmap.walllist[i].destructable==True:
                            newmap.walllist.pop(i)
                    if  ( newmap.bomb[0].y-75<newmap.walllist[i].y+75) and (newmap.bomb[0].y+150>newmap.walllist[i].y+75) and (newmap.bomb[0].x<newmap.walllist[i].x) and (newmap.bomb[0].x+75>newmap.walllist[i].x) :
                        if newmap.walllist[i].destructable==True:
                            newmap.walllist.pop(i)

                    #For each wall if four edges are in explosion range if the wall is destructable remove it from the wall list

                for i in range (len(newmap.playeringame)):
                    if newmap.playeringame[i].life==0 and newmap.playeringame[i].dead==False:   #If the hero is not dead and health is one
                        newmap.playerremain=newmap.playerremain-1                               #Decreases player by 1 and remove it and make it dead

                        newmap.playeringame[i].x=-10000
                        newmap.playeringame[i].y=-10000
                        newmap.playeringame[i].dead=True
                newmap.bomb.pop(0)                                                              #Remove the bomb and refresh the page
                newmap.printmap()



    if gamestart==True:

        if  newmap.playerremain==1:
            gamestart=False
            my_font = pygame.font.SysFont("georgia", 100) #custom font, needs font file         #If only one player is remained output the victory word with the winner
            for i in range (len(newmap.playeringame)):

                if newmap.playeringame[i].life!=0:
                    choose=i+1
            lifepoint = my_font.render("Player "+str(choose)+"VICTORY!!!", False, (0,0,0))
            screen.blit(lifepoint, (50,200))
            pygame.display.flip()
            for i in range (5):
                clock.tick(1)


            inmainmenu=True
            mainmenustuff()

    keys = pygame.key.get_pressed()
    if gamestart==True:

        if keys[pygame.K_a]:

            if checkcollision(0,"left") == False:

                newmap.playeringame[0].x=newmap.playeringame[0].x-10*newmap.playeringame[0].speed   #If the player goes left and didn't collide with anything

                                                                                                    #Move with the speed and change the walking style
                if newmap.playeringame[0].facing==3:
                    if newmap.playeringame[0].walkstyle!=3:
                        newmap.playeringame[0].walkstyle=newmap.playeringame[0].walkstyle+1
                    else:
                        newmap.playeringame[0].walkstyle=1
                else:
                    newmap.playeringame[0].walkstyle=1
            newmap.playeringame[0].facing=3


        if keys[pygame.K_d]:
            if checkcollision(0,"right") == False:
                #newmap.playeringame[0].x=x+10*newmap.playeringame[0].speed
                newmap.playeringame[0].x=newmap.playeringame[0].x+10*newmap.playeringame[0].speed   #If the player goes right and didn't collide with anything

                                                                                                    #Move with the speed and change the walking style
                if newmap.playeringame[0].facing==4:
                    if newmap.playeringame[0].walkstyle!=3:
                        newmap.playeringame[0].walkstyle=newmap.playeringame[0].walkstyle+1
                    else:
                        newmap.playeringame[0].walkstyle=1
                else:
                    newmap.playeringame[0].walkstyle=1
            newmap.playeringame[0].facing=4
        if keys[pygame.K_s]:
            if checkcollision(0,"down") == False:

                newmap.playeringame[0].y=newmap.playeringame[0].y+10*newmap.playeringame[0].speed   #same as the above
                if newmap.playeringame[0].facing==1:
                    if newmap.playeringame[0].walkstyle!=3:
                        newmap.playeringame[0].walkstyle=newmap.playeringame[0].walkstyle+1
                    else:
                        newmap.playeringame[0].walkstyle=1
                else:
                    newmap.playeringame[0].walkstyle=1
            newmap.playeringame[0].facing=1
        if keys[pygame.K_w]:
            if checkcollision(0,"up") == False:
                #newmap.playeringame[0].y=y-10*newmap.playeringame[0].speed
                newmap.playeringame[0].y=newmap.playeringame[0].y-10*newmap.playeringame[0].speed   #same as the above
                if newmap.playeringame[0].facing==2:
                    if newmap.playeringame[0].walkstyle!=3:
                        newmap.playeringame[0].walkstyle=newmap.playeringame[0].walkstyle+1
                    else:
                        newmap.playeringame[0].walkstyle=1
                else:
                    newmap.playeringame[0].walkstyle=1
            newmap.playeringame[0].facing=2





        '''
        The rest part is for other 3 characters
'''

        if keys[pygame.K_g]:

            if checkcollision(1,"left") == False:

                newmap.playeringame[1].x=newmap.playeringame[1].x-10*newmap.playeringame[1].speed


                if newmap.playeringame[1].facing==3:
                    if newmap.playeringame[1].walkstyle!=3:
                        newmap.playeringame[1].walkstyle=newmap.playeringame[1].walkstyle+1
                    else:
                        newmap.playeringame[1].walkstyle=1
                else:
                    newmap.playeringame[1].walkstyle=1
            newmap.playeringame[1].facing=3


        if keys[pygame.K_j]:
            if checkcollision(1,"right") == False:
                #newmap.playeringame[1].x=x+11*newmap.playeringame[1].speed
                newmap.playeringame[1].x=newmap.playeringame[1].x+10*newmap.playeringame[1].speed
                if newmap.playeringame[1].facing==4:
                    if newmap.playeringame[1].walkstyle!=3:
                        newmap.playeringame[1].walkstyle=newmap.playeringame[1].walkstyle+1
                    else:
                        newmap.playeringame[1].walkstyle=1
                else:
                    newmap.playeringame[1].walkstyle=1
            newmap.playeringame[1].facing=4
        if keys[pygame.K_h]:
            if checkcollision(1,"down") == False:

                newmap.playeringame[1].y=newmap.playeringame[1].y+10*newmap.playeringame[1].speed
                if newmap.playeringame[1].facing==1:
                    if newmap.playeringame[1].walkstyle!=3:
                        newmap.playeringame[1].walkstyle=newmap.playeringame[1].walkstyle+1
                    else:
                        newmap.playeringame[1].walkstyle=1
                else:
                    newmap.playeringame[1].walkstyle=1
            newmap.playeringame[1].facing=1
        if keys[pygame.K_y]:
            if checkcollision(1,"up") == False:
                #newmap.playeringame[0].y=y-10*newmap.playeringame[0].speed
                newmap.playeringame[1].y=newmap.playeringame[1].y-10*newmap.playeringame[1].speed
                if newmap.playeringame[1].facing==2:
                    if newmap.playeringame[1].walkstyle!=3:
                        newmap.playeringame[1].walkstyle=newmap.playeringame[1].walkstyle+1
                    else:
                        newmap.playeringame[1].walkstyle=1
                else:
                    newmap.playeringame[1].walkstyle=1
                newmap.playeringame[1].facing=2

        if len(newmap.playeringame)>2:
            if keys[pygame.K_k]:

                if checkcollision(2,"left") == False:

                    newmap.playeringame[2].x=newmap.playeringame[2].x-10*newmap.playeringame[2].speed


                    if newmap.playeringame[2].facing==3:
                        if newmap.playeringame[2].walkstyle!=3:
                            newmap.playeringame[2].walkstyle=newmap.playeringame[2].walkstyle+1
                        else:
                            newmap.playeringame[2].walkstyle=1
                    else:
                        newmap.playeringame[2].walkstyle=1
                newmap.playeringame[2].facing=3


            if keys[pygame.K_SEMICOLON]:
                if checkcollision(2,"right") == False:
                    #newmap.playeringame[1].x=x+11*newmap.playeringame[1].speed
                    newmap.playeringame[2].x=newmap.playeringame[2].x+10*newmap.playeringame[2].speed
                    if newmap.playeringame[2].facing==4:
                        if newmap.playeringame[2].walkstyle!=3:
                            newmap.playeringame[2].walkstyle=newmap.playeringame[2].walkstyle+1
                        else:
                            newmap.playeringame[2].walkstyle=1
                    else:
                        newmap.playeringame[2].walkstyle=1
                newmap.playeringame[2].facing=4
            if keys[pygame.K_l]:
                if checkcollision(2,"down") == False:

                    newmap.playeringame[2].y=newmap.playeringame[2].y+10*newmap.playeringame[2].speed
                    if newmap.playeringame[2].facing==1:
                        if newmap.playeringame[2].walkstyle!=3:
                            newmap.playeringame[2].walkstyle=newmap.playeringame[2].walkstyle+1
                        else:
                            newmap.playeringame[2].walkstyle=1
                    else:
                        newmap.playeringame[2].walkstyle=1
                newmap.playeringame[2].facing=1
            if keys[pygame.K_o]:
                if checkcollision(2,"up") == False:
                    #newmap.playeringame[0].y=y-10*newmap.playeringame[0].speed
                    newmap.playeringame[2].y=newmap.playeringame[2].y-10*newmap.playeringame[2].speed
                    if newmap.playeringame[2].facing==2:
                        if newmap.playeringame[2].walkstyle!=3:
                            newmap.playeringame[2].walkstyle=newmap.playeringame[2].walkstyle+1
                        else:
                            newmap.playeringame[2].walkstyle=1
                    else:
                        newmap.playeringame[2].walkstyle=1
                    newmap.playeringame[2].facing=2

        if len(newmap.playeringame)>3:
            if keys[pygame.K_KP4]:

                if checkcollision(3,"left") == False:

                    newmap.playeringame[3].x=newmap.playeringame[3].x-10*newmap.playeringame[3].speed


                    if newmap.playeringame[3].facing==3:
                        if newmap.playeringame[3].walkstyle!=3:
                            newmap.playeringame[3].walkstyle=newmap.playeringame[3].walkstyle+1
                        else:
                            newmap.playeringame[3].walkstyle=1
                    else:
                        newmap.playeringame[3].walkstyle=1
                newmap.playeringame[3].facing=3


            if keys[pygame.K_KP6]:
                if checkcollision(3,"right") == False:
                    #newmap.playeringame[1].x=x+11*newmap.playeringame[1].speed
                    newmap.playeringame[3].x=newmap.playeringame[3].x+10*newmap.playeringame[3].speed
                    if newmap.playeringame[3].facing==4:
                        if newmap.playeringame[3].walkstyle!=3:
                            newmap.playeringame[3].walkstyle=newmap.playeringame[3].walkstyle+1
                        else:
                            newmap.playeringame[3].walkstyle=1
                    else:
                        newmap.playeringame[3].walkstyle=1
                newmap.playeringame[3].facing=4
            if keys[pygame.K_KP5]:
                if checkcollision(3,"down") == False:

                    newmap.playeringame[3].y=newmap.playeringame[3].y+10*newmap.playeringame[3].speed
                    if newmap.playeringame[3].facing==1:
                        if newmap.playeringame[3].walkstyle!=3:
                            newmap.playeringame[3].walkstyle=newmap.playeringame[3].walkstyle+1
                        else:
                            newmap.playeringame[3].walkstyle=1
                    else:
                        newmap.playeringame[3].walkstyle=1
                newmap.playeringame[3].facing=1
            if keys[pygame.K_KP8]:
                if checkcollision(3,"up") == False:
                    #newmap.playeringame[0].y=y-10*newmap.playeringame[0].speed
                    newmap.playeringame[3].y=newmap.playeringame[3].y-10*newmap.playeringame[3].speed
                    if newmap.playeringame[3].facing==2:
                        if newmap.playeringame[3].walkstyle!=3:
                            newmap.playeringame[3].walkstyle=newmap.playeringame[3].walkstyle+1
                        else:
                            newmap.playeringame[3].walkstyle=1
                    else:
                        newmap.playeringame[3].walkstyle=1
                    newmap.playeringame[3].facing=2

        newmap.printmap()   #refresh the page

    #Handle any events in the current frame
    for ev in pygame.event.get(): #<-- returns a list of all Events in this frame
                                  #    and this loops over each event, acting accordingly

        #Events are objects with a type instance variable (an int, linked to pygame constants).
        #These types could be a certain key pressed, a mouse moved, or even a guitar strum!
        #These event types are mapped to constants in the pygame class.
        #You can see them all with help(pygame).

        if ev.type == QUIT: #<-- this special event type happens when the window is closed

            keep_going = False
        elif ev.type == KEYDOWN:

            if inselection==True:
                if ev.key == K_a:
                    if playerchoice[0]>1:
                        playerchoice[0]=playerchoice[0]-1
                if ev.key == K_d:
                    if playerchoice[0]<3 and playerchoice[0]!=0:            #If game is in character selection change character selection using the keys
                        playerchoice[0]=playerchoice[0]+1
                if ev.key == K_g:
                    if playerchoice[1]>1:
                        playerchoice[1]=playerchoice[1]-1
                if ev.key == K_j:
                    if playerchoice[1]<3 and playerchoice[1]!=0:
                        playerchoice[1]=playerchoice[1]+1
                if ev.key == K_k:
                    if playerchoice[2]>1:
                        playerchoice[2]=playerchoice[2]-1
                if ev.key == K_SEMICOLON:
                    if playerchoice[2]<3 and playerchoice[2]!=0:
                        playerchoice[2]=playerchoice[2]+1
                if ev.key == K_KP4:
                    if playerchoice[3]>1:
                        playerchoice[3]=playerchoice[3]-1
                if ev.key == K_KP6:
                    if playerchoice[3]<3 and playerchoice[3]!=0:
                        playerchoice[3]=playerchoice[3]+1
                characterselect()

            if gamestart==True:
                if ev.key == K_z:
                    if newmap.playeringame[0].bombnumber<3:
                        newmap.bomb.append(bomb(newmap.playeringame[0].x,newmap.playeringame[0].y,0))       #If the bomb key for each character is pressed add a bomb to the bomb list of the map
                        newmap.playeringame[0].bombnumber=newmap.playeringame[0].bombnumber+1

                if ev.key == K_v:
                    if newmap.playeringame[1].bombnumber<3:
                        newmap.bomb.append(bomb(newmap.playeringame[1].x,newmap.playeringame[1].y,1))
                        newmap.playeringame[1].bombnumber=newmap.playeringame[1].bombnumber+1
                if len(newmap.playeringame)>2:
                    if ev.key == K_m:
                        if newmap.playeringame[2].bombnumber<3:
                            newmap.bomb.append(bomb(newmap.playeringame[2].x,newmap.playeringame[2].y,2))
                            newmap.playeringame[2].bombnumber=newmap.playeringame[2].bombnumber+1
                if len(newmap.playeringame)>3:
                    if ev.key == K_KP1:
                        if newmap.playeringame[3].bombnumber<3:
                            newmap.bomb.append(bomb(newmap.playeringame[3].x,newmap.playeringame[3].y,3))
                            newmap.playeringame[3].bombnumber=newmap.playeringame[3].bombnumber+1



        elif  ev.type == MOUSEBUTTONDOWN: #A mouse click!
            if inmainmenu==True:
                if x>427 and x<657 and y>245 and y<308:
                    inmainmenu=False
                    inpregame=True

                    pregame()
                if x>439 and x<645 and y>342 and y<395:     #If specific button(area) is passed change the game page and run the function
                    inmainmenu=False
                    instructionmenu=True
                    instructionpage()
                if x>444 and x<647 and y>434 and y<491:
                    controlmenu=True
                    inmainmenu=False
                    controlpage()

            if inpregame==True:
                if x>45 and x<124 and y>45 and y<124:
                    inpregame=False
                    inmainmenu=True
                    mainmenustuff()

                if x>365 and x<404 and y>222 and y<284:
                    if life <3:
                        life=life+1
                        pregame()

                if x>636 and x<668 and y>222 and y<284:     #Change life setting
                    if life >1:
                        life=life-1
                        pregame()



                if x>364 and x<406 and y>344 and y<406:     #Change player setting
                    if player<4:
                        player=player+1
                        pregame()

                if x>636 and x<666 and y>340 and y<401:
                    if player>2:
                        player=player-1
                        pregame()
                if x>366 and x<407 and y>483 and y<550:     #Change map setting
                    if mapchoice<3:
                        mapchoice=mapchoice+1
                        pregame()
                if x>632 and x<667 and y>483 and y<550:
                    if mapchoice>1:
                        mapchoice=mapchoice-1
                        pregame()
                if x>825 and x<966 and y>494 and y<561:     #Enter character selection page
                    inpregame=False
                    inselection=True
                    playerchoice=[]
                    characterselect()
            if instructionmenu==True:
                if x>45 and x<124 and y>45 and y<124:           #Return to main menu
                    instructionmenu=False
                    inmainmenu=True
                    mainmenustuff()

            if controlmenu==True:

                if x>45 and x<124 and y>45 and y<124:       #Return to main menu
                    controlmenu=False
                    inmainmenu=True
                    mainmenustuff()
            if inselection==True:
                if x>45 and x<124 and y>45 and y<124:       #Select in game setting
                    inselection=False
                    inpregame=True
                    pregame()
                if x> 900 and x<990 and y>499 and y<580:
                    inselection=False
                    gamestart=True
                    pygame.mixer.music.load("maplestory.mp3") #used for a sound effect
                    pygame.mixer.music.set_volume(0.4)
                    pygame.mixer.music.play()
                    newmap=map(mapchoice-1,player)
                    newmap.printmap()
            x = ev.pos[0]  #the MOUSEBUTTONDOWN event has a position property
            y = ev.pos[1]  #that is an (x, y) tuple

        elif ev.type== MOUSEMOTION:
            x = ev.pos[0]  #the MOUSEBUTTONDOWN event has a position property
            y = ev.pos[1]  #that is an (x, y) tuple
            if inmainmenu==True:
                if ((x>427 and x<657 and y>245 and y<308) or (x>439 and x<645 and y>342 and y<395) or (x>444 and x<647 and y>434 and y<491))==True:
                    if onbutton ==False:
                        onbutton=True               #If the mouse in on a button output sound and highlight it
                        buttonsound()

                if ((x>427 and x<657 and y>245 and y<308) or (x>439 and x<645 and y>342 and y<395) or (x>444 and x<647 and y>434 and y<491))==False:
                    if onbutton==True:
                        onbutton=False

                if x>427 and x<657 and y>245 and y<308:
                    screen.blit(selectbackground, (427,245), pygame.Rect(427,245,230,63))
                    pygame.display.flip()
                if (x>427 and x<657 and y>245 and y<308) ==False:
                    screen.blit(background, (427,245), pygame.Rect(427,245,230,63))
                    pygame.display.flip()

                if x>439 and x<645 and y>342 and y<395:
                    screen.blit(selectbackground, (439,342), pygame.Rect(439,342,206,53))
                    pygame.display.flip()
                if (x>439 and x<645 and y>342 and y<395) ==False:
                    screen.blit(background, (439,342), pygame.Rect(439,342,206,53))
                    pygame.display.flip()

                if x>444 and x<647 and y>434 and y<491:
                    screen.blit(selectbackground, (444,434), pygame.Rect(444,434,203,57))
                    pygame.display.flip()
                if (x>444 and x<647 and y>434 and y<491) ==False:
                    screen.blit(background, (444,434), pygame.Rect(444,434,203,57))
                    pygame.display.flip()
            if instructionmenu==True:
                if (x>857 and x<933 and y>170 and y<219):
                    instructionposition=instructionposition+20      #If the mouse is on the button scroll down
                    instructionpage()
                if (x>859 and x<933 and y>359 and y<412):
                    instructionposition=instructionposition-20      #If the mouse is on the button scroll up
                    instructionpage()
    #Update and refresh the display to end this frame
   # screen.blit(background, (0, 0)) #<-- 'blit' means to copy one Surface to another
                                    #    Here, we copy the background onto the screen Surface
    #pygame.display.flip() #<-- refresh the display