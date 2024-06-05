import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 710
screen_height = 750

#game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird') #title

#define game variables:
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False

#load images
background = pygame.image.load('images/flappybg4.png')
ground_img = pygame.image.load('images/ground.png')

#uses pygame's class
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/bird1.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
        if flying == True:
            #gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8 #caps at 8 velocity
            if self.rect.bottom < 580: #if its above ground, itll keep dropping
                self.rect.y += int(self.vel)

        #jump
        if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: #checks if left clicked
            self.clicked = True
            self.vel = -10
        if pygame.mouse.get_pressed()[0] == 0 : #ensures that you cant just hold jump
            self.clicked = False


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/pipe.png')
        self.rect = self.image.get_rect()
        #position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True) #specifies that you want it flipped on y axis
            self.rect.bottomleft = [x, y]
        if position == -1:
            self.rect.topleft = [x,y]


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)


btm_pipe = Pipe(300, int(screen_height / 2), -1)
top_pipe = Pipe(300, int(screen_height / 2), 1)
pipe_group.add(btm_pipe)
pipe_group.add(top_pipe)


run = True
while run:

    clock.tick(fps)

    #puts the image as the background
    screen.blit(background, (0,0))

    #inserts bird using built in function "draw"
    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
    pipe_group.update()


    #draw ground
    screen.blit(ground_img, (ground_scroll, 580))

    #check if bird has hit ground
    if flappy.rect.bottom > 580:
        game_over = True
        flying = False

    if game_over == False:
        ground_scroll -= scroll_speed #moves ground
        #restart image (puts it back in start pos) so it looks like it continuously scrolls
        if abs(ground_scroll) > 59:
            ground_scroll = 0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False #will stop running the program
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    #update() ensures that the game actually updates itself after each iteration
    pygame.display.update()

pygame.quit()