import socket
import pickle
from threading import Thread
import time

ips = {
    "Minzung": "25.31.231.0",
    "JiMeow": "25.34.159.172",
    "GolfGrab": "25.35.236.244"
}


class Network:
    def __init__(self, client_sending_data):
        # setup server data and environment ------------------------------------
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(1)
        self.port = 3000
        self.ips = ips
        self.data = self.connect()
        self.id = str(self.data["id"])
        self.pos = self.data["pos"]
        # setup data for client and server --------------------------------------
        self.server_data = {"player": {}}
        self.client_sending_data = client_sending_data
        self.set_client_sending_data()
        # setup thread ----------------------------------------------------------
        self.thread = Thread(target=self.get_server_data)

        self.t1 = time.time()
        self.t2 = time.time()

        # self.missing_frame = 0
        # self.get_server_data_time = 0

    def disconnect(self):
        self.client.close()

    def connect(self):
        for name, ip in self.ips.items():
            try:
                self.client.connect((ip, self.port))
                return pickle.loads(self.client.recv(128000))
            except:
                print(f"Connection to {name} failed")

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(128000))
        except socket.error as e:
            print(e)

    def get_server_data(self):
        if not self.thread.is_alive():
            self.thread = Thread(target=self._get_server_data)
            self.thread.start()
            self.t2 = time.time()
            print(f"ping {(self.t2 - self.t1)*1000:.0f} ms")
            self.t1 = self.t2

        #     print(self.missing_frame)
        #     self.get_server_data_time = 0
        #     self.missing_frame = 0
        # self.get_server_data_time += self.dt
        # self.missing_frame += 1

    def _get_server_data(self):
        self.server_data = self.send(self.client_sending_data)

    def set_client_sending_data(self, player=None):
        self.client_sending_data["id"] = self.id
        if player:
            self.client_sending_data["pos"] = [*player.rect.center]
            self.client_sending_data["target_pos"] = [*player.rect.center]
        else:
            self.client_sending_data["pos"] = [*self.pos]
            self.client_sending_data["target_pos"] = [*self.pos]
        self.client_sending_data["hp"] = 0
        self.client_sending_data["mp"] = 0
        self.client_sending_data["speed"] = 0
        self.client_sending_data["angle"] = 0
        self.client_sending_data["event"] = {
            "bullets": []
        }

    def valid_player_client_data(self, client_data):
        for player_id, player in list(client_data["player"].items()):
            if player_id not in self.server_data["player"]:
                player["player"].kill()
                del client_data["player"][player_id]

    def update_client_data(self, client_data):
        self.valid_player_client_data(client_data)
        player_client_data = client_data["player"]
        for player_id, player in self.server_data["player"].items():
            if player_id == self.id:
                continue
            # update data
            if player_id in player_client_data:
                player_client_data[player_id]["id"] = player["id"]
                player_client_data[player_id]["skin"] = player["skin"]
                player_client_data[player_id]["name"] = player["name"]
                player_client_data[player_id]["pos"] = player["pos"]
                player_client_data[player_id]["target_pos"] = player["target_pos"]
                player_client_data[player_id]["hp"] = player["hp"]
                player_client_data[player_id]["mp"] = player["mp"]
                player_client_data[player_id]["speed"] = player["speed"]
                player_client_data[player_id]["angle"] = player["angle"]
                player_client_data[player_id]["event"] = player["event"]
            # create new player
            else:
                player_client_data[player_id] = {
                    "player": None,
                    "id": player["id"],
                    "skin": player["skin"],
                    "name": player["name"],
                    "pos": player["pos"],
                    "target_pos": player["target_pos"],
                    "hp": player["hp"],
                    "mp": player["mp"],
                    "speed": player["speed"],
                    "angle": player["angle"],
                    "event": player["event"]
                }

# 7 point to chage data structure
# 1.set_client_sending_data
# 2.update_client_data
# 3.update_client_data
# 4.update_stc
# 5.server
# 6.server
# 7.interact point
