from Block import Block
from time import time, sleep
from MessageType import MessageType, Proposal, Vote, Blame
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from BLSHelper import BLSHelper
from ReplicaConnection import ReplicaConnection
import math
from threading import Thread
from BFT_pb2 import Wrapper


class Replica:
    def __init__(self, n, id, bls_proto):
        # Replica Core
        self.n = n
        self.f = math.floor(n / 3)  # max-f for now
        self.qr = 2 * self.f + 1
        self.id = id
        self.protocol = ReplicaConnection(n, self)
        # Commands
        self.commands_queue = []
        for i in range(0, 20000):
            self.commands_queue.append(1)
        # Runtime Variables
        self.view = 1
        self.leader = False
        self.bls_helper = BLSHelper(0, 0, bls_proto)
        self.sk = self.bls_helper.sk[id-1]
        self.vk = self.bls_helper.vk[id-1]
        # Lock
        self.locked = None
        self.lock_time = None
        self.proposed = None
        # Blocks
        self.blocks = {}
        self.certified = []
        # Votes
        self.changes = {}
        # View Change
        self.status = {}
        # Proposals
        self.proposals = []
        self.proposal_hashes = []
        # Pending
        self.pending_proposals = []
        # Stop
        self.stop = False

    # REPLICA FUNCTIONS

    def run(self):
        connection_t = Thread(target=self.protocol.run, args=())
        connection_t.start()
        sleep(3)
        print(self.id)
        if self.id == self.view % self.protocol.n:
            print("LEADER")
            try:
                self.leader = True
                self.propose(False, {})
            except Exception as e:
                print("Exception:", e)
        connection_t.join()

    def stop(self):
        self.protocol.stop = True
        self.stop = True

    def view_change(self, status):
        self.changes[self.view] = time()
        self.status = {}
        self.proposed = None
        self.view += 1
        if self.id == self.view % self.protocol.n:
            self.leader = True
            self.propose(False, status)
        else:
            self.leader = False
            for prop in self.pending_proposals:
                if prop.view == self.view and prop.block.height == self.locked.height + 1:
                    self.receive_proposal(prop)
                elif prop.view < self.view:
                    self.pending_proposals.remove(prop)

    def create_block(self, previous):
        while len(self.commands_queue) == 0 and not self.stop:
            print("SLEEP")
            sleep(0.1)
        command = self.commands_queue.pop(0)
        previous_hash = None
        height = 0
        if previous is not None and previous.commands is not None:
            previous_hash = previous.get_hash()
            height = previous.height + 1
        block = Block(command, height, self.view, previous_hash)
        return block

    def propose(self, steady_state, status):
        if status is None:
            status = {}
        if not steady_state:
            previous = Block(None, 0, 0, None)
            for sender, block in status.items():
                if block.view >= previous.view and block.height >= previous.height: # TODO: ADD VERIFY THRESHOLD SIGNATURE
                    previous = block
        else:
            previous = self.locked
        if previous is not None and previous.commands is not None:
            previous = previous.clone_for_view(self.view)
            block = self.create_block(previous)
        else:
            block = self.create_block(None)
        signature = self.sign_blk(block)
        # TODO: ADD SIGNATURE
        proposal = Proposal(block, self.view, previous, status)
        block.sign(self, signature)
        self.proposals.append(proposal)
        self.proposal_hashes.append(proposal.get_hash())
        self.broadcast(proposal.get_proto())
        self.vote(block)

    def propose_lock(self, block):
        if self.leader:
            print(self.id, "PROPOSED UNIQUE")
            signature = self.sign_blk(block)
            block.sign(self, signature)
            proposal = Proposal(block, self.view, block.previous_hash, {})
            self.proposals.append(proposal)
            self.proposal_hashes.append(proposal.get_hash())
            prop_proto = proposal.get_proto()
            self.broadcast(proposal.get_proto())

    def receive_proposal(self, proposal):
        if proposal in self.proposals:
            return
        else:
            self.proposals.append(proposal)
        if proposal.view > self.view or (self.locked is not None and proposal.block.height > self.locked.height + 1):
            self.pending_proposals.append(proposal)
        elif proposal.view == self.view:
            block = proposal.block
            if (self.proposed is None and self.proposal_extends_status(proposal)) \
                    or (self.proposed is not None and block.previous_hash is not None and block.previous_hash == self.proposed.get_hash()):
                self.proposed = block
                self.broadcast(proposal.get_proto())
                self.vote(block)
            elif block.unique_cert is not None and self.proposed.get_hash() == block.get_hash():
                self.broadcast(proposal.get_proto())
                self.vote(block)
            elif self.proposed.get_hash() == block.get_hash() and block.unique_cert is not None:
                self.proposed.unique_cert = block.unique_cert
                self.broadcast(proposal.get_proto())
                self.vote(block)

    def vote(self, block):
        signature = self.sign_blk(block)
        # Conditionally Sign Block
        if self not in block.signatures:
            block.sign(self, signature)
            self.broadcast(Vote(block, self.view, signature, self).get_proto())
        elif len(block.signatures) >= self.qr:
            block.sign(self, signature)
            self.broadcast(Vote(block, self.view, signature, self).get_proto())
        if len(block.signatures) >= self.qr and block.unique_cert is None:
            block.certify(self.bls_helper)
            self.propose_lock(block)
        elif len(block.signatures) >= self.qr:
            block.certify(self.bls_helper)
            self.lock(block)

    def receive_vote(self, vote):
        block = vote.block
        sender_id = vote.sender
        signature = vote.signature
        block_hash = block.get_hash()
        verify = self.verify_signature(block, signature, sender_id)
        if not verify:
            # If signature not valid, blame sender
            print("BLAME FOR INVALID SIGNATURE")
            self.blame()
            return
        elif block_hash in self.blocks:
            self.blocks[block_hash].signatures[sender_id] = signature
        else:
            if sender_id not in block.signatures:
                block.signatures[sender_id] = signature
            self.blocks[block_hash] = block
        if vote.view == self.view and self.proposed is not None and block.height == self.proposed.height and block_hash != self.proposed.get_hash():
            # If same view, height and different ID
            print("BLAME FOR EQUIVOCATING BLOCK")
            print("PROPOSED", self.proposed.get_hash())
            print("NEW", block_hash)
            self.blame()
            return
        elif vote.view == self.view and block_hash not in self.blocks:
            self.blocks[block_hash] = block
        block = self.blocks[block_hash]
        if len(block.signatures) >= self.qr and block.unique_cert is None:
            block.certify(self.bls_helper)
            self.propose_lock(block)
        elif len(block.signatures) >= self.qr:
            block.certify(self.bls_helper)
            self.lock(block)

    def lock(self, block):
        if self.locked is not None and self.locked.get_hash() == block.get_hash():
            return
        self.locked = block
        self.status[self.id] = block
        print(self.id, "CERTIFIED BLOCK", block.get_hash())
        if self.leader:
            print("LEADER PROPOSE")
            self.propose(True, self.status)
        else:
            for prop in self.pending_proposals:
                if prop.view == self.view and prop.block.height == self.locked.height + 1:
                    self.receive_proposal(prop)
                elif prop.view < self.view:
                    self.pending_proposals.remove(prop)

    def blame(self):
        blame = Blame(self.view, self, self.locked)
        raise NotImplementedError
        self.broadcast(blame)

    def receive_msg(self, message):
        if message.type == MessageType.PROPOSE:
            if message.get_hash() in self.proposal_hashes:
                print(self.id, "RECEIVED REPROPOSAL")
            else:
                self.proposal_hashes.append(message.get_hash())
                print(self.id, "RECEIVED PROPOSAL")
                self.receive_proposal(message)
        elif message.type == MessageType.VOTE:
            print(self.id, "RECEIVED VOTE")
            self.receive_vote(message)
        elif message.type == MessageType.BLAME:
            print(self.id, "RECEIVED BLAME")
            self.receive_blame(message)

    def receive_blame(self, message):
        view = message.view
        sender_id = message.sender
        sender_locked = message.status
        if sender_id not in self.status:
            self.status[sender_id] = sender_locked
        if len(self.status) >= self.qr:
            self.view_change(self.status)

    def proposal_extends_status(self, proposal):
        proposed = proposal.block
        highest = Block(None, 0, 0, None)
        for sender, block in proposal.status.items():
            if block.view >= highest.view and block.height >= highest.height:
                highest = block
        if highest.commands is None or len(proposal.status) == 0 or highest.get_hash() == proposed.previous_hash:
            return True
        else:
            return False

    def proposal_extends_previous(self, proposal):
        if self.proposed.get_hash() == proposal.block.previous_hash:
            return True
        else:
            return False

    def broadcast(self, message):
        self.protocol.broadcast(message)

    def sign_blk(self, block):
        print("A")
        hash_str = block.get_hash()
        print("B")
        signature = self.bls_helper.get_signature(self.sk, str.encode(hash_str, 'utf-8'))
        print("C")
        return signature

    def verify_signature(self, block, signature, signer):
        signer_vk = self.bls_helper.vk[signer - 1]
        hash_str = block.get_hash()
        verification = self.bls_helper.verify_signature(signature, signer_vk, str.encode(hash_str, 'utf-8'))
        return verification

