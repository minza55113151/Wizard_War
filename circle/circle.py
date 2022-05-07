import pygame
from settings import *


class Circle(pygame.sprite.Sprite):
    def __init__(self, group, radius, angle, color):
        super().__init__(group)
        self.real_image = create_surface((2, 2), color)
        self.real_image_rect = self.real_image.get_rect()
        self.image = create_surface((radius*2, 2))
        self.image.blit(self.real_image, self.real_image_rect)
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=(width//2, height//2))
