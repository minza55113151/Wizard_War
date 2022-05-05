import pygame
from settings import *
import math

"""
projectile types have 8 types
1.water(q)
2.heal(w)
3.shield(e)
4.ice(r)
5.thunder(a)
6.death(s)
7.stone(d)
8.fire(f)
"""


class UIElement(pygame.sprite.Sprite):
    def __init__(self, group, pos, element, key):
        super().__init__(group)
        self.radius = UI_element_image_radius
        self.key = key
        self.key_img = UI_element_key_images[key]
        if element == "water":
            self.img1 = UI_water_image_1
            self.img2 = UI_water_image_2
            self.img3 = UI_water_image_3
        if element == "heal":
            self.img1 = UI_heal_image_1
            self.img2 = UI_heal_image_2
            self.img3 = UI_heal_image_3
        if element == "shield":
            self.img1 = UI_shield_image_1
            self.img2 = UI_shield_image_2
            self.img3 = UI_shield_image_3
        if element == "ice":
            self.img1 = UI_ice_image_1
            self.img2 = UI_ice_image_2
            self.img3 = UI_ice_image_3
        if element == "thunder":
            self.img1 = UI_thunder_image_1
            self.img2 = UI_thunder_image_2
            self.img3 = UI_thunder_image_3
        if element == "death":
            self.img1 = UI_death_image_1
            self.img2 = UI_death_image_2
            self.img3 = UI_death_image_3
        if element == "stone":
            self.img1 = UI_stone_image_1
            self.img2 = UI_stone_image_2
            self.img3 = UI_stone_image_3
        if element == "fire":
            self.img1 = UI_fire_image_1
            self.img2 = UI_fire_image_2
            self.img3 = UI_fire_image_3
        self.img1.blit(self.key_img, UI_element_key_image_offset)
        self.img2.blit(self.key_img, UI_element_key_image_offset)
        self.img3.blit(self.key_img, UI_element_key_image_offset)
        self.image = self.img1
        self.rect = self.image.get_rect(topleft=pos)

        self.hovered = False
        self.pressed = False

    def collide_mouse(self):
        x1, y1 = pygame.mouse.get_pos()
        x2, y2 = self.rect.center
        distance = math.hypot(x1 - x2, y1 - y2)
        if distance <= self.radius:
            return True
        return False

    def hover(self):
        if self.collide_mouse():
            self.hovered = True

    def press(self):
        keys = pygame.key.get_pressed()
        if keys[self.key] or (pygame.mouse.get_pressed()[0] and self.collide_mouse()):
            self.pressed = True

    def animate(self):
        if self.pressed:
            self.image = self.img3
        elif self.hovered:
            self.image = self.img2
        else:
            self.image = self.img1
        self.rect = self.image.get_rect(center=self.rect.center)
        self.hovered = False
        self.pressed = False

    def update(self):
        self.hover()
        self.press()
        self.animate()


class UISkill(pygame.sprite.Sprite):
    def __init__(self, group, pos, skill, key):
        super().__init__(group)
        self.img1 = create_surface(
            UI_element_image_size, (0, 0, 0), (0, 0, 0)
        )
        self.img2 = create_surface(
            UI_element_image_size, (0, 0, 0), (0, 0, 0)
        )
        self.image = self.img1
        self.rect = self.image.get_rect(topleft=pos)
        self.key = key
        self.hovered = False
        self.pressed = False
        if skill == "running":
            pass
        if skill == "revive":
            pass
        if skill == "reaper":
            pass
        if skill == "meteor":
            pass

    def collide_mouse(self):
        x1, y1 = pygame.mouse.get_pos()
        x2, y2 = self.rect.center
        distance = math.hypot(x1 - x2, y1 - y2)
        if distance <= self.radius:
            return True
        return False

    def hover(self):
        if self.collide_mouse():
            self.hovered = True

    def press(self):
        keys = pygame.key.get_pressed()
        if keys[self.key]:
            self.pressed = True

    def animate(self):
        if self.hovered or self.pressed:
            self.image = self.img2
        else:
            self.image = self.img1
        self.hovered = False
        self.pressed = False

    def update(self):
        self.hover()
        self.press()
        self.animate()


class UIGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.create_element()

    def create_element(self):
        order = UI_element_order
        keys = UI_element_keys
        k = 0
        stepx = UI_element_image_size[0] + 1
        stepy = UI_element_image_size[1] - 1
        for i in range(2):
            for j in range(4):
                x = width//2 - (10 - i) * stepx//2 + j * stepx
                y = height - 2 * stepy + i * stepy
                UIElement(self, (x, y), order[k], keys[k])
                print(x, y, order[k])
                k += 1

    def draw(self):
        for sprite in self.sprites():
            self.screen.blit(sprite.image, sprite.rect)

    def update(self, *args, **kwargs):
        for sprite in self.sprites():
            sprite.update()
