import pygame
from settings import *
from cameragroup import CameraGroup


class Layer:
    def __init__(self):
        # screen --------------------------------------------------------------
        self.screen = pygame.display.get_surface()
        # sprite groups -------------------------------------------------------
        self.camera = CameraGroup()
        # init cursor ---------------------------------------------------------
        self.init_cursor()

    def set_all_sprites_group(self, all_sprites_group):
        self.all_sprites_groups = all_sprites_group

    def set_UI_sprites(self, UI_sprites):
        self.UI_sprites = UI_sprites

    def init_cursor(self):
        self.cursor_image = cursor_image

    def render(self):
        self.screen.fill(background_color)
        # update
        self.update()
        # draw
        self.camera.camera_render()
        self.UI_sprites.draw()
        self.draw_cursor()
        # self.default_render(player)

    def default_render(self, player):
        self.screen.blit(self.background_image, self.background_rect)
        player.draw_move_target(self.screen)
        for sprite in self.sprites():
            self.screen.blit(sprite.image, sprite.rect)

    def draw_cursor(self):
        self.screen.blit(self.cursor_image, pygame.mouse.get_pos())

    def update(self):
        self.dt = get_dt(fps)
        for sprites_group in self.all_sprites_groups.values():
            sprites_group.update(self.dt)
