from itertools import cycle
from numpy.random import randint,choice
import sys
import neat
import pickle as pickle
import os

from pathlib import Path

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

generation = 0
max_fitness = float('-inf')
best_genome = 0


def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

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


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)


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
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False #will stop running the program
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    #update() ensures that the game actually updates itself after each iteration
    pygame.display.update()

def eval_genomes(genomes, config):
    global score
    global generation, max_fitness, best_genome
    generation += 1
    i = 0
    for genome_id, genome in genomes:
        i+=1
        genome.fitness = game(genome,config) #need game class
        if genome.fitness is None:
            genome.fitness = float('-inf') #fix errors on early termination
        print("Gen : {} Genome # : {} Fitness : {} Max Fitness : {}".format(generation,i,genome.fitness, max_fitness))
        if (genome.fitness):
            if genome.fitness >= max_fitness:
                max_fitness = genome.fitness
                best_genome = genome
        score = 0

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, 'config')

pop = neat.Population(config)
stats = neat.StatisticsReporter()
pop.add_reporter(stats)

winner = pop.run(eval_genomes, 30)

print(winner)

outputDir = os.getcwd() + '/bestGenomes'
Path(outputDir).mkdir(parents =True, exist_ok=True)
os.chdir(outputDir)
serialNo = len(os.listdir(outputDir)) + 1
outputFile = open(str(serialNo)+'_'+str(int(max_fitness))+'.p','wb')

pickle.dump(winner, outputFile)

pygame.quit()