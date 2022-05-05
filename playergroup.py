import pygame
from player import Player


class PlayerGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def get_player(self):
        for player in self.sprites():
            if player.control:
                return player

    def create_player(self, pos, skin, name, control=False, **kwargs):
        return Player(pos, skin, name, control, **kwargs)
