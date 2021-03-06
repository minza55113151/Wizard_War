import pygame
from utils.utils import *

# region game settings
draw_hitbox = False
draw_plan_camera_mouse_control = False
# endregion game settings
# region screen settings
fps = 60
# width = 640
# height = 480
# width = 1280
# height = 720
width = 1600
height = 900
# width = 1920
# height = 1080
# make it can load image
pygame.display.set_mode((width, height))
# endregion screen settings
# region other settings
small_cir_rad = width//4
big_cir_rad = width//2
background_color = (100, 100, 200)
gb_colorkey = (1, 1, 1)
# endregion other settings
# region cursor settings
cursor_image_path = "assets/mouse/cursor/cursor.png"
cursor_image = load_img(cursor_image_path)
# endregion cursor settings
# region player settings
player_image_size = (75, 75)
player_images_path = "assets/player/"
player_images = load_ani(player_images_path)
player_images_set = []
for i in range(len(player_images)):
    player_images_set.append(create_360(player_images[i]))
player_image_path_green = "assets/green.png"
player_image_green = load_img(
    player_image_path_green, gb_colorkey, player_image_size
)
player_image_path_red = "assets/red.png"
player_image_red = load_img(
    player_image_path_red, gb_colorkey, player_image_size
)

player_hitbox_size = (50, 50)
player_hitbox_size_dif = (
    player_hitbox_size[0] - player_image_size[0],
    player_hitbox_size[1] - player_image_size[1]
)
player_hitbox_image = create_surface(player_hitbox_size, (0, 255, 0))

player_move_target_size = (25, 15)
player_move_target_image_path = "assets/mouse/pos"
player_move_target_images = load_ani(
    player_move_target_image_path, (0, 0, 0), player_move_target_size
)
player_move_target_animation_speed = 0.25

player_fast_speed = 8
player_normal_speed = 5
player_slow_speed = 3
player_rotation_speed = 5
player_max_hp = 100
player_max_mp = 100

player_hp_border_offset = (2, 2)
player_hp_image_size = (player_image_size[0]-10, 5)
player_hp_border_image_size = (
    player_hp_image_size[0] + player_hp_border_offset[0] * 2,
    player_hp_image_size[1] + player_hp_border_offset[1] * 2
)
# endregion player settings
# region projectile settings
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
projectile_image_path = "assets/black.png"
projectile_image_size = (5, 5)
projectile_image = load_img(projectile_image_path, gb_colorkey)
projectile_image = pygame.transform.scale(
    projectile_image, projectile_image_size
)
projectile_images = create_360(projectile_image)
projectile_speed = 10
projectile_life_time = 5
projectile_max_health = fps * projectile_life_time

projectile_spread_image_size = (15, 15)
projectile_spread_speed = 15
projectile_spread_life_time = 0.25
projectile_spread_max_health = projectile_spread_life_time * fps
projectile_laser_image_size = (60, 15)
projectile_laser_speed = 45
projectile_laser_life_time = 0.5
projectile_laser_max_health = projectile_laser_life_time * fps
projectile_projectile_image_size = (50, 50)
projectile_projectile_speed = 50
projectile_projectile_life_time = 5
projectile_projectile_max_health = projectile_projectile_life_time * fps
projectile_shield_image_size = (5, 100)
projectile_shield_speed = 0
projectile_shield_life_time = 5
projectile_shield_max_health = projectile_shield_life_time * fps
projectile_shield_offset = 50

projectile_water_images = create_360_surface(
    projectile_spread_image_size,
    "cyan"
)
projectile_heal_images = create_360_surface(
    projectile_laser_image_size,
    "green"
)

projectile_shield_images = create_360_surface(
    projectile_shield_image_size,
    "yellow"
)

projectile_ice_images = create_360_surface(
    projectile_spread_image_size,
    "white"
)

projectile_thunder_images = create_360_surface(
    projectile_spread_image_size,
    "purple"
)

projectile_death_images = create_360_surface(
    projectile_laser_image_size,
    "red"
)
projectile_stone_images = create_360_surface(
    projectile_projectile_image_size,
    "brown"
)
projectile_fire_images = create_360_surface(
    projectile_spread_image_size,
    "orange"
)
projectile_steam_images = create_360_surface(
    projectile_spread_image_size,
    "grey"
)
projectile_data = {
    "water": {
        "damage": 0.25,
        "knockback": 0.25,
    },
    "heal": {
        "damage": -0.25
    },
    "shield": {
        "damage": 0,
    },
    "ice": {
        "damage": 0.25,
        "slow": 0.25
    },
    "thunder": {
        "damage": 0.25,
        "stun": 0.25
    },
    "death": {
        "damage": 0.5,
    },
    "stone": {
        "damage": 0.75,
    },
    "fire": {
        "damage": 0.25,
        "burn": 0.25
    }
}
projectile_max_cooldown = 3 * fps
# endregion projectile settings
# region tile settings
tile_image_path = ""
tile_image = ""
tile_image_size = (50, 50)
# endregion tile settings
# UI settings
# region UI element settings
UI_element_order = [
    "water", "heal", "shield", "ice",
    "thunder", "death", "stone", "fire"
]
UI_element_keys = [
    pygame.K_q,
    pygame.K_w,
    pygame.K_e,
    pygame.K_r,
    pygame.K_a,
    pygame.K_s,
    pygame.K_d,
    pygame.K_f
]


