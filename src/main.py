import sys

import pygame

from src.scenes.title_screen import TitleScreen
from src.utils.settings import *


class Main:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Platformer")

        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.fps = 60

        self.fullscreen = False
        self.running = True

        self.title_screen = TitleScreen()
    
    def run(self) -> None:
        while self.running == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.title_screen.run()

            self.clock.tick(self.fps)
            pygame.display.update()