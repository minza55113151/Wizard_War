import pygame
from settings import *
from projectile import Projectile


class ProjectileGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def set_all_sprites_group(self, all_sprites_group):
        self.all_sprites_group = all_sprites_group

    def update(self, *args, **kwargs):
        for sprite in self.sprites():
            sprite.update(*args, **kwargs)

    # def kwargs_element_stat(self, element):
    #     kwargs = {"damage": 0, "knockback": 0,
    #               "burn": 0, "slow": 0, "stun": 0}
    #     kwargs["damage"] += projectile_data[element].get("damage", 0)
    #     kwargs["knockback"] += projectile_data[element].get(
    #         "knockback", 0)
    #     kwargs["burn"] += projectile_data[element].get("burn", 0)
    #     kwargs["slow"] += projectile_data[element].get("slow", 0)
    #     kwargs["stun"] += projectile_data[element].get("stun", 0)
    #     return kwargs

    def create_projectile(self, author, pos, direction, element):
        kwargs = projectile_data[element]
        if element == "water":
            atk_type = "spread"
            images = projectile_water_images
        if element == "heal":
            atk_type = "laser"
            images = projectile_heal_images
        if element == "shield":
            atk_type = "shield"
            images = projectile_shield_images
            pos += direction * projectile_shield_offset
        if element == "ice":
            atk_type = "spread"
            images = projectile_ice_images
        if element == "thunder":
            atk_type = "spread"
            images = projectile_thunder_images
        if element == "death":
            atk_type = "laser"
            images = projectile_death_images
        if element == "stone":
            atk_type = "projectile"
            images = projectile_stone_images
        if element == "fire":
            atk_type = "spread"
            images = projectile_fire_images
        if atk_type == "spread":
            direction_1 = direction.rotate(-15)
            direction_2 = direction.rotate(-7.5)
            direction_3 = direction
            direction_4 = direction.rotate(7.5)
            direction_5 = direction.rotate(15)
            Projectile(self.all_sprites_group, author, pos,
                       direction_1, atk_type, element, images, **kwargs)
            Projectile(self.all_sprites_group, author, pos,
                       direction_2, atk_type, element, images, **kwargs)
            Projectile(self.all_sprites_group, author, pos,
                       direction_3, atk_type, element, images, **kwargs)
            Projectile(self.all_sprites_group, author, pos,
                       direction_4, atk_type, element, images, **kwargs)
            Projectile(self.all_sprites_group, author, pos,
                       direction_5, atk_type, element, images, **kwargs)
        else:
            Projectile(self.all_sprites_group, author, pos,
                       direction, atk_type, element, images, **kwargs)

        # if "shield" in elements:
        #     atk_type = "shield"
        #     images = projectile_shield_images
        #     pos += direction * projectile_shield_offset
        #     Projectile(
        #         self.all_sprites_group, author, pos, direction, atk_type, elements, images
        #     )
        # elif "stone" in elements:
        #     atk_type = "projectile"
        #     images = projectile_stone_images
        #     kwargs = self.kwargs_element_stat(elements)
        #     Projectile(
        #         self.all_sprites_group, author, pos, direction, atk_type, elements, images, **kwargs
        #     )
        # elif "heal" in elements or "death" in elements:
        #     atk_type = "laser"
        #     if "death" in elements:
        #         images = projectile_death_images
        #     elif "heal" in elements:
        #         images = projectile_heal_images
        #     kwargs = self.kwargs_element_stat(elements)
        #     Projectile(
        #         self.all_sprites_group, author, pos, direction, atk_type, elements, images, **kwargs
        #     )
        # else:
        #     atk_type = "spread"
        #     if "ice" == elements[0]:
        #         images = projectile_ice_images
        #     elif "fire" == elements[0]:
        #         images = projectile_fire_images
        #     elif "water" == elements[0]:
        #         images = projectile_water_images
        #     elif "thunder" == elements[0]:
        #         images = projectile_thunder_images
        #     kwargs = self.kwargs_element_stat(elements)
        #     direction_left = direction.rotate(-15)
        #     direction_right = direction.rotate(15)
        #     Projectile(
        #         self.all_sprites_group, author, pos, direction, atk_type, elements, images, **kwargs
        #     )
        #     Projectile(
        #         self.all_sprites_group, author, pos, direction_left, atk_type, elements, images, **kwargs
        #     )
        #     Projectile(
        #         self.all_sprites_group, author, pos, direction_right, atk_type, elements, images, **kwargs
        #     )
        # return None
        # if elements == ["water"]:
        #     atk_type = "spread"
        #     images = projectile_water_images
        #     direction_left = direction.rotate(-15)
        #     direction_right = direction.rotate(15)
        #     Projectile(
        #         self.all_sprites_group, author, pos, direction, atk_type, elements,
        #         images
        #     )
        #     Projectile(
        #         self.all_sprites_group, author, pos, direction_left, atk_type, elements,
        #         images
        #     )
        #     Projectile(
        #         self.all_sprites_group, author, pos, direction_right, atk_type, elements,
        #         images
        #     )
        # if elements == ["heal"]:
        #     atk_type = "laser"
        #     images = projectile_heal_images
        #     Projectile(
        #         self.all_sprites_group, author, pos, direction, atk_type, elements,
        #         images
        #     )
        # if elements == ["shield"]:
        #     pass
        # if elements == ["ice"]:
        #     atk_type = "spread"
        #     images = projectile_ice_images
        #     direction_left = direction.rotate(-15)
        #     direction_right = direction.rotate(15)
        #     Projectile(
        #         self.all_sprites_group, author, pos, direction, atk_type, elements,
        #         images
        #     )
        #     Projectile(
        #         self.all_sprites_group, author, pos, direction_left, atk_type, elements,
        #         images
        #     )
        #     Projectile(
        #         self.all_sprites_group, author, pos, direction_right, atk_type, elements,
        #         images
        #     )
        # if elements == ["thunder"]:
        #     atk_type = "spread"
        #     images = projectile_thunder_images
        #     direction_left = direction.rotate(-15)
        #     direction_right = direction.rotate(15)
        #     Projectile(
        #         self.all_sprites_group, author, pos, direction, atk_type, elements,
        #         images
        #     )
        #     Projectile(
        #         self.all_sprites_group, author, pos, direction_left, atk_type, elements,
        #         images
        #     )
        #     Projectile(
        #         self.all_sprites_group, author, pos, direction_right, atk_type, elements,
        #         images
        #     )
        # if elements == ["death"]:
        #     atk_type = "laser"
        #     images = projectile_death_images
        #     Projectile(
        #         self.all_sprites_group, author, pos, direction, atk_type, elements,
        #         images
        #     )
        # if elements == ["stone"]:
        #     pass
        # if elements == ["fire"]:
        #     atk_type = "spread"
        #     images = projectile_fire_images
        #     direction_left = direction.rotate(-15)
        #     direction_right = direction.rotate(15)
        #     Projectile(
        #         self.all_sprites_group, author, pos, direction, atk_type, elements,
        #         images
        #     )
        #     Projectile(
        #         self.all_sprites_group, author, pos, direction_left, atk_type, elements,
        #         images
        #     )
        #     Projectile(
        #         self.all_sprites_group, author, pos, direction_right, atk_type, elements,
        #         images
        #     )
