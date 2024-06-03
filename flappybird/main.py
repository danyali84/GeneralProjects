import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 30

screen_width = 710
screen_height = 750

#game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird') #title

#define game variables:
ground_scroll = 0
scroll_speed = 4

#load images
background = pygame.image.load('images/flappybg4.png')
ground_img = pygame.image.load('images/ground.png')

run = True
while run:

    clock.tick(fps)

    #puts the image as the background
    screen.blit(background, (0,0))

    #draw and scroll the ground
    screen.blit(ground_img, (ground_scroll, 580))
    ground_scroll -= scroll_speed #moves ground

    #restart image (puts it back in start pos) so it looks like it continuously scrolls
    if abs(ground_scroll) > 59:
        ground_scroll = 0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False #will stop running the program

    #update() ensures that the game actually updates itself after each iteration
    pygame.display.update()

pygame.quit()