import pygame
from settings import *


class Projectile(pygame.sprite.Sprite):
    def __init__(self, author, pos, direction, **kwargs):
        self.all_sprites_group = kwargs["all_sprites_group"]
        self.player_sprites = self.all_sprites_group["player"]
        super().__init__(self.all_sprites_group["projectile"])
        self.author = author
        self.direction = direction
        self.speed = projectile_speed
        # self.rotate_speed = projectile_rotation_speed
        self.max_health = projectile_max_health
        self.health = projectile_max_health
        self.origin_image = projectile_image
        self.origin_image = pygame.transform.scale(
            self.origin_image,
            projectile_image_size
        )
        self.origin_image = pygame.transform.rotate(
            self.origin_image,
            self.direction.angle_to(
                pygame.math.Vector2(1, 0)
            )
        )
        self.image = self.origin_image
        self.rect = self.image.get_rect(center=pos)

        self.angle = 0

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
        sprite = pygame.sprite.spritecollideany(self, self.player_sprites)
        if sprite != None and sprite != self.author:
            print(sprite.name)

    def update(self, dt, *args, **kwargs):
        self.move(dt)
        self.iscollide()
        self.life()
