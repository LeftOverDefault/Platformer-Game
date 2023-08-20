import pygame

from src.utils.settings import *


class Button:
    def __init__(self, text, font, surface_path, pos) -> None:
        self.display_surface = pygame.display.get_surface()

        self.image = pygame.image.load(surface_path).convert_alpha()
        # self.image = pygame.transform.scale(self.image, (tile_scale * (4 * 1.5), tile_scale * 1.5))
        self.image = pygame.transform.scale(self.image, (tile_scale * 6, tile_scale * 1.5))
        self.rect = self.image.get_rect(topleft = pos)
        
        self.text_surface = font.render(text, False, "#e6ecdf")
        self.text_rect = self.text_surface.get_rect(center = (self.rect.centerx, self.rect.centery - 2))
        self.shadow_text_surface = font.render(text, False, "#030015")
        self.shadow_text_rect = self.text_surface.get_rect(center = (self.rect.centerx, self.rect.centery + 2))

        self.pressed = False
    
    def draw(self):
        self.display_surface.blit(self.image, self.rect)
        self.display_surface.blit(self.shadow_text_surface, self.shadow_text_rect)
        self.display_surface.blit(self.text_surface, self.text_rect)
        self.click()
    
    def click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            # Hover
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed == True:
                    self.pressed = False
        else:
            # No Hover
            pass