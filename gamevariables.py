import pygame

pygame.init()

# define fps
fps = 60

# width, height
screen_width = 600
screen_height = 800

# alien rows, cols
alien_rows = 0
alien_cols = 0
alien_cooldown = 1000 # bullet cooldown in milliseconds

# boss 
boss_cooldown = 500 # bullet cooldown in milliseconds
boss_laser_cooldown = 5000

# define fonts
font30 = pygame.font.SysFont('Constantia', 30)
font40 = pygame.font.SysFont('Constantia', 40)


# define colours
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)


# load image
bg = pygame.image.load("img/bg.png")


# define function for creating text
def draw_text(screen, text, font, text_color, x, y):
	img = font.render(text, True, text_color)
	screen.blit(img, (x, y))

def draw_bg(screen):
	screen.blit(bg, (0, 0))

# Block
obstacle_amount = 4
ostable_x_positions = [num * (screen_width/obstacle_amount) for num in range(obstacle_amount)]