UI_element_images = None
UI_element_image_size = (50, 50)
UI_element_image_radius = UI_element_image_size[0]//2
UI_element_image_scaled_size = (
    int(UI_element_image_size[0]*1.2),
    int(UI_element_image_size[1]*1.2)
)

UI_element_key_bg_color = (255, 255, 255)
UI_element_key_bd_color = (1, 1, 1)
UI_element_key_image_size = (20, 20)
UI_element_key_image_center = (
    UI_element_key_image_size[0]//2,
    UI_element_key_image_size[1]//2
)
UI_element_key_image_offset = (-2, -2)
UI_element_key_image_r = 8
UI_element_key_image_R = 10
UI_element_key_image_font_size = 20
UI_element_key_image_font_name = None
UI_element_key_image_text_color = (1, 1, 1)
UI_element_key_images = create_key_img(
    keys=UI_element_keys,
    img_size=UI_element_key_image_size,
    bg_color=UI_element_key_bg_color,
    bd_color=UI_element_key_bd_color,
    center=UI_element_key_image_center,
    r=UI_element_key_image_r,
    R=UI_element_key_image_R,
    font_size=UI_element_key_image_font_size,
    font_name=UI_element_key_image_font_name,
    text_color=UI_element_key_image_text_color
)
# 1.water(q)
UI_water_image_path = "assets/UI/element/water/"
UI_water_images = load_ani(
    UI_water_image_path, (0, 0, 0), UI_element_image_size
)
UI_water_image_1 = UI_water_images[0]
UI_water_image_2 = UI_water_images[1]
UI_water_image_3 = pygame.transform.scale(
    UI_water_image_2, UI_element_image_scaled_size
)
# 2.heal(w)
UI_heal_image_path = "assets/UI/element/heal/"
UI_heal_images = load_ani(
    UI_heal_image_path, (0, 0, 0), UI_element_image_size
)
UI_heal_image_1 = UI_heal_images[0]
UI_heal_image_2 = UI_heal_images[1]
UI_heal_image_3 = pygame.transform.scale(
    UI_heal_image_2, UI_element_image_scaled_size
)
# 3.shield(e)
UI_shield_image_path = "assets/UI/element/shield/"
UI_shield_images = load_ani(
    UI_shield_image_path, (0, 0, 0), UI_element_image_size
)
UI_shield_image_1 = UI_shield_images[0]
UI_shield_image_2 = UI_shield_images[1]
UI_shield_image_3 = pygame.transform.scale(
    UI_shield_image_2, UI_element_image_scaled_size
)
# 4.ice(r)
UI_ice_image_path = "assets/UI/element/ice/"
UI_ice_images = load_ani(
    UI_ice_image_path, (0, 0, 0), UI_element_image_size
)
UI_ice_image_1 = UI_ice_images[0]
UI_ice_image_2 = UI_ice_images[1]
UI_ice_image_3 = pygame.transform.scale(
    UI_ice_image_2, UI_element_image_scaled_size
)
# 5.thunder(a)
UI_thunder_image_path = "assets/UI/element/thunder/"
UI_thunder_images = load_ani(
    UI_thunder_image_path, (0, 0, 0), UI_element_image_size
)
UI_thunder_image_1 = UI_thunder_images[0]
UI_thunder_image_2 = UI_thunder_images[1]
UI_thunder_image_3 = pygame.transform.scale(
    UI_thunder_image_2, UI_element_image_scaled_size
)
# 6.death(s)
UI_death_image_path = "assets/UI/element/death/"
UI_death_images = load_ani(
    UI_death_image_path, (0, 0, 0), UI_element_image_size
)
UI_death_image_1 = UI_death_images[0]
UI_death_image_2 = UI_death_images[1]
UI_death_image_3 = pygame.transform.scale(
    UI_death_image_2, UI_element_image_scaled_size
)
# 7.stone(d)
UI_stone_image_path = "assets/UI/element/stone/"
UI_stone_images = load_ani(
    UI_stone_image_path, (0, 0, 0), UI_element_image_size
)
UI_stone_image_1 = UI_stone_images[0]
UI_stone_image_2 = UI_stone_images[1]
UI_stone_image_3 = pygame.transform.scale(
    UI_stone_image_2, UI_element_image_scaled_size
)
# 8.fire(f)
UI_fire_image_path = "assets/UI/element/fire/"
UI_fire_images = load_ani(
    UI_fire_image_path, (0, 0, 0), UI_element_image_size
)
UI_fire_image_1 = UI_fire_images[0]
UI_fire_image_2 = UI_fire_images[1]
UI_fire_image_3 = pygame.transform.scale(
    UI_fire_image_2, UI_element_image_scaled_size
)

