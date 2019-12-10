from enum import Enum
import BFT_pb2
from Block import Block
import hashlib

class MessageType(Enum):
    PROPOSE = 0
    VOTE = 1
    BLAME = 2
    ENTER = 3
    COMMAND = 4

class Message:
    def __init__(self, type):
        self.type = type

class Proposal(Message):
    def __init__(self, block, view, previous_cert, status):
        self.block = block
        self.view = view
        self.previous_cert = previous_cert
        self.status = status
        super().__init__(MessageType.PROPOSE)

    def get_hash(self):
        cert = ""
        if self.block.lock_cert is not None:
            cert = self.block.lock_cert
        hash_str = self.block.get_hash() + ":" + str(self.view) + ":" + str(self.previous_cert) \
                   + ":" + str(self.status) + ":" + str(cert)
        hash_bytes = str.encode(hash_str)
        return hashlib.sha256(hash_bytes).hexdigest()

    def get_proto(self):
        wrapper_proto = BFT_pb2.Wrapper()
        wrapper_proto.proposal.block.CopyFrom(self.block.get_proto())
        if self.previous_cert is not None:
            wrapper_proto.proposal.previous = self.previous_cert
        wrapper_proto.proposal.view = self.view
        return wrapper_proto

    @staticmethod
    def get_from_proto(proto):
        status = {}
        i = 0
        if proto.status is not None:
            for blk in proto.status:
                block = Block.get_from_proto(blk)
                status[i] = block
                i += 1
        previous = None
        if proto.previous is not None:
            previous = proto.previous
        return Proposal(Block.get_from_proto(proto.block), proto.view, previous, status)

class Vote(Message):
    def __init__(self, block, view, signature, sender):
        self.block = block
        self.view = view
        self.signature = signature
        self.sender = sender
        super().__init__(MessageType.VOTE)

    def get_proto(self):
        wrapper_proto = BFT_pb2.Wrapper()
        wrapper_proto.vote.block.CopyFrom(self.block.get_proto())
        wrapper_proto.vote.view = self.view
        # proto.signature =
        wrapper_proto.vote.sender = self.sender.id
        wrapper_proto.vote.signature = str(self.signature)
        return wrapper_proto

    @staticmethod
    def get_from_proto(proto):
        signature = int(proto.signature)
        return Vote(Block.get_from_proto(proto.block), proto.view, signature, proto.sender)

class Blame(Message):
    def __init__(self, view, sender, status):
        self.view = view
        self.sender = sender
        self.status = status
        super().__init__(MessageType.BLAME)

class Command(Message):
    def __init__(self, commands):
        self.commands = commands
        super().__init__(MessageType.COMMAND)

    @staticmethod
    def get_from_proto(proto):
        print("A")
        commands = []
        for i in proto.commands:
            commands.append(i)
        print("B")
        return Command(commands)

class Enter(Message):
    def __init__(self, sender, level, block):
        self.sender = sender
        self.level = level
        self.block = block
        super().__init__(MessageType.ENTER)