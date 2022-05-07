import pygame
from settings import *


class Menu:
    def __init__(self, data):
        self.screen = pygame.display.set_mode((width, height))
        self.data = data
        self.running = True
        self.side = width//40
        self.font = create_font(self.side)
        self.bg_color = (40, 30, 30)
        self.bt_color = (200, 200, 200)
        self.text_color = (1, 1, 1)

        pygame.mouse.set_visible(False)
        self.cursor_image = cursor_image

        self.init_menu()
        self.init_profile()
        self.init_setting()
        self.menu()

    def draw_cursor(self):
        self.screen.blit(self.cursor_image, pygame.mouse.get_pos())

    def init_menu(self):
        word = ["Play", "Profile", "Setting", "Exit"]
        self.logo_image, self.logo_rect = create_text_surface(
            (width, height//2), "black", create_font(self.side * 8, "calibri"),
            "Wizard War", self.text_color,
            center=(
                width//2,
                height//2 - self.side * 6
            )
        )
        self.menu_count = len(word)
        self.menu_box_size = (self.side*9, self.side*(4*2+5))
        self.menu_box_image = create_surface(self.menu_box_size, self.bg_color)
        self.menu_box_offset = (0, self.side * 4)
        self.menu_box_rect = self.menu_box_image.get_rect(
            center=(
                width//2 + self.menu_box_offset[0],
                height//2 + self.menu_box_offset[1]
            )
        )
        self.menu_image_and_rect = []
        for i in range(len(word)):
            self.menu_image_and_rect.append(
                create_text_surface(
                    (self.side * 7, self.side * 2),
                    self.bt_color,
                    self.font,
                    word[i],
                    self.text_color,
                    center=(
                        width//2 + self.menu_box_offset[0],
                        height//2 + self.side *
                        ((i*2)-3) * 1.5 + self.menu_box_offset[1]
                    )
                )
            )

    def init_profile(self):
        self.profile_box_size = (self.side*9, self.side*(4*2+5))
        self.profile_box_image = create_surface(
            self.profile_box_size, self.bg_color
        )
        self.profile_box_rect = self.profile_box_image.get_rect(
            center=(width//2, height//2)
        )
        self.profile_header_size = (self.side*7, self.side*2)
        self.profile_header_image, self.profile_header_rect = create_text_surface(
            self.profile_header_size, self.bt_color, self.font,
            "Profile", self.text_color,
            center=(
                width//2,
                height//2 - self.side * 6
            )
        )
        self.profile_images = player_images
        for i in range(len(self.profile_images)):
            self.profile_images[i] = pygame.transform.scale(
                self.profile_images[i], (self.side * 4, self.side * 4)
            )
        self.profile_image_len = len(self.profile_images)
        self.profile_n = int(self.data["skin"])-1
        self.profile_image = self.profile_images[self.profile_n]
        self.profile_rect = self.profile_image.get_rect(
            center=(
                width//2,
                height//2 - self.side * 2
            )
        )
        self.profile_text_size = (self.side*2, self.side*1)
        self.profile_texts = []
        for i in range(len(self.profile_images)):
            self.profile_texts.append(
                create_text_surface(
                    self.profile_text_size,
                    self.bt_color,
                    self.font,
                    str(i+1),
                    self.text_color,
                    center=(
                        width//2,
                        height//2 + self.side * 2
                    )
                )
            )
        self.profile_text = self.profile_texts[self.profile_n]

        self.profile_button_size = (self.side*1, self.side*1)
        self.profile_left_button_image = create_surface(
            self.profile_button_size, "green"
        )
        self.profile_left_button_rect = self.profile_left_button_image.get_rect(
            center=(
                width//2 + self.side * 2,
                height//2 + self.side * 2
            )
        )
        self.profile_right_button_image = create_surface(
            self.profile_button_size, "green"
        )
        self.profile_right_button_rect = self.profile_right_button_image.get_rect(
            center=(
                width//2 - self.side * 2,
                height//2 + self.side * 2
            )
        )
        self.profile_input_image = create_surface(
            (self.side*5, self.side*1), self.bt_color
        )
        self.profile_input_rect = self.profile_input_image.get_rect(
            center=(width//2, height//2 + self.side*5)
        )
        self.profile_skin_text_image, self.profile_skin_text_rect = create_text_surface(
            (self.side*5, self.side*1),
            (60, 50, 50),
            self.font,
            "Skin",
            self.text_color,
            center=(
                width//2,
                height//2 + self.side*1
            )
        )
        self.profile_name_text_image, self.profile_name_text_rect = create_text_surface(
            (self.side*5, self.side*1),
            (60, 50, 50),
            self.font,
            "Name",
            self.text_color,
            center=(
                width//2,
                height//2 + self.side*4
            )
        )
        self.mouse_before = False

    def init_setting(self):
        pass

    def profile(self):
        run = True
        name = self.data["name"]
        skin = self.data["skin"]
        active = False
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                        break
                    if active:
                        if event.key == pygame.K_BACKSPACE:
                            name = name[:-1]
                        else:
                            name += event.unicode

            self.screen.fill(background_color)
            mx, my = pygame.mouse.get_pos()
            if self.profile_left_button_rect.collidepoint(mx, my) and pygame.mouse.get_pressed()[0] and not self.mouse_before:
                self.profile_n = (self.profile_n + 1) % self.profile_image_len
                self.profile_image = self.profile_images[self.profile_n]
                self.profile_text = self.profile_texts[self.profile_n]
            if self.profile_right_button_rect.collidepoint(mx, my) and pygame.mouse.get_pressed()[0] and not self.mouse_before:
                self.profile_n = (self.profile_n - 1) % self.profile_image_len
                self.profile_image = self.profile_images[self.profile_n]
                self.profile_text = self.profile_texts[self.profile_n]

            if pygame.mouse.get_pressed()[0] and not self.mouse_before:
                if self.profile_input_rect.collidepoint(mx, my):
                    active = not active
                else:
                    active = False
            text_image = self.font.render(
                name, True, self.text_color
            )
            text_rect = text_image.get_rect(
                center=self.profile_input_rect.center
            )
            # box
            # header
            # image
            # skin text
            # left skin right
            # name text
            # name
            self.screen.blit(self.profile_box_image, self.profile_box_rect)
            self.screen.blit(
                self.profile_header_image,
                self.profile_header_rect
            )
            self.screen.blit(self.profile_image, self.profile_rect)
            self.screen.blit(
                self.profile_skin_text_image,
                self.profile_skin_text_rect
            )
            self.screen.blit(self.profile_text[0], self.profile_text[1])
            self.screen.blit(
                self.profile_left_button_image,
                self.profile_left_button_rect
            )
            self.screen.blit(
                self.profile_right_button_image,
                self.profile_right_button_rect
            )
            self.screen.blit(
                self.profile_name_text_image,
                self.profile_name_text_rect
            )
            self.screen.blit(self.profile_input_image, self.profile_input_rect)
            self.screen.blit(text_image, text_rect)
            self.draw_cursor()
            pygame.display.update()
            self.mouse_before = pygame.mouse.get_pressed()[0]
        self.data["skin"] = skin
        self.data["name"] = name

    def setting(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    run = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    run = False

            self.screen.fill(background_color)
            mx, my = pygame.mouse.get_pos()
            self.draw_cursor()
            pygame.display.update()

    def menu(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                    exit()

            self.screen.fill(background_color)
            mx, my = pygame.mouse.get_pos()
            if self.menu_image_and_rect[0][1].collidepoint((mx, my)):
                if pygame.mouse.get_pressed()[0]:
                    self.running = False
                    break
            if self.menu_image_and_rect[1][1].collidepoint((mx, my)):
                if pygame.mouse.get_pressed()[0]:
                    self.profile()
            if self.menu_image_and_rect[2][1].collidepoint((mx, my)):
                if pygame.mouse.get_pressed()[0]:
                    self.setting()
            if self.menu_image_and_rect[3][1].collidepoint((mx, my)):
                if pygame.mouse.get_pressed()[0]:
                    exit()
            self.screen.blit(self.logo_image, self.logo_rect)
            self.screen.blit(self.menu_box_image, self.menu_box_rect)
            for image, rect in self.menu_image_and_rect:
                self.screen.blit(image, rect)
            self.draw_cursor()
            pygame.display.update()


if __name__ == "__main__":
    run = True
    data = {"skin": 1, "name": ""}
    while run:
        menu = Menu(data)
        exit()
