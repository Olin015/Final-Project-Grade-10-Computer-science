#Whack a snake
#Olin Pryszynski and Stan Marsh
#Jan 20, 2026

#imports
import pygame
import random
import os

#always at the beginning
pygame.init()
pygame.font.init()

#setting the screen size
WIDTH=800
HEIGHT=600
screen=pygame.display.set_mode((WIDTH,HEIGHT))

#limiting the framerate
clock=pygame.time.Clock()

#set the caption for the window
pygame.display.set_caption('Whack a Snake')

#how fas the snakes move
snake_speed=5

#setting up the loop for the beinging text scroll
text_scroll = True 

#seting up the font for the starting scroll
stans_font = pygame.font.SysFont('comicsans', 10)

stans_text = stans_font.render(f"""press any key to start click on the snakesm head to send them back to the start temperaly they get faster over time
the lore for the game is as follows
you are a race of treants that have kids by growing apples and a group of snakes are coming to eat them
the snakes are a race of hydra its just one but there are many of them they are a meance to all of civilized socity
they regualery go to bars and rack up a tab in the 1,000$ and destory the bar well drinking
they also like eating kids if they dont eat one every 3 days they die they will eat them faster then they need to for the love of the game
side note for the tree people you are playing as they like eating grandmas as feralizer
the way the apples turn into the kids is that they grow into the tree person useing newtreants from the person that ate them and the bursting out of them like chest bursters
a""",1,'yellow')
#location for the text on screen
location = (400,300)

#create the text
while text_scroll == True:
    screen.blit(stans_text, (location)) #text scroll
#event handler
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            text_scroll = False
        if event.type == pygame.QUIT:
            text_scroll = False
    #location +=5 #moves the text up every loop
    
    screen.fill((0,200,100))
    
    pygame.display.flip()


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
go_times=[]
gos=[]
for s in range(0,4):
    snake=pygame.image.load(os.path.join('assets','snake head.png')).convert_alpha()
    snake=pygame.transform.scale(snake,(100,150))
    snake_rect=snake.get_rect()
    if s==0:
        snake_rect.topleft=(50,-50)
    else:
        snake_rect.topleft=(200*s+50,-50)

    #variables to help decide when the snakes go
    go=False
    go_time=0

    go_times.append(go_time)
    gos.append(go)
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

def snake_movement():
    for s in range(0,4):
        #deciding if the snakes go or not
        if gos[s]==False and snake_rects[s].y<= -50:
            go_times[s]=random.randint(0,60)
            if go_times[s]>59:
                gos[s]=True

        #snaks moving foreward and backward
        if gos[s]==True:
            snake_rects[s].y+=snake_speed
        elif snake_rects[s].y>-50 and gos[s]==False:
            snake_rects[s].y-=snake_speed

        #if snakes make it across the whole screen
        if snake_rects[s].y>=500:
            gos[s]=False

        mouse_hit=pygame.mouse.get_pressed()
        mouse_pos=pygame.mouse.get_pos()



        #clicking on the snakes
        if mouse_hit[0]:
            if snake_rects[s].collidepoint(pygame.mouse.get_pos()):
                gos[s]=False


while running:

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,200,100))

    #draw the images
    draw()

    #controlling the snakes
    snake_movement()



    #make display appear
    pygame.display.flip()

    #limit the frame rate
    clock.tick(60)

pygame.quit()
