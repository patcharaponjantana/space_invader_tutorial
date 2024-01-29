import pygame
from pygame import mixer
from pygame.locals import KEYDOWN, K_ESCAPE, K_n
import random

from gameobjects import Spaceship, Aliens, Alien_Bullets, Boss, create_mutiple_obstacles
import gamevariables as gv


# init game
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((gv.screen_width, gv.screen_height))
pygame.display.set_caption('Space Invanders')


def run_game(level):
    # count down when starting game
    countdown = 3
    last_count = pygame.time.get_ticks()

    # create sprite groups
    spaceship_group = pygame.sprite.Group()
    alien_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    alien_bullet_group = pygame.sprite.Group()
    explosion_group = pygame.sprite.Group()
    boss_group = pygame.sprite.Group()
    obstacle_group = pygame.sprite.Group()
    charge_laser_group = pygame.sprite.Group()
    boss_laser_group = pygame.sprite.Group()

    game_group = {
        'spaceship_group': spaceship_group,
        'alien_group': alien_group,
        'bullet_group': bullet_group,
        'alien_bullet_group': alien_bullet_group,
        'explosion_group': explosion_group,
        'boss_group': boss_group,
        'obstacle_group': obstacle_group,
        'charge_laser_group': charge_laser_group,
        'boss_laser_group': boss_laser_group,
    }

    # create player
    spaceship = Spaceship(x=int(gv.screen_width / 2), y=gv.screen_height - 70)
    spaceship_group.add(spaceship)

    # generate aliens 
    # Step 3: Add Enemies. Add your code here
    

    # add obstacle
    create_mutiple_obstacles(
        offset=gv.ostable_x_positions,
        x_start=gv.screen_width/15, 
        y_start=600, 
        obstacle_group=obstacle_group
    )

    # Audio setup
    music = []
    music.append(pygame.mixer.Sound('./audio/music.wav'))                                 # music track 0
    music.append(pygame.mixer.Sound('./audio/8-Bit Boss Battle- 4 - By EliteFerrex.mp3')) # music track 1
    music[0].set_volume(0.15)
    music[0].play(loops=-1)

    # Game State
    is_boss_spawned = False
    level_win = False
    is_quite_game = False
    boss = None 
    last_alien_shot = pygame.time.get_ticks()
    alien_direction = 1
    alien_change_direction = False
    run = True

    # Increase enemy properties when level up 
    # - alien: alien_move_speed, alien_max_increase, alien_bullet_speed, alien_cooldown
    # - boss: boss_bullet_ratio, boss_laser_cooldown, boss_hp, boss_move_speed
    # Step 8: Add Multiple Level. You can adjust game level in here
    level_index = level - 1
    alien_move_speed = gv.alien_move_speed + level_index
    alien_max_increase = gv.alien_max_increase + level_index
    alien_bullet_speed = gv.alien_bullet_speed + level_index * 2
    alien_cooldown = gv.alien_cooldown - level_index * 200
    boss_bullet_ratio = gv.boss_bullet_ratio + level_index * 0.05
    boss_laser_cooldown = gv.boss_laser_cooldown - level_index * 1000
    boss_hp = gv.boss_hp + level_index * 2
    boss_move_speed = gv.boss_move_speed + level_index * 2

    while run:

        clock.tick(gv.fps)
        time_now = pygame.time.get_ticks()

        # draw background
        gv.draw_bg(screen)

        # draw sprite groups
        spaceship_group.draw(screen)
        alien_group.draw(screen)
        bullet_group.draw(screen)
        alien_bullet_group.draw(screen)
        explosion_group.draw(screen)
        obstacle_group.draw(screen)
        charge_laser_group.draw(screen)
        boss_laser_group.draw(screen)

        # waiting for start
        if countdown > 0:
            gv.draw_text(
                screen,
                text=f'Level {level}', 
                font=gv.font40, 
                text_color=gv.white, 
                x=int(gv.screen_width / 2 - 60), 
                y=int(gv.screen_height / 2 - 50 )
            )
            gv.draw_text(
                screen,
                text=f'GET READY!', 
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
            if time_now - last_count > 1000:
                countdown -= 1
                last_count = time_now

        
        else: # in game loop

            # check alien group direction                
            # Step 3: add enemies. Add your code here

            
            # alien shoot
            # Step 4: Add Enemy Bullets. Add your code here
        

            # update game objects 
            # Step 2-4: Update game objects. Add your code here
            spaceship_group.update(game_group)

            # check to spawn boss
            # Step 6: Add Boss. Add your code here


        # check game over
        # Step 5: Add Gameover Condition. Add your code here


        # check win the current level
        # Step 8: Add Multiple Level . Add your code here



        # event handlers
        for event in pygame.event.get():

            # check for next level
            if (event.type == pygame.KEYDOWN and  event.key == K_n) and level_win:
                run = False
                music[1].stop()

            # check for close the game window
            if (event.type == pygame.QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
                run = False
                is_quite_game = True


        pygame.display.update()
    
    return is_quite_game



# level loop

for level in range(1, 5):
    is_quite_game = run_game(level=level)

    if is_quite_game:
        break

pygame.quit()