import pygame
from src.utils.settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size) -> None:
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft = pos)


class StaticTile(Tile):
    def __init__(self, pos, size, surface) -> None:
        super().__init__(pos, size)
        self.image = surface
        self.image = pygame.transform.scale(self.image, (tile_scale, tile_scale))