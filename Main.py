#Whack a snake
#Olin Pryszynski and Stan Marsh
#Jan 20, 2026

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

#limiting the framerate
clock=pygame.time.Clock()

#set the caption for the window
pygame.display.set_caption('Whack a Snake')

#setting up the cave pictures
caves=[]
for c in range(0,4):
    cave=pygame.image.load(os.path.join('assets','cave.png')).convert_alpha()
    cave=pygame.transform.rotate(cave,(-90))
    cave=pygame.transform.scale(cave,(200,100))
    caves.append(cave)

#setting  up the snake images
snake_rects=[]
snakes=[]
for s in range(0,4):
    snake=pygame.image.load(os.path.join('assets','snake head.png')).convert_alpha()
    snake=pygame.transform.scale(snake,(100,150))
    snake_rect=snake.get_rect()
    if s==0:
        snake_rect.topleft=(50,-50)
    else:
        snake_rect.topleft=(200*s+50,-50)
    
    snakes.append(snake)
    snake_rects.append(snake_rect)


running=True

#function to draw the images
def draw():

    #draw the caves at the top of the screen
    pygame.draw.rect(screen,('black'),[0,0,800,100])
    
    #line for where you cannot click the snakes
    pygame.draw.line(screen,('red'),(0,100),(800,100),10)
    
    #draw the snake
    for s in range(0,4):
        screen.blit(snakes[s],snake_rects[s])

    #draw the caves
    for c in range(0,4):
        screen.blit(caves[c],(c*200,0))




    

while running:

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,200,100))

    #draw the images
    draw()



    #make display appear
    pygame.display.flip()

    #limit the frame rate
    clock.tick(60)

pygame.quit()