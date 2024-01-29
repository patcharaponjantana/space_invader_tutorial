import pygame

pygame.init()

# --------------- Game Config ---------------
# define fps
fps = 60

# width, height
screen_width = 600
screen_height = 800

# define fonts
font30 = pygame.font.SysFont('Constantia', 30)
font40 = pygame.font.SysFont('Constantia', 40)


# define colours
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)


# load image
bg = pygame.image.load("img/bg.png")



# --------------- Spaceship ---------------
spaceship_bullet_speed = 6
spaceship_move_speed = 8
spaceship_shoot_cooldown = 1000 # in milliseconds

# --------------- Alien ---------------
alien_rows = 5
alien_cols = 5
alien_cooldown = 1000 # bullet cooldown in milliseconds
alien_move_speed = 3
alien_max_increase = 3
alien_bullet_speed = 8

# --------------- Boss --------------- 
# boss_bullet_cooldown = 500 # bullet cooldown in milliseconds
boss_bullet_ratio = 0.08 # range is 0 to 1
boss_laser_cooldown = 10000 # milliseconds
boss_hp = 8
boss_move_speed = 5


# --------------- Obstacle ---------------  
obstacle_amount = 4
ostable_x_positions = [num * (screen_width/obstacle_amount) for num in range(obstacle_amount)]


# --------------- Utility Functions ---------------
# define function for creating text
def draw_text(screen, text, font, text_color, x, y):
	img = font.render(text, True, text_color)
	screen.blit(img, (x, y))

def draw_bg(screen):
	screen.blit(bg, (0, 0))

