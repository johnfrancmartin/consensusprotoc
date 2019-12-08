import math
import traceback
from threading import Thread, Lock
import socket
from Replica import Replica
from HotstuffReplica import HotstuffReplica
from MessageType import MessageType
from time import sleep
from CONFIG import PROTOCOL_PORT
from SocketHelper import SocketDisconnectedException
from Graveyard.BLSHelper import BLSHelper

# Central Authority
class Protocol:
    def __init__(self, n, latency, test_controller=None, hotstuff=False):
        # Initialization
        self.replicas = []
        self.n = n
        self.latency = latency
        self.f = math.floor(n/3) # max-f for now
        if hotstuff:
            self.qr = n-self.f
        else:
            self.qr = 2 * self.f + 1
        self.bls = BLSHelper(self.qr, n)
        self.hotstuff = hotstuff
        # Test
        self.test_controller=test_controller
        # Runtime Attributes
        self.delta = 10 # seconds

        # Unprocessed commands, when a leader creates a new block, it selects commands from this queue
        # commands_queue = [ c1 = [command, command, command], c2 = [command, command, command] ... ]
        # When leader creates a new block to propose, it pops c1, so commands_queue = [c2 = [command, command, command]]
        self.commands_queue = []
        self.commands = [] # All commands
        bls_proto = self.bls.proto_from_helper()
        for i in range(0, self.n):
            if not hotstuff:
                    self.replicas.append(Replica(self, i, self.qr, bls_proto))
            else:
                self.replicas.append(HotstuffReplica(self, i, self.qr, bls_proto))

        # Votes
        self.blocks = {}
        self.certified_blocks = {} # Store block_hash: votes set
        # Connection
        self.local_sock = self.listen_socket_init('', PROTOCOL_PORT)  # 44444
        # Stop
        self.stop = False
        # Workers
        self.worker_count = 0
        self.max_workers = 10
        self.worker_lock = Lock()
        self.pending_broadcast = []

    def pause(self):
        self.stop = True

    def initialize_connection(self):
        if self.local_sock:
            print("Local Listening Socket Established; Host:", '; Port:', PROTOCOL_PORT)

    def run(self):
        leader = self.replicas[0]
        leader.leader = True
        if not self.hotstuff:
            leader.propose(False, {})
        else:
            leader.propose(None)
        while not self.stop:
            if len(self.pending_broadcast) > 0:
                (sender, message) = self.pending_broadcast.pop(0)
                for replica in self.replicas:
                    if replica != sender:
                        replica.receive_msg(message)
            else:
                sleep(0.01)

    def broadcast(self, sender, signed_msg):
        if self.stop:
            return
        else:
            self.print_broadcast(sender, signed_msg)
            self.pending_broadcast.append((sender, signed_msg))

    def print_broadcast(self, sender, message):
        if message.type is MessageType.PROPOSE:
            if message.block.get_hash() not in self.blocks:
                self.blocks[message.block.get_hash()] = message.block
            if message.reproposal:
                x = 1
                # print(sender.id, "FORWARDED", message.block.get_hash())
            else:
                x = 1
                # print(sender.id, "PROPOSED", message.block.get_hash())
        elif message.type is MessageType.VOTE:
            hash_str = message.block.get_hash()
            if message.signature not in self.blocks[hash_str].signatures:
                self.blocks[hash_str].signatures[sender.id] = message.signature
            # print(sender.id, "VOTED FOR", message.block.get_hash())
        elif message.type is MessageType.BLAME:
            x = 1
            # print(sender.id, "BLAMED IN", message.view)
        elif message.type is MessageType.ENTER:
            x = 1
            # print(sender.id, "ENTERED", message.level)

    def send_msg_to_replica_with_id(self, id, message):
        if self.stop:
            return
        if message.type is MessageType.VOTE:
            self.print_broadcast(message.sender, message)
        replica = self.replicas[id]
        replica.receive_msg(message)

    def certify_block(self, block):
        hash_str = block.get_hash()
        if hash_str not in self.certified_blocks:
            self.certified_blocks[hash_str] = block
            if self.test_controller is not None:
                self.test_controller.did_certify(block)
            # print("CERTIFIED:", block.get_hash(), "BLOCK", len(self.certified_blocks))

    def update_commands(self):
        certified_commands = []
        new_queue = []
        for hash, block in self.certified_blocks.items():
            certified_commands.append(block.command)
        for command in self.commands:
            if command not in certified_commands:
                new_queue.append(command)
        self.commands_queue = new_queue
        if len(self.commands_queue) == 0:
            self.test_controller.commands_empty_notification()

    def add_command(self, command):
        self.commands_queue.append(command)
        self.commands.append(command)

    def listen_socket_init(self, host, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((host, port))
            sock.listen(10)
            return sock
        except Exception as e:
            print(e)

    def receive_client(self, client_socket, addr):
        while True:
            try:
                # bft_proto.BlameMSG()
                # bft_proto.ProposalMSG()
                # bft_proto.VoteMSG()
                # msg = recvMsg(client_socket, bft_proto.BlameMSG())
                msg = "NOT IMPLEMENTED YET"
                print("recv replica request: ", str(msg))
                # processA2U(msg, self)
            except SocketDisconnectedException as e:
                print("[ERROR: UPS SOCKET DISCONNECTED. RECONNECTING...]")
                # self.ups_sock, addr = self.connection.local_sock.accept()
                pass
            except Exception as e:
                print("ERROR: Listen for Replicas Thread.", e)
                print("Stack Trace:", traceback.print_exc())
                pass
            # msg = client_socket.recv(1024)
            #
            # client_socket.send(msg)
        # clientsocket.close()

    def listen_to_replicas(self):
        while True:
            c, address = self.local_sock.accept()  # Establish connection with client.
            x = Thread(target=self.receive_client, args=(c, address))
            x.start()
        # self.local_sock.close()

