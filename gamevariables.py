import pygame

pygame.init()

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


# define function for creating text
def draw_text(screen, text, font, text_color, x, y):
	img = font.render(text, True, text_color)
	screen.blit(img, (x, y))

def draw_bg(screen):
	screen.blit(bg, (0, 0))

