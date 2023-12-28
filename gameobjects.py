import pygame
from pygame import mixer
import gamevariable as gv

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


	def update(self):
		# set movement speed
		speed = 8

		# get key press
		key = pygame.key.get_pressed()
		if key[pygame.K_LEFT] and self.rect.left > 0:
			self.rect.x -= speed
		if key[pygame.K_RIGHT] and self.rect.right < gv.screen_width:
			self.rect.x += speed
