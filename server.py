import socket
from _thread import start_new_thread
import pickle
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
    server_data["player"][player_ID] = {
        "pos": start_pos,
        "id": player_ID,
        "speed": 0,
        "event": {
            "bullets": [],
            "target_pos": []
        }
    }
    client_data = server_data["player"][player_ID]
    print(f"[Sending][initial] p{player_ID}: {client_data}")
    send_data(con, client_data)

    while True:
        try:
            # recieve data from client then update data to server_data
            client_data = recv_data(con)
            print(f"[Recieve] p{player_ID}: {client_data}")
            server_data["player"][player_ID]["pos"] = client_data["pos"]
            server_data["player"][player_ID]["speed"] = client_data["speed"]
            server_data["player"][player_ID]["event"] = client_data["event"]
            print(f"[Sending] p{player_ID}: {server_data}")
            send_data(con, server_data)

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
