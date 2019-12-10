import sys
from Replica import Replica
from google.protobuf.internal.encoder import _EncodeVarint
import BFT_pb2
import uuid
from time import sleep, time
import socket


BASE = 60000

class Client:
    def __init__(self, n, rate, batch_size):
        self.n = n
        self.rate = rate
        self.batch_size = batch_size
        self.sockets = []

    def connect_to_replicas(self, start_port):
        for i in range(1, self.n+1):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((socket.gethostname(), start_port + i))
            self.sockets.append(s)

    def send_msg(self, s, prototype):
        prototype.timestamp = time()
        if prototype is not None:
            msg = None
            try:
                msg = prototype.SerializeToString()
            except:
                print("ERROR SERIALIZING TO STRING")
            if msg is None:
                raise Exception
            _EncodeVarint(s.sendall, len(msg), None)
            try:
                s.sendall(msg)
            except:
                print("SOCKET DISCONNECTED EXCEPTION")

    def run(self):
        self.connect_to_replicas(60000)
        while True:
            uid = str(uuid.uuid4())
            wrapper = BFT_pb2.Wrapper()
            for i in range(0, self.batch_size):
                wrapper.command.commands.append(uid)
            wrapper.id = uid
            for sock in self.sockets:
                self.send_msg(sock, wrapper)
            sleep(1/self.rate)



def main():
    args = sys.argv[1:]
    n = int(args[0])
    rate = int(args[1])
    batch_size = int(args[2])
    print("Running Client...")
    try:
        client = Client(n, rate, batch_size)

    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    main()