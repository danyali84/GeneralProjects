import pygame
from pygame.locals import *

import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 710
screen_height = 750

#game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird') #title

#define font
font = pygame.font.SysFont('Bauhaus 930', 60)
#define colors
white = (255, 255, 255)


#define game variables:
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500 #miliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False


#load images
background = pygame.image.load('images/flappybg4.png')
ground_img = pygame.image.load('images/ground.png')

#RESTART BUTTON
button_image = pygame.image.load("images/restart.png")


def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height/ 2)
    score = 0
    return score

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
        if game_over == False:
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
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x,y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill() #deletes the pipe to save storage

#RESTART BUTTON
class Button():
    def __init__(self, x , y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check if mouse is over the button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)

button = Button(screen_width//2 - 50, screen_height//2 - 100, button_image)

run = True
while run:

    clock.tick(fps)

    #puts the image as the background
    screen.blit(background, (0,0))

    #inserts bird using built in function "draw"
    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    #draw ground
    screen.blit(ground_img, (ground_scroll, 580))

    #check the score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

    draw_text(str(score), font, white, int(screen_width/2), 20)

    #look for collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        #2 falses are just additional parameters we dont need, and also checks if it hit the top
        game_over = True

    #check if bird has hit ground
    if flappy.rect.bottom >= 580:
        game_over = True
        flying = False

    if game_over == False and flying == True:

        #generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        ground_scroll -= scroll_speed #moves ground
        #restart image (puts it back in start pos) so it looks like it continuously scrolls
        if abs(ground_scroll) > 59:
            ground_scroll = 0

        pipe_group.update()

    #check for game over and reset
    #THIS IS WITH BUTTON
    #uncomment this if you want the button, and comment the without button section
    # if game_over == True:
    #     if button.draw() == True:
    #         game_over = False
    #         score = reset_game()

    #WIHTOUT BUTTON
    if game_over == True:
        game_over = False
        score = reset_game()
            
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False #will stop running the program
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    #update() ensures that the game actually updates itself after each iteration
    pygame.display.update()

pygame.quit()