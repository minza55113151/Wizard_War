import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, group, pos, color):
        super().__init__(group)
        self.image = pygame.Surface(tile_image_size).convert()
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)
