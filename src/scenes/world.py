import pygame
import sys

from src.classes.camera import CameraGroup
from src.classes.player import Player
from src.classes.tile import StaticTile
from src.utils.settings import *
from src.utils.support import import_csv_layout, import_cut_graphics


class World:
	def __init__(self, world_data, surface) -> None:
		self.display_surface = surface
		self.running = True

		terrain_layout = import_csv_layout(world_data["grass"])
		self.terrain_group = self.create_tile_group(terrain_layout, "grass")

		player_layout = import_csv_layout(world_data["player"])
		self.player_group = pygame.sprite.GroupSingle()
		self.player_setup(player_layout)
		self.layer_dict = {
			"grass": self.terrain_group,
			"player": self.player_group
		}
		self.camera_group = CameraGroup(self.layer_dict)
	
	def create_tile_group(self, layout, type):
		sprite_group = pygame.sprite.Group()

		for row_index, row in enumerate(layout):
			for column_index, value in enumerate(row):
				if value != "-1":
					x = column_index * tile_scale
					y = row_index * tile_scale
					if type == "grass":
						grass_tile_list = import_cut_graphics("./assets/img/tilesheets/grass.png")
						surface = grass_tile_list[int(value)]
						sprite = StaticTile((x, y), tile_scale, surface)
						sprite_group.add(sprite)
		
		return sprite_group
	
	def player_setup(self, layout):
		for row_index, row in enumerate(layout):
			for column_index, value in enumerate(row):
				x = column_index * tile_scale
				y = row_index * tile_scale
				if value == "0":
					self.player = Player((x, y))
					self.player_group.add(self.player)
	
	def horizontal_movement_collision(self):
		player = self.player
		player.rect.x += player.direction.x * player.speed

		for sprite in self.camera_group.grass_group.sprites():
			if sprite.rect.colliderect(player.rect):
				if player.direction.x < 0:
					player.rect.left = sprite.rect.right
					player.on_left = True
					self.current_x = player.rect.left
				elif player.direction.x > 0:
					player.rect.right = sprite.rect.left
					player.on_right = True
					self.current_x = player.rect.right
		
		if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
			player.on_left = False
		if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
			player.on_right = False

	def vertical_movement_collision(self):
		player = self.player
		player.apply_gravity()

		for sprite in self.camera_group.grass_group.sprites():
			if sprite.rect.colliderect(player.rect):
				if player.direction.y > 0:
					player.rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.on_ground = True
				elif player.direction.y < 0:
					player.rect.top = sprite.rect.bottom
					player.direction.y = 0
					player.on_ceiling = True
		
		if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
			player.on_ground = False
		if player.on_ceiling and player.direction.y > 0:
			player.on_ceiling = False

	def update_groups(self):
		self.horizontal_movement_collision()
		self.vertical_movement_collision()
		self.terrain_group.update()
		self.player_group.update()

	def run(self):
		while self.running == True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			self.update_groups()
			self.camera_group.custom_draw(self.player)
			pygame.display.update()