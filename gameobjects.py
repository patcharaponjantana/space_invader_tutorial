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

laser_charge_fx = pygame.mixer.Sound("audio/laser_charge.wav")
laser_charge_fx.set_volume(0.25)

laser_shoot_fx = pygame.mixer.Sound("audio/shoot_laser.wav")
laser_shoot_fx.set_volume(0.25)

# --------------- Spaceship ---------------
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.last_shot = pygame.time.get_ticks()
        self.speed = gv.spaceship_move_speed
        self.shoot_cooldown = gv.spaceship_shoot_cooldown # milliseconds


    def update(self, game_group):
        # get key press
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        elif key[pygame.K_RIGHT] and self.rect.right < gv.screen_width:
            self.rect.x += self.speed             

        # Step 2: Add Spaceship Bullet. Add your code here
        # record current time
            
        
        # check collide with alien or bullet
        # Step 3: Add Enemies. Add your code here
        # Step 4: Add Enemy Bullet. Add your code here
        # Step 7: Add Boss Laser. Add your code here
            


# --------------- Spaceship Bullet ---------------
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= gv.spaceship_bullet_speed
        if self.rect.bottom < 0:
            self.kill()               


# --------------- Aliens ---------------
class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y, move_speed, bullet_speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"img/alien{str(random.randint(1, 5))}.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_speed = move_speed
        self.bullet_speed = bullet_speed

    # Step 3: Add Enemies. Add your code here
        


# --------------- Alien Bullets ---------------
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

# --------------- Explosion ---------------
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
            # add the image to the list
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

# --------------- Obstacle ---------------
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,size,color,x,y):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = (x,y))

    def update(self, game_group):               
        # check collide with alien or bullet
        hit_alien = pygame.sprite.spritecollide(self, game_group['alien_group'], False)
        hit_alien_bullet = pygame.sprite.spritecollide(self, game_group['alien_bullet_group'], True) 
        hit_spaceship_bullet = pygame.sprite.spritecollide(self, game_group['bullet_group'], True) 
        hit_laser = pygame.sprite.spritecollide(self, game_group['boss_laser_group'], False) 

        if hit_alien or hit_alien_bullet or hit_spaceship_bullet or hit_laser:
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
        create_obstacle(x_start, y_start, offset_x, obstacle_group)



# --------------- Boss ---------------
class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, move_speed, hp, bullet_ratio, bullet_speed, laser_cooldown):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"img/boss_alien.png")

        # Set the size for the image
        boss_size = (150, 150)
 
        # Scale the image to your needed size
        self.image = pygame.transform.scale(self.image, boss_size)
        self.hp = hp
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_speed = move_speed
        self.bullet_ratio = bullet_ratio
        self.bullet_speed = bullet_speed
        self.laser_cooldown = laser_cooldown
        self.last_boss_laser = pygame.time.get_ticks()
        self.is_shoot_laser = False
        self.charge_laser_obj = None
        self.boss_laser_obj = None

    # Step 6: Add Boss. Add your code here
        


# --------------- Boss Laser ---------------
class ChargeLaser(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.n_frame = 3
        for num in range(1, self.n_frame + 1):
            img = pygame.image.load(f"img/laser_charge{num}.png")
            if size == 1:
                img = pygame.transform.scale(img, (20, 20))
            if size == 2:
                img = pygame.transform.scale(img, (80, 80))
            if size == 3:
                img = pygame.transform.scale(img, (160, 160))
            #add the image to the list
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.start_time = pygame.time.get_ticks()
        self.counter = 0
        self.is_finish = False
        
        # play sound
        laser_charge_fx.play()


    def update(self, boss_x, boss_y):
        current_time = pygame.time.get_ticks()
        animate_duration = 2000 # ms
        animate_speed = 3
        self.rect.x = boss_x
        self.rect.y = boss_y

        # update animation
        self.counter += 1

        if (self.counter >= animate_speed):
            self.counter = 0
            self.index = (self.index + 1) % self.n_frame
            self.image = self.images[self.index]

        # if the animation is complete, delete it
        if current_time - self.start_time > animate_duration:
            self.kill()
            self.is_finish = True


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        img = pygame.image.load(f"img/laser_beam.png")
        img = pygame.transform.scale(img, (80, 800))

        # add the image to the list
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.start_time = pygame.time.get_ticks()
        self.is_finish = False
        
        # play sound
        laser_shoot_fx.play()


    def update(self):
        current_time = pygame.time.get_ticks()
        animate_duration = 1000

        # if the animation is complete, delete it
        if current_time - self.start_time > animate_duration:
            self.kill()
            self.is_finish = True