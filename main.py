import pygame
from pygame import mixer
from pygame.locals import KEYDOWN, K_ESCAPE
import random

from gameobjects import Spaceship, Aliens, Alien_Bullets, Boss
import gamevariables as gv


# init game
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((gv.screen_width, gv.screen_height))
pygame.display.set_caption('Space Invanders')

# count down when starting game
countdown = 3
last_count = pygame.time.get_ticks()


# def run_game():


# create sprite groups
spaceship_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()

# create player
spaceship = Spaceship(int(gv.screen_width / 2), gv.screen_height - 100, 3)
spaceship_group.add(spaceship)

# generate aliens
for row in range(gv.alien_rows):
    for col in range(gv.alien_cols):
        x = 100 + col * 100
        y = 100 + row * 70
        alien = Aliens(x=x, y=y, move_speed=3, bullet_speed=3)
        alien_group.add(alien)

# create boss
# boss = Boss(int(gv.screen_width / 2), 100)
# boss_group.add(boss)

run = True

last_alien_shot = pygame.time.get_ticks()
last_boss_shot = pygame.time.get_ticks()


# level
# alien speed, alien bullet speed, bullet delay
boss_level = [1, 3]


# Audio setup
music = []
music.append(pygame.mixer.Sound('./audio/music.wav'))                                 # music track 0
music.append(pygame.mixer.Sound('./audio/8-Bit Boss Battle- 4 - By EliteFerrex.mp3')) # music track 1
music[0].set_volume(0.25)
music[0].play(loops=-1)

is_boss_spawned = False

while run:

    clock.tick(gv.fps)
    time_now = pygame.time.get_ticks()

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
        if time_now - last_count > 1000:
            countdown -= 1
            last_count = time_now
    
    else:

		# alien shoot
        if (time_now - last_alien_shot > gv.alien_cooldown) and len(alien_bullet_group) < 5 and len(alien_group) > 0:
            attacking_alien = random.choice(alien_group.sprites())
            alien_bullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
            alien_bullet_group.add(alien_bullet)
            last_alien_shot = time_now

        # boss shoot
        # if (time_now - last_boss_shot > gv.boss_cooldown):
        #     boss_bullet = Alien_Bullets(boss.rect.centerx, boss.rect.bottom)
        #     alien_bullet_group.add(boss_bullet)
        #     last_boss_shot = time_now

        # update game objects            
        spaceship_group.update(
            alien_group=alien_group, 
            alien_bullet_group=alien_bullet_group,
            bullet_group=bullet_group,
            explosion_group=explosion_group,
        )
        alien_group.update(
            bullet_group=bullet_group, 
            explosion_group=explosion_group
        )
        bullet_group.update()
        alien_bullet_group.update()
        explosion_group.update()
        

    # draw sprite groups
    spaceship_group.draw(screen)
    alien_group.draw(screen)
    bullet_group.draw(screen)
    alien_bullet_group.draw(screen)
    explosion_group.draw(screen)
    

    # check to spawn boss
    if len(alien_group) == 0 and not is_boss_spawned:
        # if current_aliens_amount == 0 and len(self.boss_alien.sprites())==0 and not self.boss_spawned:
        boss = Boss(x=int(gv.screen_width / 2), y=-50, move_speed=5)
        boss_group.add(boss)
        is_boss_spawned = True    
        music[0].fadeout(2000) # fade out old music track over 2 seconds

        music[1].set_volume(0.25)
        music[1].play(loops=-1)

    if is_boss_spawned:
        boss_group.update()

        boss_group.draw(screen)

    # check game over
    if len(spaceship_group) == 0:
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