import pygame

from src.utils.settings import *


class CameraGroup(pygame.sprite.Group):
    def __init__(self, layers) -> None:
        super().__init__()
        self.ground_group = layers["terrain"]
        # self.liquid_group = liquid_group
        self.player_group = layers["player"]
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

        # Center Camera
        self.x_distance_to_center = self.display_surface.get_size()[0] // 2
        self.y_distance_to_center = self.display_surface.get_size()[1] // 2

        # Box Camera
        self.camera_borders = {"left": 200, "right": 200, "top": 100, "bottom": 100}
        left = self.camera_borders["left"]
        top = self.camera_borders["top"]
        width = self.display_surface.get_size()[0] - (self.camera_borders["left"] + self.camera_borders["right"])
        height = self.display_surface.get_size()[1] - (self.camera_borders["top"] + self.camera_borders["bottom"])
        self.camera_rect = pygame.Rect(left, top, width, height)

        # Background
        self.background_surface = pygame.image.load("./assets/img/background.png").convert_alpha()
        self.background_surface = pygame.transform.scale(self.background_surface, (screen_width, screen_height))
        self.background_rect = self.background_surface.get_rect(topleft = (0, 0))

        self.keyboard_speed = 5
        self.mouse_speed = 0.075

        self.zoom_scale = 0.8
        # self.internal_surface_size = (screen_width, screen_height)
        self.internal_surface = self.display_surface
        # self.internal_surface = pygame.Surface(self.internal_surface_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surface.get_rect(center = (self.x_distance_to_center, self.y_distance_to_center))
        # self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surface_size)
        self.internal_offset = pygame.math.Vector2()
        self.internal_offset.x = screen_width // 2 - self.x_distance_to_center
        self.internal_offset.y = screen_height // 2 - self.y_distance_to_center

    def center_camera(self, target):
        self.offset.x += (target.rect.centerx - self.x_distance_to_center - self.offset.x) / 25
        self.offset.y += (target.rect.centery - self.y_distance_to_center- self.offset.y) / 25

    def box_camera(self, target):

        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right

        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom

        self.offset.x = self.camera_rect.left - self.camera_borders["left"]
        self.offset.y = self.camera_rect.top - self.camera_borders["top"]
    
    def keyboard_camera(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.camera_rect.x += self.keyboard_speed
        if keys[pygame.K_LEFT]:
            self.camera_rect.x -= self.keyboard_speed
        if keys[pygame.K_UP]:
            self.camera_rect.y -= self.keyboard_speed
        if keys[pygame.K_DOWN]:
            self.camera_rect.y += self.keyboard_speed
        
        self.offset.x = self.camera_rect.left - self.camera_borders["left"]
        self.offset.y = self.camera_rect.top - self.camera_borders["top"]

    def mouse_camera(self):
        pygame.event.set_grab(True)
        mouse = pygame.math.Vector2(pygame.mouse.get_pos())
        mouse_offset_vector = pygame.math.Vector2()

        left_border = self.camera_borders["left"]
        top_border = self.camera_borders["top"]
        right_border = self.display_surface.get_size()[0] - self.camera_borders["right"]
        bottom_border = self.display_surface.get_size()[1] - self.camera_borders["bottom"]

        if top_border < mouse.y < bottom_border:
            if mouse.x < left_border:
                mouse_offset_vector.x = mouse.x - left_border
            if mouse.x > right_border:
                mouse_offset_vector.x = mouse.x - right_border
        elif mouse.y < top_border:
            if mouse.x < left_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(left_border, top_border)
            if mouse.x > right_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(right_border, top_border)
        elif mouse.y > bottom_border:
            if mouse.x < left_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(left_border, bottom_border)
            if mouse.x > right_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(right_border, bottom_border)
        if left_border < mouse.x < right_border:
            if mouse.y < top_border:
                mouse_offset_vector.y = mouse.y - top_border
            if mouse.y > bottom_border:
                mouse_offset_vector.y = mouse.y - bottom_border
        
        self.offset += mouse_offset_vector * self.mouse_speed

    def zoom_keyboard_camera(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_KP_PLUS]:
            self.zoom_scale += 0.1
        if keys[pygame.K_KP_MINUS]:
            self.zoom_scale -= 0.1

    def custom_draw(self, player):
        self.center_camera(player)
        # self.box_camera(player)
        # self.keyboard_camera()
        # self.mouse_camera()
        # self.zoom_keyboard_camera()
        # if self.zoom_scale < 0.5:
        #     self.zoom_scale = 0.5
        # if self.zoom_scale > 0.8:
        #     self.zoom_scale = 0.8
        
        
        self.display_surface.blit(self.background_surface, (0, 0))
        # self.internal_surface.fill("#ffffff00")

        # background_offset_position = self.background_rect.topleft - (self.offset + self.internal_offset)

        # Background

        # Active ELements
        for sprite in self.ground_group.sprites():
            offset_position = sprite.rect.topleft - self.offset + self.internal_offset
            self.internal_surface.blit(sprite.image.convert_alpha(), offset_position)
        
        # for sprite in self.liquid_group.sprites():
        #     offset_position = sprite.rect.topleft - self.offset + self.internal_offset
        #     self.internal_surface.blit(sprite.image, offset_position)
        
        for sprite in self.player_group.sprites():
            offset_position = sprite.rect.topleft - self.offset + self.internal_offset
            self.internal_surface.blit(sprite.image, offset_position)

        # scaled_surface = pygame.transform.scale(self.internal_surface, self.internal_surface_size_vector * self.zoom_scale)
        # scaled_rect = scaled_surface.get_rect(center = (self.x_distance_to_center, self.y_distance_to_center))
        
        # self.display_surface.blit(self.background_surface, self.background_rect)
        self.display_surface.blit(self.internal_surface, self.internal_rect)