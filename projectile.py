import pygame
from settings import *


class Projectile(pygame.sprite.Sprite):
    def __init__(self, all_sprites_group, author, pos, direction, atk_type, element, images, **kwargs):
        self.all_sprites_group = all_sprites_group
        self.player_sprites = self.all_sprites_group["player"]
        super().__init__(self.all_sprites_group["projectile"])
        self.author = author
        self.direction = direction
        if atk_type == "spread":
            self.speed = projectile_spread_speed
            self.max_health = projectile_spread_max_health
        if atk_type == "laser":
            self.speed = projectile_laser_speed
            self.max_health = projectile_laser_max_health
        if atk_type == "projectile":
            self.speed = projectile_projectile_speed
            self.max_health = projectile_projectile_max_health
        if atk_type == "shield":
            self.speed = projectile_shield_speed
            self.max_health = projectile_shield_max_health
        self.health = self.max_health
        self.damage = kwargs.get("damage", 0)
        self.knockback = kwargs.get("knockback", 0)
        self.burn = kwargs.get("burn", 0)
        self.slow = kwargs.get("slow", 0)
        self.stun = kwargs.get("stun", 0)
        self.origin_images = images
        self.angle = direction.angle_to(
            pygame.math.Vector2(1, 0)
        ) + 180
        self.image = self.origin_images[int(self.angle)]
        self.rect = self.image.get_rect(center=pos)

    def move(self, dt):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.rect.x += int(self.direction.x * self.speed * dt)
        self.rect.y += int(self.direction.y * self.speed * dt)

    def life(self):
        if self.health <= 0:
            self.kill()
        self.health -= 1

    def iscollide(self):
        sprite = self.player_sprites.collide_player(self)
        if sprite != None and sprite != self.author:
            print(sprite.name)
            if self.stun:
                print("stun")
            if self.knockback:
                print("knockback")
            if self.burn:
                print("burn")
            if self.slow:
                print("slow")
            sprite.hp -= self.damage
            self.kill()

    def update(self, dt, *args, **kwargs):
        self.move(dt)
        self.iscollide()
        self.life()


#
