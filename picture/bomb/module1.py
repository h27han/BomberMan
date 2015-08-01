"""
A basic program establishing a simple framework for future games.
"""

#Import & initialize the pygame module
import pygame
import thread
from pygame.locals import *  #This is not necessary for most games, but can simplify some things
pygame.init()












#Set-up the main display window and the background
size = (1024,600)  #<-- that is a tuple (just like a list) for width & height
screen = pygame.display.set_mode(size) #<-- screen is now a Surface type object
pygame.display.set_caption("Bomber Man") #<-- caption appears in the title bar


background = pygame.Surface(size) #<-- like display, but creates a Surface object from scratch
background = background.convert() #<-- creates a copy of the Surface with a standard (faster)
                                  #    colour format
background.fill((0, 0, 0)) #<-- fills Surface with colour using a tuple (red, green, blue).
                             #    See http://en.wikipedia.org/wiki/RGB_color_model for RGB info
                             #    See http://en.wikipedia.org/wiki/List_of_colors for colours









#The game loop
clock = pygame.time.Clock() #<-- used to control the frame rate
       #<-- a 'flag' variable for the game loop condition
pygame.display.flip()







bomb1 = pygame.image.load("bomb1.png") #load an image as a Surface
bomb1 = bomb1.convert() #need to convert it after we have set-up the screen
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

explodeimage=[bomb1,bomb2,bomb4,bomb5,bomb6,bomb7,bomb8,bomb9,bomb10]








pygame.mixer.music.load("bombsound.mp3") #used for a sound effect
pygame.mixer.music.set_volume(0.4)




def explode(position):
    for i in range (9):

        screen.blit(explodeimage[i], (position[0]-37.5,position[1]-37.5))
        pygame.display.flip()
        clock.tick(10)
        if i ==0:
            pygame.mixer.music.play()
        screen.blit(background, (position[0]-37.5, position[1]-37.5), pygame.Rect(position[0]-37.5, position[1]-37.5, 75, 75))
        pygame.display.flip()
    #screen.blit(background,(0,0))
    pygame.display.flip()




end=False

while end==False:

    clock.tick(10) #<-- Set a constant frame rate, argument is frames per second

    #Handle any events in the current frame
    for ev in pygame.event.get(): #<-- returns a list of all Events in this frame
                                  #    and this loops over each event, acting accordingly

        #Events are objects with a type instance variable (an int, linked to pygame constants).
        #These types could be a certain key pressed, a mouse moved, or even a guitar strum!
        #These event types are mapped to constants in the pygame class.
        #You can see them all with help(pygame).

        if ev.type == QUIT: #<-- this special event type happens when the window is closed
           end = True
        elif  ev.type == MOUSEBUTTONDOWN: #A mouse click!
            x = ev.pos[0]  #the MOUSEBUTTONDOWN event has a position property
            y = ev.pos[1]  #that is an (x, y) tuple

            bomb=thread.start_new_thread(explode,(ev.pos,))






    #Update and refresh the display to end this frame
   # screen.blit(background, (0, 0)) #<-- 'blit' means to copy one Surface to another
                                    #    Here, we copy the background onto the screen Surface
    #pygame.display.flip() #<-- refresh the display