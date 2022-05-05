import pygame
from settings import *


class CameraGroup(pygame.sprite.Group):
    def __init__(self, all_sprites_groups):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.offset = pygame.math.Vector2()
        self.pcmc_vec = pygame.math.Vector2()
        self.all_sprites_groups = all_sprites_groups
        self.player = self.all_sprites_groups["player"].get_player()
        self.player.set_pcmc_vec(self.pcmc_vec)
        # region box setup [nessary]
        self.camera_boarders = {
            "left": 200,
            "right": 200,
            "top": 200,
            "bottom": 200
        }
        l = self.camera_boarders["left"]
        t = self.camera_boarders["top"]
        w = self.width - \
            self.camera_boarders["right"] - self.camera_boarders["left"]
        h = self.height - \
            self.camera_boarders["bottom"] - self.camera_boarders["top"]
        self.camera_rect = pygame.Rect(l, t, w, h)
        # endregion
        # region zoom setup [optional]
        self.keyboard_speed = 5
        self.mouse_speed = 0.4
        self.zoom_scale = 1
        self.min_zoom_scale = 0.5
        self.max_zoom_scale = 2
        self.internal_surface_size = (
            self.width * 1/self.min_zoom_scale, self.height * 1/self.min_zoom_scale
        )
        self.internal_surface = pygame.Surface(
            self.internal_surface_size, pygame.SRCALPHA
        )
        self.internal_rect = self.internal_surface.get_rect(
            center=(self.width//2, self.height//2)
        )
        self.internal_surface_size_vector = pygame.math.Vector2(
            self.internal_surface_size
        )
        self.internal_offset = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surface_size[0] // 2 - \
            self.width // 2
        self.internal_offset.y = self.internal_surface_size[1] // 2 - \
            self.height // 2
        # endregion

    def sprites(self):
        sprites = []
        for group in self.all_sprites_groups.values():
            sprites += group.sprites()
        return sprites

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.width//2
        self.offset.y = target.rect.centery - self.height//2

    def box_target_camera(self, target):
        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom

        self.offset.x = self.camera_rect.left - self.camera_boarders["left"]
        self.offset.y = self.camera_rect.top - self.camera_boarders["top"]

    def keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.offset.x -= self.keyboard_speed
        if keys[pygame.K_d]:
            self.offset.x += self.keyboard_speed
        if keys[pygame.K_w]:
            self.offset.y -= self.keyboard_speed
        if keys[pygame.K_s]:
            self.offset.y += self.keyboard_speed

    def mouse_control(self):
        mouse = pygame.math.Vector2(pygame.mouse.get_pos())
        mouse_offset_vector = pygame.math.Vector2()

        left_border = self.camera_boarders["left"]
        top_border = self.camera_boarders["top"]
        right_border = self.width - self.camera_boarders["right"]
        bottom_border = self.height - self.camera_boarders["bottom"]

        if top_border < mouse.y < bottom_border:
            if mouse.x < left_border:
                mouse_offset_vector.x = mouse.x - left_border
                pygame.mouse.set_pos(left_border, mouse.y)
            if mouse.x > right_border:
                mouse_offset_vector.x = mouse.x - right_border
                pygame.mouse.set_pos(right_border, mouse.y)
        elif mouse.y < top_border:
            if mouse.x < left_border:
                mouse_offset_vector = mouse - \
                    pygame.math.Vector2(left_border, top_border)
                pygame.mouse.set_pos(left_border, top_border)
            if mouse.x > right_border:
                mouse_offset_vector = mouse - \
                    pygame.math.Vector2(right_border, top_border)
                pygame.mouse.set_pos(right_border, top_border)
        elif mouse.y > bottom_border:
            if mouse.x < left_border:
                mouse_offset_vector = mouse - \
                    pygame.math.Vector2(left_border, bottom_border)
                pygame.mouse.set_pos(left_border, bottom_border)
            if mouse.x > right_border:
                mouse_offset_vector = mouse - \
                    pygame.math.Vector2(right_border, bottom_border)
                pygame.mouse.set_pos(right_border, bottom_border)

        if left_border < mouse.x < right_border:
            if mouse.y < top_border:
                mouse_offset_vector.y = mouse.y - top_border
                pygame.mouse.set_pos(mouse.x, top_border)
            if mouse.y > bottom_border:
                mouse_offset_vector.y = mouse.y - bottom_border
                pygame.mouse.set_pos(mouse.x, bottom_border)

        self.offset += mouse_offset_vector * self.mouse_speed

    def zoom_keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.zoom_scale += 0.1
        if keys[pygame.K_e]:
            self.zoom_scale -= 0.1
        if self.zoom_scale < self.min_zoom_scale:
            self.zoom_scale = self.min_zoom_scale
        if self.zoom_scale > self.max_zoom_scale:
            self.zoom_scale = self.max_zoom_scale

    def pre_zoom(self):
        self.zoom_keyboard_control()
        self.offset -= self.internal_offset
        self.internal_surface.fill(background_color)
        self.surface = self.internal_surface

    def post_zoom(self):
        scaled_surface = pygame.transform.scale(
            self.internal_surface, self.internal_surface_size_vector * self.zoom_scale
        )
        scaled_rect = scaled_surface.get_rect(
            center=(self.width//2, self.height//2)
        )
        self.screen.blit(scaled_surface, scaled_rect)

    def plan_camera_mouse_control(self):
        mouse = pygame.mouse.get_pos()
        mouse_vec = pygame.math.Vector2(
            mouse[0]-self.width//2,
            mouse[1]-self.height//2
        )
        percent = min(max(mouse_vec.magnitude()-small_cir_rad, 0) /
                      (big_cir_rad-small_cir_rad), 1)
        if mouse_vec.magnitude() != 0:
            mouse_vec.normalize_ip()
        self.pcmc_vec.x = mouse_vec.x * percent * 100
        self.pcmc_vec.y = mouse_vec.y * percent * 100

        self.offset += self.pcmc_vec

    def camera_render(self):
        self.surface = self.screen
        self.center_target_camera(self.player)
        # self.box_target_camera(self.player)
        # self.keyboard_control()
        # self.mouse_control()
        self.plan_camera_mouse_control()

        # self.pre_zoom()

        # all sprites
        sprites = self.sprites()
        for sprite in sprites:
            if sprite == self.player:
                continue
            if sprite in self.all_sprites_groups["circle"]:
                continue
            if sprite in self.all_sprites_groups["UI"]:
                continue

            offset_pos = sprite.rect.topleft - self.offset
            if offset_pos.x < -100 or offset_pos.y < -100 or offset_pos.x > self.width + 100 or offset_pos.y > self.height + 100:
                continue
            self.surface.blit(sprite.image, offset_pos)

        for sprite in self.all_sprites_groups["circle"]:
            self.surface.blit(sprite.image, sprite.rect)
        # move target point
        self.player.draw_move_target(self.surface, self.offset)
        # player
        offset_pos = self.player.rect.topleft - self.offset
        self.surface.blit(self.player.image, offset_pos)
        # self.post_zoom()
        pass