UI_element_image_small_scaled_size = (
    player_image_size[0]//3, player_image_size[1]//3
)
UI_scale_water_image = pygame.transform.scale(
    UI_water_image_1, UI_element_image_small_scaled_size
)
UI_scale_heal_image = pygame.transform.scale(
    UI_heal_image_1, UI_element_image_small_scaled_size
)
UI_scale_shield_image = pygame.transform.scale(
    UI_shield_image_1, UI_element_image_small_scaled_size
)
UI_scale_ice_image = pygame.transform.scale(
    UI_ice_image_1, UI_element_image_small_scaled_size
)
UI_scale_thunder_image = pygame.transform.scale(
    UI_thunder_image_1, UI_element_image_small_scaled_size
)
UI_scale_death_image = pygame.transform.scale(
    UI_death_image_1, UI_element_image_small_scaled_size
)
UI_scale_stone_image = pygame.transform.scale(
    UI_stone_image_1, UI_element_image_small_scaled_size
)
UI_scale_fire_image = pygame.transform.scale(
    UI_fire_image_1, UI_element_image_small_scaled_size
)
# endregion UI element settings
# region UISkill settings
UI_skill_order = [
    "running", "revive", "reaper", "meteor"
]
UI_skill_keys = [
    pygame.K_1,
    pygame.K_2,
    pygame.K_3,
    pygame.K_4,
]
UI_skill_image_path = "assets/UI/skill/"
UI_skill_image_size = (75, 75)
UI_element_image_scaled_size = (
    int(UI_skill_image_size[0]*1.2),
    int(UI_skill_image_size[1]*1.2)
)
UI_skill_key_bg_color = (255, 255, 255)
UI_skill_key_bd_color = (1, 1, 1)
UI_skill_key_image_size = (20, 20)
UI_skill_key_image_center = (
    UI_skill_key_image_size[0]//2,
    UI_skill_key_image_size[1]//2
)
UI_skill_key_image_r = 8
UI_skill_key_image_R = 10
UI_skill_key_image_font_size = 20
UI_skill_key_image_font_name = None
UI_skill_key_image_text_color = (1, 1, 1)
UI_skill_key_images = create_key_img(
    keys=UI_skill_keys,
    img_size=UI_skill_key_image_size,
    bg_color=UI_skill_key_bg_color,
    bd_color=UI_skill_key_bd_color,
    center=UI_skill_key_image_center,
    r=UI_skill_key_image_r,
    R=UI_skill_key_image_R,
    font_size=UI_skill_key_image_font_size,
    font_name=UI_skill_key_image_font_name,
    text_color=UI_skill_key_image_text_color
)
# 1.running
UI_running_image_path = "assets/UI/skill/running/"
UI_running_images = load_ani(UI_running_image_path, size=UI_skill_image_size)
UI_running_images.append(pygame.transform.scale(
    UI_running_images[1], UI_element_image_scaled_size
))
# 2.revive
UI_revive_image_path = "assets/UI/skill/revive/"
UI_revive_images = load_ani(UI_revive_image_path, size=UI_skill_image_size)
UI_revive_images.append(pygame.transform.scale(
    UI_revive_images[1], UI_element_image_scaled_size
))
# 3.reaper
UI_reaper_image_path = "assets/UI/skill/reaper/"
UI_reaper_images = load_ani(UI_reaper_image_path, size=UI_skill_image_size)
UI_reaper_images.append(pygame.transform.scale(
    UI_reaper_images[1], UI_element_image_scaled_size
))
# 4.meteor
UI_meteor_image_path = "assets/UI/skill/meteor/"
UI_meteor_images = load_ani(UI_meteor_image_path, size=UI_skill_image_size)
UI_meteor_images.append(pygame.transform.scale(
    UI_meteor_images[1], UI_element_image_scaled_size
))
# endregion UISkill settings
# region UIBorder settings
# 0.
UI_border_color = (37, 25, 22)
UI_border0_image_size = (width, 50)
UI_border0_image = create_surface(UI_border0_image_size, color=UI_border_color)
UI_border0_image_bottomleft = (0, height)

UI_border1_image_size = (width//3 - 20, 130)
UI_border1_image = create_surface(
    UI_border1_image_size, color=UI_border_color
)
w = width//2 - 10 * (UI_element_image_size[0] + 1)//2 - 5
UI_border1_image_bottomleft = (w, height)
# endregion UIBorder settings
# region UIMana settings
UI_mp_border_offset = (2, 2)
UI_mp_image_size = (
    UI_skill_image_size[0]*len(UI_skill_order),
    UI_skill_image_size[1]//3
)
UI_mp_border_image_size = (
    UI_mp_image_size[0] + UI_mp_border_offset[0]*2,
    UI_mp_image_size[1] + UI_mp_border_offset[1]*2
)


UI_mp_border_color = (1, 1, 1)

# endregion UIMana settings
