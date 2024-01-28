import pygame
from pygame import mixer
import random

import gamevariables as gv

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

# load sounds
laser_fx = pygame.mixer.Sound("audio/laser.wav")
laser_fx.set_volume(0.25)

explosion_fx = pygame.mixer.Sound("audio/explosion.wav")
explosion_fx.set_volume(0.25)

bullet_hit_fx = pygame.mixer.Sound("audio/bullet_hit.wav")
bullet_hit_fx.set_volume(0.25)

# create spaceship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.last_shot = pygame.time.get_ticks()
        self.speed = 8
        self.shoot_cooldown = 1000 # milliseconds


    def update(self, alien_group, alien_bullet_group, bullet_group, explosion_group):
        # get key press
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        elif key[pygame.K_RIGHT] and self.rect.right < gv.screen_width:
            self.rect.x += self.speed            
        elif key[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed        
        elif key[pygame.K_DOWN] and self.rect.bottom < gv.screen_height:
            self.rect.y += self.speed            

        #record current time
        time_now = pygame.time.get_ticks()
            
        #shoot
        if key[pygame.K_SPACE] and (time_now - self.last_shot) > self.shoot_cooldown:
            laser_fx.play()
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = time_now
        
        # check collide with alien or bullet
        hit_alien = pygame.sprite.spritecollide(self, alien_group, False, pygame.sprite.collide_mask)
        hit_bullet = pygame.sprite.spritecollide(self, alien_bullet_group, False, pygame.sprite.collide_mask) 
        if hit_alien or hit_bullet:
            self.kill()

            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            explosion_group.add(explosion)


class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y, move_speed, bullet_speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"img/alien{str(random.randint(1, 5))}.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_speed = move_speed
        self.bullet_speed = bullet_speed

    def update(self, bullet_group, explosion_group):
        self.rect.x += self.move_speed
        self.move_counter += self.move_speed
        if abs(self.move_counter) > 75:
            self.move_speed *= -1
            # self.move_counter = 0
            self.rect.y += 5
        
        if pygame.sprite.spritecollide(self, bullet_group, True):
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)
            self.kill()


# create Bullets class
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
               
# create Alien Bullets class
class Alien_Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/alien_bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.bullet_speed = bullet_speed

    def update(self):
        self.rect.y += self.bullet_speed
        if self.rect.top > gv.screen_height:
            self.kill()

#create Explosion class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f"img/exp{num}.png")
            if size == 1:
                img = pygame.transform.scale(img, (20, 20))
            if size == 2:
                img = pygame.transform.scale(img, (40, 40))
            if size == 3:
                img = pygame.transform.scale(img, (160, 160))
            #add the image to the list
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0
        
        # play sound
        explosion_fx.play()


    def update(self):
        explosion_speed = 3
        # update explosion animation
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        # if the animation is complete, delete explosion
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()


# Obstacle
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,size,color,x,y):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = (x,y))

    def update(self, alien_group, alien_bullet_group, bullet_group):               
        # check collide with alien or bullet
        hit_alien = pygame.sprite.spritecollide(self, alien_group, False, pygame.sprite.collide_mask)
        hit_alien_bullet = pygame.sprite.spritecollide(self, alien_bullet_group, True, pygame.sprite.collide_mask) 
        hit_spaceship_bullet = pygame.sprite.spritecollide(self, bullet_group, True, pygame.sprite.collide_mask) 
        if hit_alien or hit_alien_bullet or hit_spaceship_bullet:
            self.kill()

obstacle_shape = [
'  xxxxxxx',
' xxxxxxxxx',
'xxxxxxxxxxx',
'xxxxxxxxxxx',
'xxxxxxxxxxx',
'xxx     xxx',
'xx       xx']

def create_obstacle(x_start, y_start, offset_x, obstacle_group):
    block_size = 6
    for row_index, row in enumerate(obstacle_shape):
        for column_index, col in enumerate(row):
            if col == 'x':
                x = x_start  + column_index * block_size + offset_x
                y = y_start + row_index  * block_size
                block = Obstacle(block_size,(241,79,80),x,y)
                obstacle_group.add(block)


def create_mutiple_obstacles(offset, x_start, y_start, obstacle_group):
    '''
    intput:
        x_start:    start position x of the onstacle
        y_start:    start position y of the onstacle
        offset_x:   off set between each obstacle
    output: create multiple obstacles
    '''
    for offset_x in offset:
        print('te ', offset_x)
        create_obstacle(x_start, y_start, offset_x, obstacle_group)



# Boss
class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, move_speed, hp=5):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"img/boss_alien.png")

        # Set the size for the image
        DEFAULT_IMAGE_SIZE = (150, 150)
 
        # Scale the image to your needed size
        self.image = pygame.transform.scale(self.image, DEFAULT_IMAGE_SIZE)
        self.hp = hp
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_speed = move_speed

    def update(self, bullet_group, explosion_group):
        self.rect.x += self.move_speed

        if self.rect.left < 0 or self.rect.right >= gv.screen_width:
            self.move_speed *= -1
            self.rect.y += 20
        
        if pygame.sprite.spritecollide(self, bullet_group, True):
            self.hp -= 1
            bullet_hit_fx.play()

            if self.hp == 0:
                explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
                explosion_group.add(explosion)
                self.kill()