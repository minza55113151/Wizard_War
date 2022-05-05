import pygame
from settings import *


class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, direction, **kwargs):
        self.all_sprites_group = kwargs["all_sprites_group"]
        super().__init__(self.all_sprites_group["projectile"])
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

    def bounce(self):
        if self.rect.x < 0 or self.rect.x > width:
            self.direction.x *= -1
        if self.rect.y < 0 or self.rect.y > height:
            self.direction.y *= -1

    # def rotate(self):
    #     self.image = pygame.transform.rotate(self.origin_image, self.angle)
    #     self.rect = self.image.get_rect(center=self.rect.center)
    #     self.angle += self.max_health - self.health

    def update(self, dt, *args, **kwargs):
        self.move(dt)
        # self.bounce()
        # self.rotate()
        self.life()
