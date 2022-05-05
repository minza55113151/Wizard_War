import pygame
from settings import *
from tile.tile import Tile
import random


class TileGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def create_random_tile(self, radius):
        for x in range(-radius, radius+1, tile_image_size[0]):
            for y in range(-radius, radius+1, tile_image_size[1]):
                if random.randint(0, 100) > 97:
                    r = random.randint(0, 255)
                    g = random.randint(0, 255)
                    b = random.randint(0, 255)
                    Tile(
                        self,
                        pos=(x, y),
                        color=(r, g, b),
                    )
