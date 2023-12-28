import pygame
from pygame import mixer
from pygame.locals import KEYDOWN, K_ESCAPE
from gameobjects import Spaceship, Aliens
import gamevariables as gv

# init game
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((gv.screen_width, gv.screen_height))
pygame.display.set_caption('Space Invanders')

# count down when starting game
countdown = 3
last_count = pygame.time.get_ticks()

# create sprite groups
spaceship_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()

# create player
spaceship = Spaceship(int(gv.screen_width / 2), gv.screen_height - 100, 3)
spaceship_group.add(spaceship)

# generate aliens
for row in range(gv.alien_rows):
    for col in range(gv.alien_cols):
        x = 100 + col * 100
        y = 100 + row * 70
        alien = Aliens(x=x, y=y)
        alien_group.add(alien)

run = True
is_game_over = False
while run:

    clock.tick(gv.fps)

	#draw background
    gv.draw_bg(screen)

    if countdown > 0:
        gv.draw_text(
            screen,
            text='GET READY!', 
            font=gv.font40, 
            text_color=gv.white, 
            x=int(gv.screen_width / 2 - 110), 
            y=int(gv.screen_height / 2 + 50)
        )
        gv.draw_text(
            screen,
            text=str(countdown), 
            font=gv.font40, 
            text_color=gv.white, 
            x=int(gv.screen_width / 2 - 10), 
            y=int(gv.screen_height / 2 + 100)
        )
        count_timer = pygame.time.get_ticks()        
        if count_timer - last_count > 1000:
            countdown -= 1
            last_count = count_timer
    
    else:
        # update game objects            
        is_game_over = spaceship.update(alien_group)
        alien_group.update()

    # draw sprite groups
    spaceship_group.draw(screen)
    alien_group.draw(screen)

    if is_game_over:
        gv.draw_text(
        screen,
        text='GAME OVER!', 
        font=gv.font40, 
        text_color=gv.white, 
        x=int(gv.screen_width / 2 - 110), 
        y=int(gv.screen_height / 2 + 50)
    )

	# event handlers
    for event in pygame.event.get():
        # check for close the game window
        if event.type == pygame.QUIT:
            run = False
		
        # check for ESCAPE Key to exit
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            run = False


    pygame.display.update()

pygame.quit()