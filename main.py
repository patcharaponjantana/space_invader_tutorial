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
    for row in range(gv.alien_rows):
        for col in range(gv.alien_cols):
            x = 100 + col * 100
            y = 100 + row * 70
            alien = Aliens(x=x, y=y, move_speed=gv.alien_move_speed, bullet_speed=3)
            alien_group.add(alien)
    

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

    # Increase when level up 
    # - alien: alien_move_speed, alien_max_increase, alien_bullet_speed, alien_cooldown
    # - boss: boss_bullet_ratio, boss_laser_cooldown, boss_hp, boss_move_speed
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
            increase_value = alien_max_increase - alien_max_increase * len(alien_group) / (gv.alien_rows * gv.alien_cols)
            current_alien_move_speed = alien_move_speed + increase_value

            for alien in alien_group:
                if (alien.rect.right >= gv.screen_width) or (alien.rect.left <= 0):
                    alien_change_direction = True
                
            if alien_change_direction:
                alien_direction *= -1
                for alien in alien_group:
                    alien.rect.y += 10
                
                alien_change_direction = False

            
            # alien shoot
            # Step 4: Add Enemy Bullets. Add your code here
            if (time_now - last_alien_shot > alien_cooldown) and len(alien_bullet_group) < 10 and len(alien_group) > 0:
                attacking_alien = random.choice(alien_group.sprites())
                alien_bullet = Alien_Bullets(
                    attacking_alien.rect.centerx, 
                    attacking_alien.rect.bottom, 
                    bullet_speed=alien_bullet_speed
                )
                alien_bullet_group.add(alien_bullet)
                last_alien_shot = time_now

            # update game objects            
            spaceship_group.update(game_group)
            bullet_group.update()
            obstacle_group.update(game_group)
            alien_group.update(
                game_group=game_group,
                alien_direction=alien_direction,
                alien_move_speed=current_alien_move_speed,
            )
            explosion_group.update()
            alien_bullet_group.update()
            


            # check to spawn boss
            # if len(alien_group) == 0 and not is_boss_spawned:               
            #     boss = Boss(
            #         x=int(gv.screen_width / 2), 
            #         y=-50, 
            #         move_speed=boss_move_speed, 
            #         hp=boss_hp,
            #         bullet_ratio=boss_bullet_ratio,
            #         bullet_speed=alien_bullet_speed,
            #         laser_cooldown=boss_laser_cooldown,
            #     )     
            #     boss_group.add(boss)
            #     is_boss_spawned = True   

            #     # change music 
            #     music[0].fadeout(2000) # fade out old music track over 2 seconds
            #     music[1].set_volume(0.25)
            #     music[1].play(loops=-1)

            # update and display boss object
            # if is_boss_spawned:
            #     boss_group.update(game_group)
            #     charge_laser_group.update(boss_x=boss.rect.centerx - 30, boss_y=boss.rect.bottom)
            #     boss_laser_group.update()

            #     boss_group.draw(screen)

        # check game over
        # if len(spaceship_group) == 0:
        #     gv.draw_text(
        #         screen,
        #         text='GAME OVER!', 
        #         font=gv.font40, 
        #         text_color=gv.white, 
        #         x=int(gv.screen_width / 2 - 110), 
        #         y=int(gv.screen_height / 2 )
        #     )

        # check win the current level
        # if len(alien_group) == 0 and len(boss_group) == 0 :
        #     gv.draw_text(
        #         screen,
        #         text='Win!', 
        #         font=gv.font40, 
        #         text_color=gv.white, 
        #         x=int(gv.screen_width / 2 - 30), 
        #         y=int(gv.screen_height / 2)
        #     )
        #     gv.draw_text(
        #         screen,
        #         text='Press N for next level', 
        #         font=gv.font40, 
        #         text_color=gv.white, 
        #         x=int(gv.screen_width / 2 - 150), 
        #         y=int(gv.screen_height / 2 + 50)
        #     )      
        #     level_win = True

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