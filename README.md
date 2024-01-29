# Space Invader Tutorial

Ref: 
- https://youtu.be/f4coFYbYQzw?si=yW3awvdysHYHV7Q2 
- https://www.youtube.com/watch?v=o-6pADy5Mdg  
- https://www.youtube.com/watch?v=N17xEoyEkKY 

# Content
1. [run project](#1-run-project)
2. [add spaceship bullet](#2-add-spaceship-bullet)
3. [add enemies](#3-add-enemies)

4. [add enemy bullets](#4-add-enemy-bullets)
5. [add gameover condition](#5-add-gameover-condition)

6. [add boss](#6-add-boss)  
7. [add boss laser](#7-add-boss-laser)  
8. [add multiple level](#8-add-multiple-level)  

9. [make window executable file (.exe)](#9-make-window-executable-file)


<h2 id="1-run-project"> 1. Run Project </h2>

- install pygame
```sh
pip install pygame
```

- run project
```sh
python main.py
```

<h2 id="2-add-spaceship-bullet"> 2. Add Spaceship Bullet </h2>

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
# Step 2-4: Update game objects. Add your code here
...
bullet_group.update()
obstacle_group.update(game_group) 
```

<h2 id="3-add-enemies"> 3. Add Enemies </h2>

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
            # Step 2-4: Update game objects. Add your code here
            ...
            alien_group.update(
                game_group=game_group,
                alien_direction=alien_direction,
                alien_move_speed=current_alien_move_speed,
            )
            explosion_group.update()

```

<h2 id="4-add-enemy-bullets"> 4. Add Enemy Bullets </h2>

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
            # Step 2-4: Update game objects. Add your code here 
            ...
            alien_bullet_group.update()

```

<h2 id="5-add-gameover-condition"> 5. Add Gameover Condition </h2>

- check if no spaceship in the group 
```py
# main.py

...

while run:

    if countdown > 0:
        ...
    
    else:
        ...

    # check game over
    # Step 5: Add Gameover Condition. Add your code here
    if len(spaceship_group) == 0:
        gv.draw_text(
            screen,
            text='GAME OVER!', 
            font=gv.font40, 
            text_color=gv.white, 
            x=int(gv.screen_width / 2 - 110), 
            y=int(gv.screen_height / 2 )
        )

```

<h2 id="6-add-boss"> 6. Add Boss </h2>

- add boss spawn condition
```py
# main.py
    ...

    while run:

        if countdown > 0:
            ...
        
        else:
            ...

            # check to spawn boss
            # Step 6: Add Boss. Add your code here
            if len(alien_group) == 0 and not is_boss_spawned:               
                boss = Boss(
                    x=int(gv.screen_width / 2), 
                    y=-50, 
                    move_speed=boss_move_speed, 
                    hp=boss_hp,
                    bullet_ratio=boss_bullet_ratio,
                    bullet_speed=alien_bullet_speed,
                    laser_cooldown=boss_laser_cooldown,
                )     
                boss_group.add(boss)
                is_boss_spawned = True   

                # change music 
                music[0].fadeout(2000) # fade out old music track over 2 seconds
                music[1].set_volume(0.25)
                music[1].play(loops=-1)

            # update and display boss object
            if is_boss_spawned:
                boss_group.update(game_group)
                charge_laser_group.update(boss_x=boss.rect.centerx - 30, boss_y=boss.rect.bottom)
                boss_laser_group.update()

                boss_group.draw(screen)

```

- add update method in `Boss` class
```py
gameobjects.py

class Boss(pygame.sprite.Sprite):
    ...

    # Step 6: Add Boss. Add your code here
    def update(self, game_group):
        time_now = pygame.time.get_ticks()

        if not self.is_shoot_laser:
            self.rect.x += self.move_speed

            if (self.rect.centerx < 0) or (self.rect.centerx >= gv.screen_width):
                self.move_speed *= -1
                self.rect.y += 40
        
        if pygame.sprite.spritecollide(self, game_group['bullet_group'], True):
            self.hp -= 1
            bullet_hit_fx.play()

            if self.hp == 0:
                explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
                game_group['explosion_group'].add(explosion)
                self.kill()
        

        # boss shoot
        if random.random() < self.bullet_ratio:
            boss_bullet = Alien_Bullets(
                    self.rect.centerx, 
                    self.rect.bottom, 
                    bullet_speed=self.bullet_speed
                )
            game_group['alien_bullet_group'].add(boss_bullet)
```

<h2 id="7-add-boss-laser"> 7. Add Boss Laser </h2>

- add update method in `Boss` class
```py
gameobjects.py

class Boss(pygame.sprite.Sprite):
    ...

    # Step 6: Add Boss. Add your code here
    def update(self, game_group):
        ...

        # Step 7: Add Boss Laser. Add your code here
        # charge laser
        if (time_now - self.last_boss_laser > self.laser_cooldown):
            self.charge_laser_obj = ChargeLaser(self.rect.centerx, self.rect.bottom, 2)
            game_group['charge_laser_group'].add(self.charge_laser_obj)
            self.last_boss_laser = time_now
        
        # shoot laser
        if (self.charge_laser_obj) and (self.charge_laser_obj.is_finish) and (self.boss_laser_obj == None):
            self.is_shoot_laser = True
            self.boss_laser_obj = Laser(self.rect.centerx, self.rect.bottom + 400, 2)
            game_group['boss_laser_group'].add(self.boss_laser_obj)

        # check if finish shoot laser, reset it
        if self.boss_laser_obj and self.boss_laser_obj.is_finish:
            self.boss_laser_obj = None
            self.charge_laser_obj = None
            self.is_shoot_laser = False
```

<h2 id="8-add-multiple-level"> 8. Add Multiple Level  </h2>

- add boss spawn condition
```py
# main.py
    ...

    while run:

        if countdown > 0:
            ...
        
        else:
            ...
        
        # check win the current level
        # Step 8: Add Multiple Level . Add your code here
        if len(alien_group) == 0 and len(boss_group) == 0 :
            gv.draw_text(
                screen,
                text='Win!', 
                font=gv.font40, 
                text_color=gv.white, 
                x=int(gv.screen_width / 2 - 30), 
                y=int(gv.screen_height / 2)
            )
            gv.draw_text(
                screen,
                text='Press N for next level', 
                font=gv.font40, 
                text_color=gv.white, 
                x=int(gv.screen_width / 2 - 150), 
                y=int(gv.screen_height / 2 + 50)
            )      
            level_win = True   
```

- You can adjust enemy properties when level up in `main.py` 
```py
# main.py 

    ... 
    # Increase enemy properties when level up 
    # - alien: alien_move_speed, alien_max_increase, alien_bullet_speed, alien_cooldown
    # - boss: boss_bullet_ratio, boss_laser_cooldown, boss_hp, boss_move_speed
    # Step 8: Add Multiple Level. You can ajust game level in here
    level_index = level - 1
    alien_move_speed = gv.alien_move_speed + level_index
    alien_max_increase = gv.alien_max_increase + level_index
    alien_bullet_speed = gv.alien_bullet_speed + level_index * 2
    alien_cooldown = gv.alien_cooldown - level_index * 200
    boss_bullet_ratio = gv.boss_bullet_ratio + level_index * 0.05
    boss_laser_cooldown = gv.boss_laser_cooldown - level_index * 1000
    boss_hp = gv.boss_hp + level_index * 2
    boss_move_speed = gv.boss_move_speed + level_index * 2
```

<h2 id="9-make-window-executable-file"> Make Window Executable File (.exe)  </h2>

windows key + r

type cmd

type pip install pyinstaller

close command prompt and open library

go to your project

highlight the path displayed at the top and change it to cmd

press enter; command prompt should open up

type pyinstaller --onefile -w [name of file].py

wait for it to finish