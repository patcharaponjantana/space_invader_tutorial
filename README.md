# Space Invader Tutorial

ref:  https://www.youtube.com/watch?v=PFMoo_dvhyw 

# Content
- run project 
- add enemies
- add gameover condition
- add character bullet
- add enemy bullets
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
- add colision condition
