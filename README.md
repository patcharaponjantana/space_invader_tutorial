# Space Invader Tutorial

ref:  https://www.youtube.com/watch?v=PFMoo_dvhyw 

# Content
- run project 
- add enemies
- add gameover condition
- add spaceship bullet
- add enemy bullets
- add explosion
- add health bar
- add missions
- add boss


## Run Project
- install pygame
```sh
pip install pygame
```

- run project
```sh
python main.py
```

## Add Enemies
- add `Aliens` class in `gameobjects.py`
```py
# gameobjects.py

import random
...

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

```

- add alien group and generate each aliens
```py
# main.py

... 

# create sprite groups
alien_group = pygame.sprite.Group()


# generate aliens
for row in range(gv.alien_rows):
    for col in range(gv.alien_cols):
        x = 100 + col * 100
        y = 100 + row * 70
        alien = Aliens(x=x, y=y)
        alien_group.add(alien)

... 

```

- update and draw `alien_group`
```py
# main.py

...

while run:
    if countdown > 0:
        ...
    
    else:
        # update game objects 
        ... 
        alien_group.update()


    # draw sprite groups
    ...
    alien_group.draw(screen)

``` 

## Add Gameover Condition
- check that spaceship hit with any aliens
```py
# gameobjects.py

...


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        ...

        self.is_dead = False

    # add alien_group for checking collision
    def update(self, alien_group):
        ...

        # add up, down movement
        elif key[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= speed        
        elif key[pygame.K_DOWN] and self.rect.bottom < gv.screen_height:
            self.rect.y += speed            
            
        if pygame.sprite.spritecollide(self, alien_group, False, pygame.sprite.collide_mask):
            self.kill()
            self.is_dead = True

        return self.is_dead

```

- get game over status. if it is true, game will show game over text.
```py
is_game_over = False
while run:

    if countdown > 0:
        ...
    
    else:
        # update game objects            
        is_game_over = spaceship.update(alien_group)
        ...

    # draw sprite groups
    ...

    if is_game_over:
        gv.draw_text(
        screen,
        text='GAME OVER!', 
        font=gv.font40, 
        text_color=gv.white, 
        x=int(gv.screen_width / 2 - 110), 
        y=int(gv.screen_height / 2 + 50)
    )

```

## Add Spaceship Bullet
- add bullet class
```py
# gameobjects.py

...

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        ...

        self.shoot_cooldown = 1000 # milliseconds

    # add more bullet group
    def update(self, alien_group, bullet_group):
        ...

        # record current time
        time_now = pygame.time.get_ticks()
            
        # shoot
        if key[pygame.K_SPACE] and (time_now - self.last_shot) > self.shoot_cooldown:
            laser_fx.play()
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = time_now
        
        ...

# create Bullets class
class Bullets(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("img/bullet.png")
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]

	def update(self, alien_group):
		self.rect.y -= 5
		if self.rect.bottom < 0:
			self.kill()
		if pygame.sprite.spritecollide(self, alien_group, True):
			self.kill()

```

- add bullet group, send it to spaceship and draw it

```py
# main.py

...

# create sprite groups
...
bullet_group = pygame.sprite.Group()

while run:
    
    ...
    if countdown > 0:
        ...
    else:
        # update game objects            
        is_game_over = spaceship.update(
            alien_group=alien_group, 
            bullet_group=bullet_group,
        )
        alien_group.update()
        bullet_group.update(alien_group)

    # draw sprite groups
    spaceship_group.draw(screen)
    alien_group.draw(screen)
    bullet_group.draw(screen)
```