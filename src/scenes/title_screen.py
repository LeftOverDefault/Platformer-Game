import sys
import pygame

from src.classes.button import Button
from src.scenes.world import World
from src.utils.game_data import world_map
from src.utils.settings import *


class TitleScreen:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()
        self.running = True

        self.font = pygame.font.Font("./assets/font/font.ttf", 32)

        self.background = pygame.image.load("./assets/img/title_background.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        self.background_rect = self.background.get_rect(topleft = (0, 0))

        self.start_button = Button("Play", self.font, "./assets/img/buttonx64.png", (0, self.display_surface.get_size()[1] - (390)))
        self.multiplayer_button = Button("Multiplayer", self.font, "./assets/img/buttonx64.png", (0, self.display_surface.get_size()[1] - (390 - (6 * 24))))
        self.settings_button = Button("Settings", self.font, "./assets/img/buttonx64.png", (self.display_surface.get_size()[0] - (64 * 6), self.display_surface.get_size()[1] - (390)))
        self.quit_button = Button("Quit", self.font, "./assets/img/buttonx64.png", (self.display_surface.get_size()[0] - (64 * 6), self.display_surface.get_size()[1] - (390 - (6 * 24))))

        self.world = World(world_map, self.display_surface)
    
    def run(self):
        while self.running == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.display_surface.blit(self.background, self.background_rect)
            self.start_button.draw()
            self.multiplayer_button.draw()
            self.settings_button.draw()
            self.quit_button.draw()

            if self.start_button.pressed == True:
                self.running = False
                self.world.run()
            if self.multiplayer_button.pressed == True:
                pass
            if self.settings_button.pressed == True:
                pass
            if self.quit_button.pressed == True:
                pygame.quit()
                sys.exit()
            pygame.display.update()
