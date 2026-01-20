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
pygame.mixer.init(44100, -16, 2, 512, "none", 5)

#setting the screen size
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH,HEIGHT))

clock=pygame.time.Clock()  #make clock so I can limit the framerate later

pygame.display.set_caption('Whack a Snake')  #set the caption for the window

full_game=True  #variable for loop to allow the entire game to be repeated

#setting up sounds
requiem = pygame.mixer.Sound("assets/requiem.wav")  #music to play during main game
clicked = pygame.mixer.Sound("assets/metal pipe.wav")  #clicking on snakes
clicked.set_volume(0.5)  #quieting down the metal pipes
you_damaged = pygame.mixer.Sound("assets/sonic rings.wav")  #losing a life
you_damaged.set_volume(0.5)  #quieting down the rings sound effect
you_die = pygame.mixer.Sound("assets/yoda death sfx.wav")  #losing the game
life_up = pygame.mixer.Sound("assets/extra life.mp3")  #gaining a life
title_song = pygame.mixer.Sound("assets/title song.mp3")  #song to play during title crawl
title_song.set_volume(0.1)  #set the volume of the title song
audio_playing = False
died_audio_played = False
title_playing = False

text_scroll = True  #setting up the loop for the beinging text scroll. Placed here so text scroll doent play when the game is played again

