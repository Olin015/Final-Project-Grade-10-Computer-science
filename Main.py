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

#how fast the snakes move
snake_speed=5


#keeping track of the score
score = 0
#keeping track of what the score was
score_check=0
#keeping track of your lives
lives = 3 
#keeping track of if you have lost yet or not
play=True
#variable to keep the game loop on
running=True

#setting up the loop for the beinging text scroll
text_scroll = True 

#make sure people dont just hold the click button down
mouse_click=False

#seting up the font for the starting scroll
stans_font = pygame.font.SysFont('comicsans', 30)

#text to tell people to start the game
start_txt = stans_font.render('Press any key to start', 1, 'white')

stans_text = stans_font.render(f"""click on the snakesm head to send them back to the start temperaly they get faster over time
the lore for the game is as follows
you are a race of treants that have kids by growing apples and a group of snakes are coming to eat them
the snakes are a race of hydra its just one but there are many of them they are a meance to all of civilized socity
they regualery go to bars and rack up a tab in the 1,000$ and destory the bar well drinking
they also like eating kids if they dont eat one every 3 days they die they will eat them faster then they need to for the love of the game
side note for the tree people you are playing as they like eating grandmas as feralizer
the way the apples turn into the kids is that they grow into the tree person useing newtreants from the person that ate them and the bursting out of them like chest bursters
a""",1,'yellow')
#location for the text on screen
location_x = 100
location_y = 300

#create the text
while text_scroll == True:

    screen.fill(('black'))

    screen.blit(stans_text, (location_x,location_y)) #text scroll
    screen.blit(start_txt, (460,20)) #text to tell people to start the game

#event handler
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            text_scroll = False
        if event.type == pygame.QUIT:
            text_scroll = False
    location_y -=5 #moves the text up every loop
    
    pygame.display.flip()

    clock.tick(60)

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
snaketails=[]
for s in range(0,4):
    snake=pygame.image.load(os.path.join('assets','snake head.png')).convert_alpha()
    snake=pygame.transform.scale(snake,(100,150))
    snake_rect=snake.get_rect()

    snake_rect.topleft=(200*s+50,-50)

    snaketail=pygame.Rect(200*s+80,-700,40,700)

    #variables to help decide when the snakes go
    go=False
    go_time=0

    go_times.append(go_time)
    gos.append(go)
    snakes.append(snake)
    snake_rects.append(snake_rect)
    snaketails.append(snaketail)

apples=[]
for a in range(0,lives):
    apple=pygame.image.load(os.path.join('assets','apple.png'))
    apple=pygame.transform.scale(apple,(50,50))
    apples.append(apple)



#function to draw the images
def draw():

    global lives
    global play

    #draw the mountain wall at the top
    pygame.draw.rect(screen,((88,62,33)),[0,0,800,100])

    
    #line for where you cannot click the snakes
    pygame.draw.line(screen,('red'),(0,100),(800,100),10)

    
    #draw the snake
    for s in range(0,4):
        screen.blit(snakes[s],snake_rects[s])
        pygame.draw.rect(screen,(114,213,97),snaketails[s])

    #draw the next part of the big wall at the top
    pygame.draw.rect(screen,((88,62,33)),[0,0,800,10])

    #draw the caves
    for c in range(0,4):
        screen.blit(caves[c],(c*200,0))

    #draw the score
    score_txt = stans_font.render(f"""Score: {score}""",1,'white')
    screen.blit(score_txt, (650,550))

    #drawing how many lives are left
    lives_txt = stans_font.render('Lives: ',1,'white')
    screen.blit(lives_txt,(30,550))
    for a in range(0,lives):
        screen.blit(apples[a],(130+50*a,550))

    #when you lose the game
    if lives<=0:
        loss_txt=stans_font.render("You Lose",1,'white')
        screen.blit(loss_txt,(335,300))
        play=False

def snake_movement():
    for s in range(0,4):
        #make score global so i can update it in this function
        global score
        global lives
        global play
        global snake_speed
        global score_check
        global mouse_click
        #deciding if the snakes go or not
        if gos[s]==False and snake_rects[s].y<= -50 and play==True:
            go_times[s]=random.randint(0,60)
            if go_times[s]>59:
                gos[s]=True

        #snaks moving foreward and backward
        if gos[s]==True:
            snake_rects[s].y+=snake_speed
            snaketails[s].y+=snake_speed
        elif snake_rects[s].y>-50 and gos[s]==False:
            snake_rects[s].y-=snake_speed
            snaketails[s].y-=snake_speed

        #if snakes make it across the whole screen
        if snake_rects[s].y>=500:
            gos[s]=False
            if play==True:
                score-=1
                lives-=1

        mouse_hit=pygame.mouse.get_pressed()

        #clicking on the snakes
        if mouse_hit[0] and snake_rects[s].collidepoint(pygame.mouse.get_pos()) and gos[s]==True and play==True and snake_rects[s].y>100 and mouse_click==False:
            gos[s]=False
            score += 1
            mouse_click=True

        if not mouse_hit[0]:
            mouse_click=False

        #send snakes back into the holes if you lose the game
        if play==False:
            gos[s]=False

        #speed up snakes
        if score==score_check+10:
            score_check=score
            snake_speed+=1


while running:

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(('black'))



    #controlling the snakes
    snake_movement()

    #draw the images
    draw()



    #make display appear
    pygame.display.flip()

    #limit the frame rate
    clock.tick(60)

pygame.quit()
