import pygame
from settings import *
from circle.circle import Circle


class CircleGroup(pygame.sprite.Group):
    def __init__(self, pcmc):
        super().__init__()
        self.pcmc = pcmc
        if self.pcmc:
            self.create_pcmc()

    def create_pcmc(self):
        for i in range(720):
            Circle(self, small_cir_rad, i/2, "yellow")
            Circle(self, big_cir_rad, i/2, "red")
