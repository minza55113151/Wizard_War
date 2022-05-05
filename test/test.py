import threading
from time import sleep


def test():
    raise Exception("test")
    sleep(1)


thread = threading.Thread(target=test)

# sleep(2)
