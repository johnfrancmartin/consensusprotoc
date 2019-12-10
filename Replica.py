from Block import Block
from time import time, sleep
from MessageType import MessageType, Proposal, Vote, Blame
from ReplicaConnection import ReplicaConnection
import math
import json
from Crypto.PublicKey import RSA
import Crypto.Util.number as CUN
import os
import uuid


class Replica:
    def __init__(self, n, id):
        # Replica Core
        self.print = True
        self.n = n
        self.f = math.floor(n / 3)  # max-f for now
        self.qc = 2 * self.f + 1
        self.qr = 2 * self.f + 1
        self.id = id
        self.protocol = ReplicaConnection(n, self)
        # Commands
        self.commands_queue = []
        batch_size = 64
        for i in range(0, 20000):
            uid = str(uuid.uuid4())
            command = [uid for i in range(0, batch_size)]
            self.commands_queue.append(command)
        # Runtime Variables
        self.view = 1
        self.leader = False
        with open("private.json", "r") as prv_file:
            privs = json.load(prv_file)
        with open("public.json", "r") as pub_file:
            pubs = json.load(pub_file)

        self.public_key = None
        self.private_key = None
        self.private_keys = {}
        self.public_keys = {}
        for id, key in privs.items():
            int_id = int(id)
            rsa_key = RSA.importKey(key.encode())
            self.private_keys[int_id] = rsa_key
            if int_id == self.id:
                self.private_key = rsa_key
        for id, key in pubs.items():
            int_id = int(id)
            rsa_key = RSA.importKey(key.encode())
            self.public_keys[int_id] = rsa_key
            if int_id == self.id:
                self.public_key = rsa_key
        # Lock
        self.locked = None
        self.lock_time = None
        self.proposed = None
        # Blocks
        self.blocks = {}
        self.certified = []
        self.committed = []
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
        self.protocol.run()

    def network_initialized(self):
        if self.id == self.view % self.protocol.n:
            if self.print:
                print("LEADER", flush=True)
            try:
                self.leader = True
                self.propose(False, {})
            except Exception as e:
                if self.print:
                    print("Exception:", e, flush=True)

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
            if self.print:
                print("SLEEP", flush=True)
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
            previous = self.proposed
        if previous is not None and previous.commands is not None:
            previous = previous.clone_for_view(self.view)
            block = self.create_block(previous)
        else:
            block = self.create_block(None)
        signature = self.sign_blk(block)
        # TODO: ADD SIGNATURE
        proposal = Proposal(block, self.view, previous, status)
        block.sign(self.id, signature)
        self.proposals.append(proposal)
        self.proposal_hashes.append(proposal.get_hash())
        self.broadcast(proposal.get_proto())
        self.vote(block)

    def propose_cert(self, block):
        if self.leader:
            if self.print:
                print(self.id, "PROPOSED UNIQUE", flush=True)
            signature = self.sign_blk(block)
            block.sign(self.id, signature)
            proposal = Proposal(block, self.view, block.previous_hash, {})
            self.proposals.append(proposal)
            self.proposal_hashes.append(proposal.get_hash())
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
            elif block.lock_cert is not None and self.proposed.get_hash() == block.get_hash():
                self.broadcast(proposal.get_proto())
                self.vote(block)
            elif self.proposed.get_hash() == block.get_hash() and block.lock_cert is not None:
                self.proposed.lock_cert = block.lock_cert
                self.broadcast(proposal.get_proto())
                self.vote(block)

    def vote(self, block):
        signature = self.sign_blk(block)
        if self not in block.signatures:
            block.sign(self.id, signature)
            self.broadcast(Vote(block, self.view, signature, self).get_proto())


    def block_extends(self, block):
        if self.locked is None:
            return True
        elif block.height == self.locked.height:
            return block.get_hash() == self.locked.get_hash()
        else:
            if block.height > self.locked.height:
                current = block
                end = self.locked
            else:
                current = self.locked
                end = block
            for i in range(0, current.height):
                previous_hash = current.previous_hash
                if previous_hash == end.get_hash():
                    return True
                if previous_hash in self.blocks:
                    current = self.blocks[previous_hash]
                else:
                    return False
        return False

    def receive_vote(self, vote):
        block = vote.block
        sender_id = vote.sender
        signature = vote.signature
        block_hash = block.get_hash()
        verify = self.verify_signature(block, signature, sender_id)
        if not verify:
            # If signature not valid, blame sender
            if self.print:
                print("BLAME FOR INVALID SIGNATURE", flush=True)
            self.blame()
            return
        elif not self.block_extends(block):
            if self.print:
                print("BLAME FOR EQUIVOCATING BLOCK", flush=True)
                print("PROPOSED", self.proposed.get_hash(), flush=True)
                print("NEW", block_hash, flush=True)
            self.blame()
        elif block_hash in self.blocks:
            self.blocks[block_hash].sign(sender_id, signature)
        else:
            if sender_id not in block.signatures:
                block.sign(sender_id, signature)
            self.blocks[block_hash] = block
        self.check_block_status(self.blocks[block_hash])

    def check_block_status(self, block):
        if len(block.signatures) >= self.qr and block.lock_cert is None:
            block.certify()
            self.lock(block)
            self.next()
        elif len(block.signatures) >= self.qc:
            block.certify()
            if block.previous_hash in self.blocks and self.blocks[block.previous_hash].commit_cert is not None:
                previous = self.blocks[block.previous_hash]
                self.commit(previous)

    def commit(self, block):
        self.committed.append(block)
        current = block
        for i in range(0, block.height):
            previous_hash = current.previous_hash
            if previous_hash not in self.blocks:
                break
            current = self.blocks[previous_hash]
            if current.commit_cert is None:
                current.certify()
            else:
                return

    def next(self):
        if self.leader:
            if self.print:
                print("LEADER PROPOSE", flush=True)
            self.propose(True, self.status)
        else:
            for prop in self.pending_proposals:
                if prop.view == self.view and prop.block.height == self.locked.height + 1:
                    self.receive_proposal(prop)
                elif prop.view < self.view:
                    self.pending_proposals.remove(prop)

    def lock(self, block):
        if self.locked is not None and self.locked.get_hash() == block.get_hash():
            return
        self.locked = block
        self.status[self.id] = block
        if self.print:
            print(self.id, "CERTIFIED BLOCK", block.get_hash(), flush=True)
        self.certified.append(block)


    def blame(self):
        blame = Blame(self.view, self, self.locked)
        raise NotImplementedError
        self.broadcast(blame)

    def receive_msg(self, message):
        if message.type == MessageType.PROPOSE:
            if message.get_hash() in self.proposal_hashes:
                if self.print:
                    print(self.id, "RECEIVED REPROPOSAL", flush=True)
            else:
                self.proposal_hashes.append(message.get_hash())
                if self.print:
                    print(self.id, "RECEIVED PROPOSAL", flush=True)
                self.receive_proposal(message)
        elif message.type == MessageType.VOTE:
            if self.print:
                print(self.id, "RECEIVED VOTE", flush=True)
            self.receive_vote(message)
        elif message.type == MessageType.BLAME:
            if self.print:
                print(self.id, "RECEIVED BLAME", flush=True)
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
        hash_str = block.get_hash()
        K = CUN.getRandomNumber(128, os.urandom)
        hash_enc = hash_str.encode()
        signature = self.private_key.sign(hash_enc, K)
        return signature[0]

    def verify_signature(self, block, signature, signer):
        signer_pub_key = self.public_keys[signer]
        hash_str = block.get_hash()
        hash_enc = hash_str.encode()
        verification = signer_pub_key.verify(hash_enc, (signature,))
        return verification

