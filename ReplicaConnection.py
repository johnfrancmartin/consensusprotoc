import socket
from BFT_pb2 import Wrapper
import traceback
from time import sleep, time
from threading import Thread, Lock
import atexit
from MessageType import Block, Blame, Proposal, Vote, Command
import uuid
import select
from google.protobuf.internal.encoder import _EncodeVarint
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.timestamp_pb2 import Timestamp

BASE = 60000
HOST = "127.0.0.1"


class ReplicaConnection:
    def __init__(self, n, replica):
        self.print = replica.print
        self.n = n
        self.start = time()
        self.replica = replica
        self.stop = False
        self.sockets_by_id = {}
        port = 2000+replica.id
        print(port)
        self.local_sock = self.listen_socket_init(socket.gethostname(), 2000+replica.id)
        self.messages = []
        self.received = []
        atexit.register(self.exit)

        # EPOLL
        self.local_port = 60000+self.replica.id
        self.epoll = select.epoll()
        self.lock = Lock()

        self.IDs = {}  # fileno2ID
        self.filenos = {}  # ID2fileno
        self.sockets = {}
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind((socket.gethostname(), self.local_port))
        self.serversocket.listen(self.n)

        self.recv_times = []
        self.send_times = []
        self.process_times = []
        self.transfer_times = []

    def connect_to_lessers(self):
        connections = {}
        print("CONNECTING TO LESSERS", flush=True)
        if self.replica.id == 1:
            return
        while len(connections) < self.replica.id - 1 and not self.stop:
            for i in range(1, self.replica.id):
                if i in connections:
                    continue
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((socket.gethostname(), BASE + i))
                    s.setblocking(0)
                    self.epoll.register(s.fileno(), select.EPOLLIN)
                    self.sockets[s.fileno()] = s
                    self.IDs[s.fileno()] = i
                    self.filenos[i] = s.fileno()
                    print(self.replica.id, "CONNECTED TO", i, flush=True)
                    connections[i] = True
                except:
                    print(self.replica.id, "FAILED TO CONNECT TO LESSER")

    def accept_from_greaters(self):
        connections = {}
        print("ACCEPTING FROM GREATERS", flush=True)
        while len(connections) < self.n - self.replica.id and not self.stop:
            for i in range(self.replica.id + 1, self.n+1):
                try:
                    if i in connections:
                        continue
                    s, addr = self.serversocket.accept()
                    s.setblocking(0)
                    self.epoll.register(s.fileno(), select.EPOLLIN)
                    self.sockets[s.fileno()] = s
                    self.IDs[s.fileno()] = i
                    self.filenos[i] = s.fileno()
                    print(len(connections), "TOTAL CONNECTIONS FOR", self.replica.id, flush=True)
                    print(self.replica.id, "ACCEPTED CONNECTION FROM", i, flush=True)
                    connections[i] = True
                except:
                    print(self.replica.id, "FAILED TO ACCEPT GREATER")

    def accept_from_client(self):
        print("ACCEPTING FROM CLIENT", flush=True)
        i = 0
        connected = False
        while not connected and not self.stop:
            try:
                s, addr = self.serversocket.accept()
                s.setblocking(0)
                self.epoll.register(s.fileno(), select.EPOLLIN)
                self.sockets[s.fileno()] = s
                self.IDs[s.fileno()] = i
                self.filenos[i] = s.fileno()
                print(self.replica.id, "ACCEPTED CONNECTION FROM CLIENT", flush=True)
                connected = True
            except:
                print(self.replica.id, "FAILED TO CONNECT TO CLIENT")

    def epoll_listen(self):
        while not self.stop:
            events = self.epoll.poll(1)
            for fileno, event in events:
                if event & select.EPOLLIN:
                    sock = self.sockets[fileno]
                    wrapper = Wrapper()
                    start = time()
                    msg = self.recv_msg(sock, wrapper)
                    if msg is None:
                        continue
                    transfer_time = time() - msg.timestamp
                    self.transfer_times.append(transfer_time)
                    recv_time = time() - start
                    self.recv_times.append(recv_time)
                    # print(self.replica.id, "RECEIVED MESSAGE", msg.id, flush=True)
                    python_msg = self.get_python_message(msg)
                    start = time()
                    self.replica.receive_msg(python_msg, msg.id)
                    process_time = time() - start
                    self.process_times.append(process_time)
                    # self.received.append(python_msg)
                    # message = self.sockets[fileno].recv(1024)
                elif event & select.EPOLLOUT:
                    if self.print:
                        print("EPOLLOUT!")
                elif event & select.EPOLLHUP:
                    if self.print:
                        print("EPOLLHUP!")
                    self.epoll.unregister(fileno)
                    self.sockets[fileno].connect()

    def epoll_send(self):
        while not self.stop:
            if len(self.messages) == 0:
                # print("NO MESSAGES TO SEND", flush=True)
                # sleep(0.01)
                continue
            (replica_id, message) = self.messages.pop(0)
            try:
                fileno = self.filenos[replica_id]
                sock = self.sockets[fileno]
                # print(self.replica.id, "SENT MSG", message.id, flush=True)
                start = time()
                self.send_msg(sock, message)
                recv_time = time() - start
                self.send_times.append(recv_time)
            except Exception as e:
                self.messages.append((replica_id, message))
                # print("FAILED TO SEND", flush=True)
                pass

    def exit(self):
        self.local_sock.close()
        for replica_id, sock in self.sockets_by_id.items():
            sock.close()
        for f, sock in self.sockets.items():
            sock.close()
        self.stop = True
        print("EXITING", self.replica.id)
        total_cmts = len(self.replica.committed)
        print("COMMITTED TOTAL", total_cmts, "BLOCKS")
        duration = time() - self.start
        print("IN", duration, "seconds")
        if total_cmts > 0:
            avg_cmt = duration/total_cmts
            print("AVG CMT TIME", avg_cmt)
        per_sec = 1/avg_cmt
        print("CMT PER SEC", per_sec)
        print("OPS PER SEC", self.replica.batch_size * per_sec)
        if len(self.replica.command_commit_times) > 0:
            print("COMMAND LATENCY", sum(self.replica.command_commit_times)/len(self.replica.command_commit_times))
        if len(self.recv_times) > 0:
            print("AVERAGE RECEIVE TIME:", sum(self.recv_times)/len(self.recv_times))
        if len(self.process_times) > 0:
            print("AVERAGE PROCESSING TIME:", sum(self.process_times) / len(self.process_times))
        if len(self.send_times) > 0:
            print("AVERAGE SEND TIME:", sum(self.send_times) / len(self.send_times))
        if len(self.transfer_times) > 0:
            print("AVERAGE TRANSFER TIME:", sum(self.transfer_times) / len(self.transfer_times))


    def broadcast(self, message):
        while len(self.sockets) < self.n/2:
            continue
        message.id = str(uuid.uuid4())
        if self.print:
            print("BROADCAST", message.id, flush=True)
        for i in range(1, self.n+1):
            if i != self.replica.id:
                self.messages.append((i, message))


    def run(self):
        self.connect_to_lessers()
        self.accept_from_greaters()
        self.accept_from_client()
        print("INITIALIZED NETWORK FOR", self.replica.id, flush=True)
        self.start = time()
        listen_t = Thread(target=self.epoll_listen, args=())
        listen_t.start()
        # execute_t = Thread(target=self.execute, args=())
        # execute_t.start()
        self.replica.network_initialized()
        self.epoll_send()
        listen_t.join()
        # execute_t.join()

        # connect_t = Thread(target=self.connect_to_replicas, args=())
        # connect_t.start()
        #
        # accept_t = Thread(target=self.accept_replica_sockets, args=())
        # accept_t.start()
        #
        # sleep(1)
        # listen_t = Thread(target=self.listen, args=())
        # listen_t.start()
        #
        # send_t = Thread(target=self.send, args=())
        # send_t.start()
        #
        # execute_t = Thread(target=self.execute, args=())
        # execute_t.start()
        #
        # connect_t.join()
        # accept_t.join()
        # listen_t.join()
        # send_t.join()
        # execute_t.join()

    def send(self):
        while not self.stop:
            if len(self.messages) == 0:
                continue
            (replica_id, message) = self.messages.pop(0)
            try:
                sock = self.sockets_by_id[replica_id]
                if self.print:
                    print(self.replica.id, "SENT MSG", message.id, flush=True)
                self.send_msg(sock, message)
            except Exception as e:
                self.messages.append((replica_id, message))
                if self.print:
                    print("FAILED TO SEND", flush=True)

    def execute(self):
        while not self.stop:
            if len(self.received) == 0:
                continue
            msg = self.received.pop(0)
            self.replica.receive_msg(msg)

    def listen(self):
        while len(self.sockets_by_id) == 0:
            sleep(1)
        replica_id = self.get_next_replica_id(0)
        while not self.stop:
            if len(self.sockets_by_id) == 0:
                sleep(0.5)
            sock = self.sockets_by_id[replica_id]
            try:
                # bft_proto.BlameMSG()
                # bft_proto.ProposalMSG()
                # bft_proto.VoteMSG()
                # msg = recvMsg(client_socket, bft_proto.BlameMSG())
                wrapper = Wrapper()
                msg = self.recv_msg(sock, wrapper)
                if msg is None:
                    continue
                print(self.replica.id, "RECEIVED MESSAGE", msg.id)
                python_msg = self.get_python_message(msg)
                self.received.append(python_msg)
            except IndexError as e:
                print("INDEX ERROR")
                raise e
            except Exception as e:
                print("ERROR: Listen for Replicas Thread.", e)
                traceback.print_tb(e.__traceback__)
                pass
            replica_id = self.get_next_replica_id(replica_id)

    def listen_socket_init(self, host, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((host, port))
            sock.listen(10)
            print("Listen Socket Initialized at:", host, port)
            return sock
        except Exception as e:
            print("Error initializing listen sock", e)


    def get_next_replica_id(self, current):
        new = current + 1
        while new == self.replica.id or new > self.n or new not in self.sockets_by_id:
            new += 1
            if new > self.n-1:
                new = 1
        return new

    def get_python_message(self, message):
        if message.HasField('proposal'):
            proposal = Proposal.get_from_proto(message.proposal)
            return proposal
        elif message.HasField('vote'):
            return Vote.get_from_proto(message.vote)
        elif message.HasField('blame'):
            blame_proto = message.blame
            raise NotImplementedError
        else:
            command = Command.get_from_proto(message.command)
            return command
        # elif message.HasField('enter'):
        #     enter = message.enter
        #     raise NotImplementedError


    def connect_to_replicas(self):
        print("CONNECTING TO REPLICAS")
        for i in range(1, self.replica.id):
            if i == self.replica.id:
                print("SELF")
                continue
            sock = self.connect_socket_init(socket.gethostname(), 2000+i, i)
            self.sockets_by_id[i] = sock

    def connect_socket_init(self, host, port, replica_id):
        while not self.stop:
            send_port = 10000 + 100 * self.replica.id + replica_id
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.bind((socket.gethostname(), send_port))
                print("Trying to connect from", send_port, "...")
                sock.connect((host, port))
                # sock.setblocking(0)
                return sock
            except Exception as e:
                print("Exception connecting to", replica_id, e, send_port)
                sleep(1)
                pass

    def accept_replica_sockets(self):
        print("ACCEPTING REPLICAS")
        while not self.stop:
            client, address = self.local_sock.accept()
            (host, port) = address
            sender_id = int(((port-self.replica.id)/100)-100)
            print("ACCEPTED")
            print("Accepted request at", self.replica.id, "FROM:", sender_id, client.getsockname(), address)
            self.sockets_by_id[sender_id] = client

    def send_msg(self, s, prototype):
        prototype.timestamp = time()
        if prototype is not None:
            msg = None
            try:
                msg = prototype.SerializeToString()
            except:
                if self.print:
                    print("ERROR SERIALIZING TO STRING")
            if msg is None:
                raise Exception
            _EncodeVarint(s.sendall, len(msg), None)
            try:
                s.sendall(msg)
            except:
                if self.print:
                    print("SOCKET DISCONNECTED EXCEPTION")
                raise SocketDisconnectedException("Socket Disconnected")

    def recv_msg(self, sock, prototype):
        var_int_buff = []
        msg_len = 0
        sock.setblocking(1)
        while not self.stop:
            buf = sock.recv(1)
            if not buf:
                sock.setblocking(0)
                return
            var_int_buff += buf
            try:
                msg_len, new_pos = _DecodeVarint32(var_int_buff, 0)
                if new_pos != 0:
                    break
            except Exception as e:
                # print("ERROR RECEIVING MSG", e)
                pass
        try:
            whole_msg = sock.recv(msg_len)
            prototype.ParseFromString(whole_msg)
            sock.setblocking(0)
            return prototype
        except BlockingIOError:
            return self.recv_blocked_msg(sock, prototype, msg_len)

    def recv_blocked_msg(self, sock, prototype, msg_len):
        attempts = 0
        while not self.stop:
            try:
                whole_msg = sock.recv(msg_len)
                prototype.ParseFromString(whole_msg)
                sock.setblocking(0)
                return prototype
            except:
                attempts += 1
                if attempts > 10:
                    sock.setblocking(0)
                    return None
                pass

class SocketDisconnectedException(Exception):
    def __init__(self, message=None):
        message = "Replica disconnected, trying to reconnect."
        super().__init__(message)

# Listen at: 2000+id: 2001, 2002, 2003, 2004
# Send at: 10104
# Receive = 10000 + 100*self.replica.id