while full_game:  #loop to allow the full game to repeat

    stans_font = pygame.font.SysFont('comicsans', 30)  #seting up the font for the starting scroll
    #loading screen
    screen.fill(('black'))
    loading_txt = stans_font.render('Loading...',1,'White')
    screen.blit(loading_txt,(335,280))
    pygame.display.flip()

    snake_speed = 5  #how fast the snakes move

    #keep track of the location of the extra life
    life_x = 0
    life_y = 900
    life_time = True

    secret = [] #keeping track of the secret code

    code_entered = 0  #keeping track of how many codes are entered
    
    master = False  #keeping track of if you are the master

    key_pressed = False

    score = 0  #keeping track of the score
    
    score_check = 0  #keeping track of what the score was
    
    lives = 3  #keeping track of your lives
    
    play = True  #keeping track of if you have lost yet or not
    
    running = True  #variable to keep the game loop on

    mouse_click = False  #make sure people dont just hold the click button down

    start_txt = stans_font.render('Press any key to start', 1, 'white')  #text to tell people to start the game

    #variable text ask people to quit or play again
    loss_txt=stans_font.render("You Lose",1,'white')
    end_txt = stans_font.render('Press p to play again',1,'white')
    quit_txt = stans_font.render('Press q to quit',1,'white')

    #variable text to make the text scroll at the beginning
    stans_text = stans_font.render(f"Click on the snakes head to send them back to the start",1,'yellow')
    stans_text1 = stans_font.render(f"temperarely. Click on apples to gain a life.",1,'yellow')
    stans_text2 = stans_font.render(f"======================================================",1,'yellow')
    stans_text3 = stans_font.render(f"You are a race of treants that have kids by growing",1,'yellow')
    stans_text4 = stans_font.render(f"apples and a group of snakes are coming to eat them.",1,'yellow')
    stans_text5 = stans_font.render(f"The snakes are a race of hydra its just one but there",1,'yellow')
    stans_text6 = stans_font.render(f"are many of them they are a menace to all of civil ",1,'yellow')
    stans_text7 = stans_font.render(f"socity. They regualery go to bars and rack up a tab  ",1,'yellow')
    stans_text8 = stans_font.render(f"in the 1,000$ and destroy the bar well drinking. ",1,'yellow')
    stans_text9 = stans_font.render(f"They also like eating kids, if they dont eat one ",1,'yellow')
    stans_text10 = stans_font.render(f"every 3 days they die. They will eat them faster  ",1,'yellow')
    stans_text11 = stans_font.render(f"then they need to beacuse they are evil. Side note, ",1,'yellow')
    stans_text12 = stans_font.render(f"for the tree people you are playing as, they like  ",1,'yellow')
    stans_text13 = stans_font.render(f"eating grandmas as feralizer. The way the apple turn ",1,'yellow')
    stans_text14 = stans_font.render(f"into the kids is that they grow into the tree person  ",1,'yellow')
    stans_text15 = stans_font.render(f"useing newtreants from the person that ate them and  ",1,'yellow')
    stans_text16 = stans_font.render(f"then crawling out of the toilet one day after they ",1,'yellow')
    stans_text17 = stans_font.render(f"have taken a dump.",1,'yellow')
    
    
    #location for the text on screen
    location_x = 10
    location_y = 500

    caves = []  #cave array
    for c in range(0,4):  #setting up the cave pictures
        cave = pygame.image.load(os.path.join('assets','cave.png')).convert_alpha()
        cave = pygame.transform.rotate(cave,(-90))
        cave = pygame.transform.scale(cave,(200,100))
        caves.append(cave)

    snake_rects = []  #snake hitbox array
    snakes = []  #snake images array
    go_times = []  #array of variable to decide when the snakes go
    gos = []  #array of variables that tell if the snakes are currently going
    snaketails = []  #array of rects to act as the snaketails
    for s in range(0,4):  #setting  up the snake images and hitboxes and controlls for how they move
        snake = pygame.image.load(os.path.join('assets','snake head.png')).convert_alpha()
        snake = pygame.transform.scale(snake,(100,150))
        snake_rect = snake.get_rect()

        snake_rect.topleft = (200*s+50,-50)

        snaketail = pygame.Rect(200*s+80,-700,40,700)

        #variables to help decide when the snakes go
        go = False
        go_time = 0

        go_times.append(go_time)
        gos.append(go)
        snakes.append(snake)
        snake_rects.append(snake_rect)
        snaketails.append(snaketail)
 
    apples=[]  #array of apples to display extra lives
    for a in range(0,10):  #creating the apples to show how many lives you have from the bottom of your screen
        apple = pygame.image.load(os.path.join('assets','apple.png'))
        apple = pygame.transform.scale(apple,(50,50))
        apples.append(apple)

    #creating the extra life apple that will fall down ocasioanlly
    extra_life = pygame.image.load(os.path.join('assets', 'apple.png'))
    extra_life = pygame.transform.scale(extra_life,(50,50))
    life_rect = extra_life.get_rect()
    
    def draw():  #function to draw the images

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

        #drawing the extra life
        screen.blit(extra_life,(life_rect))

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
            if lives>0:
                screen.blit(apples[a],(130+50*a,550))

    def snake_movement():  #function to make the snakes move
        for s in range(0,4):
            #make score global so i can update it in this function
            global score
            global lives
            global play
            global snake_speed
            global score_check
            global mouse_click
            global life_x
            global life_y
            global life_time
            #deciding if the snakes go or not
            if not gos[s] and snake_rects[s].y <= -50:
                if play or master:
                    go_times[s] = random.randint(0,600)
                    if go_times[s] > 590:
                        gos[s] = True
                    if go_times[s] >= 600 and life_time == True and lives < 10 and lives > 0:
                        life_y = 0
                        life_x = random.randint(100,700)
                        life_time = False


            #snakes moving foreward and backward
            if gos[s] == True:
                snake_rects[s].y += snake_speed
                snaketails[s].y += snake_speed
            elif snake_rects[s].y > -50 and gos[s] == False:
                snake_rects[s].y -= snake_speed
                snaketails[s].y -= snake_speed

            #if snakes make it across the whole screen
            if snake_rects[s].y >= 500:
                gos[s] = False
                if play == True and master == False:
                    lives -= 1
                you_damaged.play()

            mouse_hit=pygame.mouse.get_pressed()

            #clicking on the snakes
            if mouse_hit[0] and snake_rects[s].collidepoint(pygame.mouse.get_pos()) and gos[s] and play and snake_rects[s].y > 100 and not mouse_click:
                gos[s]=False
                score += 1
                mouse_click = True
                clicked.play()

            #send snakes back into the holes if you lose the game
            if not play:
                gos[s] = False

            #speed up snakes
            if score==score_check+10:
                score_check=score
                snake_speed+=1


            #clicking on the extra live
            if mouse_hit[0] and life_rect.collidepoint(pygame.mouse.get_pos()) and life_time==False and lives<10 and lives>0 and mouse_click==False:
                lives += 1
                life_y += 900
                life_time = True
                mouse_click = True
                life_up.play()

            #resetting the mouse click
            if not mouse_hit[0]:
                mouse_click = False

    while text_scroll:  #create the text scroll
     
        for event in pygame.event.get():  #event handler
            if event.type == pygame.QUIT:
                text_scroll = False
                running = False
                full_game = False
        
        screen.fill(('black'))  #fill the screen with black

        #play title music
        if not title_playing:
            title_playing = True
            title_song.play(9,0,0,)

        #draw the text scroll to the screen
        screen.blit(stans_text, (location_x, location_y))
        screen.blit(stans_text1, (location_x,location_y+90))
        screen.blit(stans_text2, (location_x,location_y+180))
        screen.blit(stans_text3, (location_x,location_y+270))
        screen.blit(stans_text4, (location_x,location_y+360))
        screen.blit(stans_text5, (location_x,location_y+450))    
        screen.blit(stans_text6, (location_x,location_y+540))    
        screen.blit(stans_text7, (location_x,location_y+630))     
        screen.blit(stans_text8, (location_x,location_y+720))     
        screen.blit(stans_text9, (location_x,location_y+810))    
        screen.blit(stans_text10, (location_x,location_y+900))   
        screen.blit(stans_text11, (location_x,location_y+990))
        screen.blit(stans_text12, (location_x,location_y+1080))
        screen.blit(stans_text13, (location_x,location_y+1170))
        screen.blit(stans_text14, (location_x,location_y+1260))
        screen.blit(stans_text15, (location_x,location_y+1350))
        screen.blit(stans_text16, (location_x,location_y+1440))
        screen.blit(stans_text17, (location_x,location_y+1530))

        screen.blit(start_txt, (460,20)) #text to tell people to start the game

        location_y -= 0.5  #moves the text up every loop

        keys=pygame.key.get_pressed()  #checks if each key is being pressed

        #secret code
        if keys[pygame.K_UP] and not key_pressed:  #if up is entered
            secret.append('up')
            code_entered+=1
            key_pressed=True

        elif keys[pygame.K_DOWN] and not key_pressed:  #if down is entered
            secret.append('down')
            code_entered+=1
            key_pressed=True

        elif keys[pygame.K_LEFT] and not key_pressed:  #if left is entered
            secret.append('left')
            code_entered += 1
            key_pressed=True
        
        elif keys[pygame.K_RIGHT] and not key_pressed:  #if right is entered
            secret.append('right')
            code_entered+=1
            key_pressed=True
     
        elif keys[pygame.K_b] and not key_pressed and code_entered == 8:  #if b is entered
            secret.append('b')
            code_entered += 1
            key_pressed=True
      
        elif keys[pygame.K_a] and not key_pressed and code_entered == 9:  #if a is entered
            secret.append('a')
            code_entered += 1
            key_pressed = True
     
        elif any(keys) and not key_pressed:  #if any key is pressed end the text scroll
            text_scroll=False
            title_song.stop()
   
        if not keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not keys[pygame.K_b] and not keys[pygame.K_a]:  #allow another key to be pressed
            key_pressed = False

        
        if code_entered==10:  #if konami code is entered
            if secret[0] == 'up' and secret[1] == 'up' and secret[2] == 'down' and secret[3] == 'down' and secret[4] == 'left' and secret[5] == 'right' and secret[6] == 'left' and secret[7] == 'right' and secret[8] == 'b' and secret[9] == 'a':
                master = True
                text_scroll = False
                title_song.stop()

        pygame.display.flip()  #update the display

        clock.tick(60)  #limit frame rate to 60 fps

    while running:  #main game loop

        #event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                text_scroll = False
                running = False
                full_game = False

        screen.fill(('black'))  #make the screen plack and prevent trails from apearing

        #list of every key that gets pressed
        keys=pygame.key.get_pressed()

        #start the music
        if not audio_playing:
            audio_playing = True
            requiem.play(9,0,0,)
        

        #moving the extra lives
        life_y += snake_speed
        life_rect.topleft = (life_x,life_y)
        if life_y > HEIGHT:
            life_time = True
     
        snake_movement()  #controlling the snakes
        draw()  #draw the images
        
        #when you lose the game
        if lives <= 0 and not master:
            play = False
            screen.blit(loss_txt,(335,200))
            screen.blit(end_txt,(255,300))
            screen.blit(quit_txt,(280,400))
            if died_audio_played == False:
                you_die.play(0,0,0)
                died_audio_played = True
            if keys[pygame.K_p]:
                running = False
            elif keys[pygame.K_q]:
                running = False
                full_game = False
            

        #make display appear
        pygame.display.flip()

        #limit the frame rate
        clock.tick(60)


pygame.quit()
