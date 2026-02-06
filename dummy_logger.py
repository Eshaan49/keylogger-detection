import time
import socket

while True:
    try:
        s = socket.socket()
        s.connect(("example.com", 80))
        s.close()
    except:
        pass

    # keep CPU active
    for _ in range(1000000):
        pass

    time.sleep(1)
