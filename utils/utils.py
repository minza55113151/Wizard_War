import pygame
import os


pygame.init()


def create_font(font_size=20, font_name=None):
    font = pygame.font.Font(font_name, font_size)
    return font


def draw_text_to_surface(surface, font, text, text_color="black", bg_color=None, pos=None):
    text = font.render(str(text), True, text_color)
    if pos == None:
        text_rect = text.get_rect(
            center=(surface.get_width()//2, surface.get_height()//2)
        )
    else:
        text_rect = text.get_rect(center=pos)
    if bg_color != None:
        pygame.draw.rect(surface, bg_color, text_rect)
    surface.blit(text, text_rect)


def load_img(path, colorkey=(0, 0, 0), size=None):
    img = pygame.image.load(path).convert()
    if size:
        img = pygame.transform.scale(img, size)
    img.set_colorkey(colorkey)
    return img


def load_ani(path, colorkey=(0, 0, 0), size=None):
    ani = []
    for filename in os.listdir(path):
        img_path = os.path.join(path, filename)
        ani.append(load_img(img_path, colorkey, size))
    return ani


def create_surface(size, color=(0, 0, 0), colorkey=(0, 0, 0)):
    surface = pygame.Surface(size).convert()
    surface.set_colorkey(colorkey)
    if color:
        surface.fill(color)
    return surface


def create_key_img(keys, img_size, bg_color, bd_color, center, r, R, font_size, font_name=None, text_color=(0, 0, 0)):
    key_images = {}
    for key in keys:
        surface = create_surface(img_size)
        pygame.draw.circle(surface, bd_color, center, R)
        pygame.draw.circle(surface, bg_color, center, r)
        draw_text_to_surface(
            surface=surface,
            font=create_font(font_size, font_name),
            text=chr(key).upper(),
            text_color=text_color,
            bg_color=None,
            pos=None,
        )
        key_images[key] = surface
    return key_images


def debug(info, debug_count):
    screen = pygame.display.get_surface()
    font = create_font(20)
    text = font.render(str(info), True, "White")
    rect = text.get_rect(topleft=(0, debug_count[0] * (20//2+2)))
    pygame.draw.rect(screen, "Black", rect)
    screen.blit(text, rect)
    debug_count[0] += 1


lt = 0
t = 0
dt = 0


def get_dt(fps):
    global lt, t, dt
    t = pygame.time.get_ticks()
    dt = (t - lt) * fps / 1000
    lt = t
    return dt
