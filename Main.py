#imports
import pygame
import random
import os

#always at the beginning
pygame.init()

#setting the screen size
WIDTH=800
HEIGHT=600
screen=pygame.display.set_mode((WIDTH,HEIGHT))


running=True

while running:

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,200,100))

    #make display appear
    pygame.display.flip()

pygame.quit()