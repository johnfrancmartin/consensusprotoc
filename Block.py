from Certificate import Certificate
import hashlib
from time import time
import BFT_pb2
from bls.scheme import Bn


class Block:
    def __init__(self, command, height, view, previous_hash):
        self.command = command
        if command is not None:
            self.commands = [command]
        else:
            self.commands = []
        self.height = height
        self.view = view
        self.previous_hash = previous_hash
        if height > 0 and previous_hash is None:
            raise NotImplementedError
        self.signatures = {}
        self.unique_cert = None
        self.certification = None

    def get_proto(self):
        proto = BFT_pb2.Block()
        for i in self.commands:
            proto.commands.append(i)
        proto.view = self.view
        proto.height = self.height
        prev = self.previous_hash
        if prev == None:
            prev = ""
        proto.previous = prev
        if self.unique_cert is not None:
            proto.unique_cert = self.unique_cert.hex().encode('utf-8')
        return proto

    @staticmethod
    def get_from_proto(proto):
        commands = []
        for command in proto.commands:
            commands.append(command)
        if len(commands) == 0:
            command = 0
            print("NO COMMANDS")
        else:
            command = commands[0]
        block = Block(command, proto.height, proto.view, proto.previous)
        unique_cert = proto.unique_cert
        if unique_cert is not None and unique_cert != b'':
            block.unique_cert = Bn.from_hex(proto.unique_cert.decode('utf-8'))
        return block

    def clone_for_view(self, view):
        return Block(self.command, self.height, view, self.previous_hash)

    def get_hash(self):
        previous = self.previous_hash
        if previous is None:
            previous = ""
        if len(self.commands) != 0:
            commands_str = " ".join([str(i) for i in self.commands])
        else:
            commands_str = ""
        hash_str = commands_str + ":" + str(self.view) + ":" + str(self.height) + ":" + previous
        hash_bytes = str.encode(hash_str)
        return hashlib.sha256(hash_bytes).hexdigest()

    def sign(self, sender, signature):
        self.signatures[sender.id] = signature

    def certify(self, bls_helper):
        if self.unique_cert is None:
            sigs = [sig for sender, sig in self.signatures.items()]
            self.unique_cert = bls_helper.aggregate_sigs(sigs)
        else:
            sigs = [sig for sender, sig in self.signatures.items()]
            self.certification = bls_helper.aggregate_sigs(sigs)