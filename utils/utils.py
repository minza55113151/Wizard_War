import pygame
import os
import json


pygame.init()
pygame.font.init()


def create_font(font_size=20, font_name=None, **kwargs):
    if font_name:
        font = pygame.font.SysFont(font_name, font_size, **kwargs)
    else:
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
    # print(f"load: {path}")
    img = pygame.image.load(path).convert()
    if size:
        img = pygame.transform.scale(img, size)
    img.set_colorkey(colorkey)
    return img


def load_ani(path, colorkey=(0, 0, 0), size=None):
    ani = []
    for filename in sorted(os.listdir(path), key=lambda x: int(x[x.find("(")+1:x.find(")")])):
        img_path = os.path.join(path, filename)
        ani.append(load_img(img_path, colorkey, size))
    return ani


def create_360(surface):
    images = []
    for i in range(360):
        images.append(pygame.transform.rotate(surface, i))
    return images


def create_360_surface(size, color=(0, 0, 0), colorkey=(0, 0, 0)):
    surface = create_surface(size, color, colorkey)
    return create_360(surface)


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


def create_text_surface(size, bg_color, font, text, text_color, **kwargs):
    surface = create_surface(size, bg_color)
    draw_text_to_surface(surface, font, text, text_color)
    rect = surface.get_rect(**kwargs)
    return surface, rect


def read_json(path):
    with open(path, "r") as f:
        return json.load(f)


def write_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f)


def read_client():
    try:
        data = read_json("client.json")
    except FileNotFoundError:
        data = {"skin": 1, "name": "Wizard"}
    return data


def write_client(data):
    write_json("client.json", data)
