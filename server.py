import socket
from _thread import start_new_thread
import pickle
import time
# setup server data and environment
ip = "25.31.231.0"
port = 3000
server_data = {"player": {}}
start_pos = [0, 0]

# initial socket
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind((ip, port))
soc.listen(10)
print("Start!")


def get_player_ID():  # get player ID
    i = 1
    while True:
        if str(i) not in server_data["player"]:
            return str(i)
        i += 1


def recv_data(con):  # recieve data from client
    return pickle.loads(con.recv(128000))


def send_data(con, send):  # send data to client
    con.send(pickle.dumps(send))


def threaded_client(con):  # threaded client function to handle each client connection

    # initial player data in server then send to client
    player_ID = get_player_ID()
    first_sending_data = {
        "id": player_ID,
        "skin": 1,
        "name": "player " + player_ID,
        "pos": start_pos,
        "target_pos": start_pos,
        "hp": 0,
        "mp": 0,
        "speed": 0,
        "angle": 0,
        "event": {
            "bullets": [],
        }
    }
    print(f"[Sending][initial] p{player_ID}: {first_sending_data}")
    send_data(con, first_sending_data)

    client_data = recv_data(con)
    print(f"[Recieve][initial] p{player_ID}: {client_data}")
    server_data["player"][player_ID] = client_data
    print(f"[Sending][start] p{player_ID}: {server_data}")
    send_data(con, server_data)
    t1 = time.time()
    while True:
        try:

            # recieve data from client then update data to server_data
            client_data = recv_data(con)
            t2 = time.time()
            print(f"p{player_ID} ping {(t2-t1)*1000:.0f} ms")
            # print(f"[Recieve] p{player_ID}: {client_data}")
            k = 0
            for i in range(100000):
                k += i**2
            server_data["player"][player_ID]["skin"] = client_data["skin"]
            server_data["player"][player_ID]["name"] = client_data["name"]
            server_data["player"][player_ID]["pos"] = client_data["pos"]
            server_data["player"][player_ID]["target_pos"] = client_data["target_pos"]
            server_data["player"][player_ID]["hp"] = client_data["hp"]
            server_data["player"][player_ID]["mp"] = client_data["mp"]
            server_data["player"][player_ID]["speed"] = client_data["speed"]
            server_data["player"][player_ID]["angle"] = client_data["angle"]
            server_data["player"][player_ID]["event"] = client_data["event"]
            # print(f"[Sending] p{player_ID}: {server_data}")
            send_data(con, server_data)
            t1 = time.time()

        except Exception as e:
            print(f"{player_ID} Lost connection [{e}]")
            break

    # delete player data in server when lost connection
    del server_data["player"][player_ID]

    con.close()


while True:
    # wait for client connection then start new thread
    con, adr = soc.accept()
    print("Connected to: ", adr)
    start_new_thread(threaded_client, (con,))
