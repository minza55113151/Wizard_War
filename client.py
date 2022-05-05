import pygame
from settings import *
from circle.circlegroup import CircleGroup
from tile.tilegroup import TileGroup
from layer import Layer
from network import Network
from playergroup import PlayerGroup
from projectile import Projectile
from ui import UIGroup

# done
# right click to walk
# connection timeout socket.settimeout
# camera lock
# camera follow by mouse
# slow speed when cast
# offset mouse target point
# walk point image
# set speed other player from server data

# done?
# interpolation
# exterpolation

# to do
# map
# projectile author [pass author in bullets and pass in projectiles]
# select server

# select elements qwer asdf 8 elements
# ui Ex : hp, mp, exp, level, skill point, skill list
# element : water, heal, shield, ice, thunder, death, stone, fire
# skill : fast walk, revive, reaper, metor shower

# left click shoot
# middle click or space bar use to yourself or in your area
# right click walk

# element iteration like fire + water
# health damage stun slow fire ice falling knockback
# when cast should slow speed and speed rotate face direction

# server validation data

# refactor update_stc, other player slow walk
# refactor camera follow by mouse
# connect everything together


class Game:
    def __init__(self):
        # setup game ------------------------------------------------------------
        pygame.init()
        self.screen = pygame.display.set_mode(
            (width, height),
        )
        pygame.display.set_caption("Client")
        # pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()
        self.running = True
        # setup sprites ----------------------------------------------------------
        self.tile_sprites = TileGroup()
        self.tile_sprites.create_random_tile(2000)
        self.circle_sprites = CircleGroup(pcmc=False)
        self.projectile_sprites = pygame.sprite.Group()
        self.player_sprites = PlayerGroup()
        self.UI_sprites = UIGroup()
        self.all_sprites_group = {
            "tile": self.tile_sprites,
            "circle": self.circle_sprites,
            "projectile": self.projectile_sprites,
            "player": self.player_sprites,
            "UI": self.UI_sprites
        }
        # setup network ---------------------------------------------------------
        self.client_sending_data = {}
        self.client_data = {"player": {}}
        self.network = Network(self.client_sending_data)
        self.id = self.network.id
        # setup player ----------------------------------------------------------
        self.player = self.player_sprites.create_player(
            pos=self.network.pos,
            color="green",
            name="player " + self.id,
            control=True,
            client_sending_data=self.client_sending_data,
            all_sprites_group=self.all_sprites_group
        )
        # setup layer -----------------------------------------------------------
        self.layer = Layer(self.all_sprites_group)

    def update_stc(self):
        # update data from server to client
        other_player_client_data = self.client_data["player"]
        for player_id, other_player in other_player_client_data.items():
            if other_player["player"] == None:
                other_player["player"] = self.player_sprites.create_player(
                    pos=other_player["pos"],
                    color="red",
                    name="player " + player_id,
                    all_sprites_group=self.all_sprites_group
                )
            # other_player["player"].is_shoot = False
            if other_player["event"]["bullets"]:
                # other_player["player"].is_shoot = True
                bullets = other_player["event"]["bullets"]
                for bullet in bullets:
                    face_direction = pygame.math.Vector2(*bullet["direction"])
                    Projectile(
                        bullet["pos"],
                        face_direction,
                        all_sprites_group=self.all_sprites_group
                    )
            if other_player["event"]["target_pos"]:
                other_player["player"].target_pos = other_player["event"]["target_pos"]
            other_player["player"].speed = other_player["speed"]

    def network_update(self):
        # get data from server --------------------------------------------------
        self.network.get_server_data()
        # prepare data from server -----------------------------------------------
        self.server_data = self.network.server_data
        self.network.update_client_data(self.client_data)
        # update data from server to client -------------------------------------
        self.update_stc()
        # set sending data for sending to server --------------------------------
        self.network.set_client_sending_data(self.player)

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
                self.network.disconnect()
                # pygame.quit()
            if event.type == pygame.MOUSEWHEEL:
                self.layer.camera.zoom_scale += event.y * 0.03

    def run(self):
        while self.running:
            # game tick ----------------------------------------------------------
            self.clock.tick(fps)
            # pygame event -------------------------------------------------------
            self.event_handler()
            # client data and server data ----------------------------------------
            self.network_update()
            # render layer -------------------------------------------------------
            self.layer.render()
            # display debug ------------------------------------------------------
            self.display_debug()
            # pygame display update ----------------------------------------------
            pygame.display.update()

    def display_debug(self):
        self.debug_count = [0]
        debugs = [
            f"fps: {self.clock.get_fps():.2f}",
            f"pos: {self.player.rect.centerx},{self.player.rect.centery}",
            f"target_pos: {self.player.target_pos[0]},{self.player.target_pos[1]}",
            f"mouse_pos: {pygame.mouse.get_pos()}",
            f"move_durection: {self.player.move_direction.x:.2f},{self.player.move_direction.y:.2f}",
            f"face_direction: {self.player.face_direction.x:.2f},{self.player.face_direction.y:.2f}",
            f"face_angle: {self.player.face_direction.angle_to(pygame.math.Vector2(1, 0)):.2f}",
            f"players: {len(self.player_sprites.sprites())}",
            f"projectiles: {len(self.projectile_sprites.sprites())}"
        ]
        for text in debugs:
            debug(text, self.debug_count)


game = Game()
game.run()
