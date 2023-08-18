import pygame

from src.utils.settings import *


class Player(pygame.sprite.Sprite):
	def __init__(self, pos) -> None:
		super().__init__()
		self.image = pygame.image.load("./assets/img/player.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (tile_scale, tile_scale * 2))
		# self.image.fill("#fbd05c")
		self.rect = self.image.get_rect(topleft = pos)
		self.direction = pygame.math.Vector2()
		self.speed = 6

		self.gravity = 0.8
		self.jump_speed = -16
		self.on_ground = False
		self.on_ceiling = False
		self.on_right = False
		self.on_left = False

	def input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_d]:
			self.direction.x = 1
		elif keys[pygame.K_a]:
			self.direction.x = -1
		else:
			self.direction.x = 0
		
		if keys[pygame.K_w] and self.on_ground == True:
			self.jump()
		
		if keys[pygame.K_s] and self.on_ground == True:
			self.crouch()

	def apply_gravity(self):
		self.direction.y += self.gravity
		self.rect.y += self.direction.y
	
	def jump(self):
		self.direction.y = self.jump_speed
		self.on_floor = False
	
	def crouch(self):
		self.speed = 3

	def update(self):
		self.speed = 6
		self.input()