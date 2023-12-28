import pygame
from pygame import mixer
import random

import gamevariables as gv

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

# load sounds
laser_fx = pygame.mixer.Sound("img/laser.wav")
laser_fx.set_volume(0.25)


# create spaceship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.last_shot = pygame.time.get_ticks()
        self.is_game_over = False


    def update(self, alien_group):
        # set movement speed
        speed = 8

        # get key press
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        elif key[pygame.K_RIGHT] and self.rect.right < gv.screen_width:
            self.rect.x += speed            
        elif key[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= speed        
        elif key[pygame.K_DOWN] and self.rect.bottom < gv.screen_height:
            self.rect.y += speed            
            
        if pygame.sprite.spritecollide(self, alien_group, False, pygame.sprite.collide_mask):
            self.kill()
            self.is_game_over = True

        return self.is_game_over

class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"img/alien{str(random.randint(1, 5))}.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction = 1

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction
            self.rect.y += 5
