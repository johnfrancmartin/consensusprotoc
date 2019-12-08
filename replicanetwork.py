import sys
import time
import socket
import select
import threading

N = 5
ID = int(sys.argv[1])
Base = 60000
Host = "127.0.0.1"
Port = 60000+ID

epoll = select.epoll()
lock = threading.Lock()

IDs = {}  # fileno2ID
filenos = {}  # ID2fileno
sockets = {}


class Thread (threading.Thread):

    def run(self):
        while True:
            time.sleep(1)
            lock.acquire()
            for i in range(0, N):
                if i == ID:
                    continue
                fileno = filenos[i]
                sockets[fileno].sendall(("Hi %d, I am %d" % (i, ID)).encode())
            lock.release()


for i in range(0, ID):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((Host, Base+i))
    s.setblocking(0)
    epoll.register(s.fileno(), select.EPOLLIN)
    sockets[s.fileno()] = s
    IDs[s.fileno()] = i
    filenos[i] = s.fileno()
    print(ID, "Connect to", i)


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((Host, Port))
serversocket.listen(N)

for i in range(ID+1, N):
    s, addr = serversocket.accept()
    s.setblocking(0)
    epoll.register(s.fileno(), select.EPOLLIN)
    sockets[s.fileno()] = s
    IDs[s.fileno()] = i
    filenos[i] = s.fileno()
    print(ID, "Accept", i)

print(ID, "Finish the network setup")

subThread = Thread()
subThread.start()

count = 0
while True:
    events = epoll.poll(1)
    for fileno, event in events:
        if event & select.EPOLLIN:
            message = sockets[fileno].recv(1024)
            print("%d received message from %d. Message: %s" %
                  (ID, IDs[fileno], message.decode()))
            count += 1
        elif event & select.EPOLLOUT:
            print("EOLLOUT!")
        elif event & select.EPOLLHUP:
            print("EPOLLHUP!")
            epoll.unregister(fileno)
            sockets[fileno].connect
    if count >= N-1:
        break

subThread.join()
