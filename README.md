# Space Invader Tutorial

Ref: 
- https://youtu.be/f4coFYbYQzw?si=yW3awvdysHYHV7Q2 
- https://www.youtube.com/watch?v=o-6pADy5Mdg  
- https://www.youtube.com/watch?v=N17xEoyEkKY 

# Content
part 1
1. [run project](#run-project)
2. [add spaceship bullet](#add-spaceship-bullets)
3. [add enemies](#add-enemies)

4. [add enemy bullets](#add-enemy-bullets)
5. [add gameover condition](#add-gameover-condition)

part 2
6. [add boss](#add-boss)
7. [add boss laser](#add-boss-laser)
8. [add multiple level](#add-multiple-level)



# Part 1

## 1. Run Project
- install pygame
```sh
pip install pygame
```

- run project
```sh
python main.py
```


## 2. Add Spaceship Bullet
- add shooting feature to update method of `Spaceship` class
```py
# gameobjects.py

...

class Spaceship(pygame.sprite.Sprite):
    ...

    # add more bullet group
    def update(self, alien_group, bullet_group):
        ...

        # record current time
        time_now = pygame.time.get_ticks()

        #shoot
        if key[pygame.K_SPACE] and (time_now - self.last_shot) > self.shoot_cooldown:
            laser_fx.play()
            bullet = Bullets(self.rect.centerx, self.rect.top)
            game_group['bullet_group'].add(bullet)
            self.last_shot = time_now

```

- add update bullet group in `main.py`

```py
# main.py
...

# update game objects  
...
bullet_group.update()
obstacle_group.update(game_group) 
```


## 3. Add Enemies
- In `gameobjects.py`, add colid condition in `Spaceship` class and add update method in `Aliens` class 
```py
# gameobjects.py

...

class Spaceship(pygame.sprite.Sprite):

    def update(self, game_group):
        ...
        
        # check collide with alien or bullet
        # Step 3: Add Enemies. Add your code here
        # Step 4: Add Enemy Bullet. Add your code here
        # Step 7: Add Boss Laser. Add your code here
        hit_alien = pygame.sprite.spritecollide(self, game_group['alien_group'], False)
        hit_bullet = pygame.sprite.spritecollide(self, game_group['alien_bullet_group'], False) 
        hit_laser = pygame.sprite.spritecollide(self, game_group['boss_laser_group'], False) 
        
        if hit_alien or hit_bullet or hit_laser:
            self.kill()

            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            game_group['explosion_group'].add(explosion)



class Aliens(pygame.sprite.Sprite):
    ...

    def update(self, game_group, alien_direction, alien_move_speed):
        self.move_speed = alien_move_speed
        self.rect.x += self.move_speed * alien_direction
        
        if pygame.sprite.spritecollide(self, game_group['bullet_group'], True):
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            game_group['explosion_group'].add(explosion)
            self.kill()

```

- generate each aliens and set their movement condition
```py
# main.py

def run_game(level):
    ... 

    # generate aliens
    # Step 2: add enemies. Add your code here
    for row in range(gv.alien_rows):
        for col in range(gv.alien_cols):
            x = 100 + col * 100
            y = 100 + row * 70
            alien = Aliens(x=x, y=y, move_speed=gv.alien_move_speed, bullet_speed=3)
            alien_group.add(alien)
    ... 


    while run:
        ...

        if countdown > 0:
            ...
        else: # in game loop
            
            # check alien group direction
            # Step 2: add enemies. Add your code here
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

            ...

            # update game objects  
            ...
            alien_group.update(
                game_group=game_group,
                alien_direction=alien_direction,
                alien_move_speed=current_alien_move_speed,
            )
            explosion_group.update()

```

## 4. Add Enemy Bullets
- generate enemy bullets by choosing random enemy  
```py
# main.py

def run_game(level):
    ... 

    while run:
        ...

        if countdown > 0:
            ...
        else: # in game loop
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

            ...

            # update game objects  
            ...
            alien_bullet_group.update()

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

# Part 2
## Add Boss
- add boss class
```py
# gameobjects.py

...

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"img/boss_alien.png")
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