import random
import pygame
from projectile import Projectile
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, skin, name, control=False, **kwargs):
        self.screen = pygame.display.get_surface()

        self.client_sending_data = kwargs.get("client_sending_data")
        self.all_sprites_group = kwargs["all_sprites_group"]
        super().__init__(self.all_sprites_group["player"])
        self.init_player_image(pos, skin, name)
        self.init_move_target_image()

        self.hitbox_image = player_hitbox_image
        self.hitbox = self.rect.inflate(*player_hitbox_size_dif)
        self.skin = skin
        self.name = name
        self.control = control
        self.target_pos = pos
        self.normal_speed = player_normal_speed
        self.slow_speed = player_slow_speed
        self.speed = self.normal_speed
        self.rotate_speed = player_rotation_speed
        self.max_hp = player_max_hp
        self.hp = self.max_hp
        self.max_mp = player_max_mp
        self.mp = self.max_mp

        self.bullets = []
        self.move_direction = pygame.math.Vector2()
        self.face_direction = pygame.math.Vector2()
        self.pcmc_vec = pygame.math.Vector2()
        self.is_shoot = False
        self.angle = 0

    def set_pcmc_vec(self, pcmc_vec):
        self.pcmc_vec = pcmc_vec

    def init_player_image(self, pos, skin, name):
        # setup original image
        self.origin_images = player_images_set[int(skin)-1]
        # setup text
        # draw_text_to_surface(
        #     surface=self.origin_image,
        #     font=create_font(10),
        #     text=name,
        #     text_color="white",
        #     bg_color=(1, 1, 1),
        #     pos=[
        #         player_image_size[0]//2,
        #         player_image_size[1]//2
        #     ]
        # )

        # setup image and rect
        self.image = self.origin_images[0]
        self.rect = self.image.get_rect(center=pos)

        self.name_image, self.name_rect = create_text_surface(
            (self.rect.width*2, self.rect.height),
            (0, 0, 0),
            create_font(25, "calibri", bold=True),
            "MinZung",
            (1, 1, 1),
            center=(
                self.rect.centerx,
                self.rect.centery - player_image_size[1]//2 -
                player_hp_image_size[1] * 6
            )
        )
        print(self.name_image, self.name_rect)

    def init_move_target_image(self):
        self.move_target_images = player_move_target_images
        self.move_target_image_len = len(self.move_target_images)
        self.move_target_image_frame = 0
        self.move_target_image = self.move_target_images[self.move_target_image_frame]
        self.move_target_rect = self.move_target_image.get_rect()

    def draw_hitbox(self, screen, offset=pygame.math.Vector2(0, 0)):
        offset_pos = self.hitbox.topleft - offset
        screen.blit(self.hitbox_image, offset_pos)

    def draw_move_target(self, screen, offset=pygame.math.Vector2(0, 0)):
        if self.move_direction.magnitude() != 0:
            self.move_target_rect = self.move_target_image.get_rect(
                center=self.target_pos
            )
            offset_pos = self.move_target_rect.topleft - offset
            screen.blit(self.move_target_image, offset_pos)

    def draw_hp(self, screen, offset=pygame.math.Vector2(0, 0)):
        self.hp_border_image = create_surface(
            player_hp_border_image_size, (30, 20, 20)
        )
        self.hp_image_size = (
            (self.hp/self.max_hp) * player_hp_image_size[0],
            player_hp_image_size[1]
        )
        self.hp_image = create_surface(self.hp_image_size, (0, 120, 0))
        self.hp_border_image.blit(self.hp_image, player_hp_border_offset)
        self.hp_image = self.hp_border_image
        self.hp_rect = self.hp_image.get_rect(
            center=(
                self.rect.centerx,
                self.rect.centery - player_image_size[1]//2 -
                player_hp_image_size[1] * 2
            )
        )
        offset_pos = self.hp_rect.topleft - offset
        screen.blit(self.hp_image, offset_pos)

        self.hp = random.randint(0, self.max_hp)

    def draw_name(self, screen, offset=pygame.math.Vector2(0, 0)):
        self.name_rect.center = (
            self.rect.centerx,
            self.rect.centery - player_image_size[1]//2 -
            player_hp_image_size[1] * 6
        )
        offset_pos = self.name_rect.topleft - offset
        screen.blit(self.name_image, offset_pos)

    def animation(self):
        # move_target
        self.move_target_image_frame = (
            self.move_target_image_frame + player_move_target_animation_speed) % self.move_target_image_len
        self.move_target_image = self.move_target_images[int(
            self.move_target_image_frame)]
        self.image = self.origin_images[int(self.angle)]
        self.rect = self.image.get_rect(center=self.rect.center)

    # def keyboard(self):
    #     keys = pygame.key.get_pressed()
    #     if keys[pygame.K_w]:
    #         self.move_direction.y = -1
    #     elif keys[pygame.K_s]:
    #         self.move_direction.y = 1
    #     else:
    #         self.move_direction.y = 0

    #     if keys[pygame.K_a]:
    #         self.move_direction.x = -1
    #     elif keys[pygame.K_d]:
    #         self.move_direction.x = 1
    #     else:
    #         self.move_direction.x = 0

    def set_face_direction(self):
        mouse = pygame.mouse.get_pos()
        self.face_direction = pygame.math.Vector2(
            mouse[0] - width//2,
            mouse[1] - height//2
        )
        self.angle = self.face_direction.angle_to(
            pygame.math.Vector2(1, 0)
        ) + 180

    def set_target_pos(self):
        mouse = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[2]:
            self.target_pos = [
                int(mouse[0] - width//2 + self.rect.centerx + self.pcmc_vec.x),
                int(mouse[1] - height//2 + self.rect.centery + self.pcmc_vec.y)
            ]

    def shoot(self):
        # reset bullet and is_shoot
        if self.is_shoot:
            self.is_shoot = False
            self.bullets = []
        if pygame.mouse.get_pressed()[0]:
            if self.face_direction.magnitude() != 0:
                self.is_shoot = True
                if self.move_direction.magnitude() != 0:
                    self.bullet_direction = (self.face_direction.normalize() * projectile_speed +
                                             self.move_direction.normalize() * self.slow_speed).normalize()
                else:
                    self.bullet_direction = self.face_direction
                self.bullet_direction.normalize_ip()
                bullet = {
                    "pos": [self.rect.centerx, self.rect.centery],
                    "direction": [self.bullet_direction.x, self.bullet_direction.y]
                }
                self.bullets.append(bullet)
                Projectile(
                    self,
                    self.rect.center,
                    self.bullet_direction,
                    all_sprites_group=self.all_sprites_group
                )

    def move(self, dt):
        self.move_direction = pygame.math.Vector2(
            self.target_pos[0] - self.rect.centerx,
            self.target_pos[1] - self.rect.centery
        )
        if self.move_direction.magnitude() != 0:
            if self.move_direction.magnitude() < (self.move_direction.normalize() * self.speed * dt).magnitude():
                self.rect.center = self.target_pos
            else:
                self.move_direction.normalize_ip()
                self.rect.center += self.move_direction * self.speed * dt
        self.hitbox.center = self.rect.center

    def set_speed(self):
        if self.is_shoot:
            self.speed = self.slow_speed
        elif self.speed == self.slow_speed:
            self.speed = self.normal_speed

    def send_data(self):
        self.client_sending_data["skin"] = self.skin
        self.client_sending_data["target_pos"] = self.target_pos
        self.client_sending_data["angle"] = self.angle
        self.client_sending_data["speed"] = self.speed
        self.client_sending_data["hp"] = self.hp
        self.client_sending_data["mp"] = self.mp
        self.client_sending_data["event"]["bullets"] = self.bullets
        # def rotate(self):
        #     self.image = pygame.transform.rotate(self.origin_image, self.angle)
        #     self.rect = self.image.get_rect(center=self.rect.center)
        #     self.angle += self.rotate_speed

    def update(self, dt, *args, **kwargs):
        if self.control:
            self.set_face_direction()
            self.set_target_pos()
            self.shoot()
            # self.keyboard()
            self.set_speed()
            self.send_data()
        self.move(dt)
        self.animation()
