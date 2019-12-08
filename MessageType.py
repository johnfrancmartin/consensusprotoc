from enum import Enum
import BFT_pb2
from Block import Block
import hashlib

class MessageType(Enum):
    PROPOSE = 0
    VOTE = 1
    BLAME = 2
    ENTER = 3

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
        if self.block.unique_cert is not None:
            cert = self.block.unique_cert
        hash_str = self.block.get_hash() + ":" + str(self.view) + ":" + str(self.previous_cert) + ":" + str(self.status) + ":" + str(cert)
        hash_bytes = str.encode(hash_str)
        return hashlib.sha256(hash_bytes).hexdigest()

    def get_proto(self):
        wrapper_proto = BFT_pb2.Wrapper()
        wrapper_proto.proposal.block.CopyFrom(self.block.get_proto())
        wrapper_proto.proposal.view = self.view
        return wrapper_proto

    @staticmethod
    def get_from_proto(proto):
        status = {}
        i = 0
        for blk in proto.status:
            block = Block.get_from_proto(blk)
            status[i] = block
            i += 1
        proposal = Proposal(Block.get_from_proto(proto.block), proto.view, proto.previous, status)
        return Proposal(Block.get_from_proto(proto.block), proto.view, proto.previous, status)

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

class Enter(Message):
    def __init__(self, sender, level, block):
        self.sender = sender
        self.level = level
        self.block = block
        super().__init__(MessageType.ENTER)