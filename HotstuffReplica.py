from HotstuffBlock import Block
from ReplicaConnection import ReplicaConnection
from time import time, sleep
from MessageType import MessageType, Proposal, Vote, Blame, Enter
from threading import Lock
from Crypto.PublicKey import RSA
import Crypto.Util.number as CUN
import os
import uuid
import json
import math


class HotstuffReplica:
    def __init__(self, n, id):
        # Replica Core
        self.n = n
        # Debug
        self.print = False
        self.stop = False
        # Voting
        self.qr = n - math.floor(n / 3)
        self.id = id
        self.level = 1
        self.leader = False
        # Commands
        self.commands_lock = Lock()
        self.commands_queue = []
        self.command_start_times = {}
        self.command_commit_times = []
        self.batch_size = 2048
        # KEYS
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
        self.commands_lock = Lock()
        # Lock
        self.locked = None
        self.lock_time = None
        self.proposed = None
        # Blocks
        self.blocks = {}
        self.blockchain = {}
        self.certified = []
        self.committed = []
        # Votes
        self.changes = {}
        # View Change
        self.status = {}
        # Proposals
        self.proposals = []
        self.proposal_hashes = []
        self.proposed = None
        # Pending
        self.pending_proposals = []
        # QC
        self.qc_ref = None
        self.hqc = None
        #
        self.propose_lock = Lock()
        # Connection
        self.protocol = ReplicaConnection(n, self)

    # REPLICA FUNCTIONS
        # REPLICA FUNCTIONS
    def run(self):
        self.protocol.run()

    def network_initialized(self):
        if self.id == self.level % self.protocol.n:
            print("LEADER", flush=True)
            try:
                self.leader = True
                self.propose(None)
            except Exception as e:
                print("Exception:", e, flush=True)

    def exit(self):
        self.stop = True

    def view_change(self, block):
        if block is None:
            # self.level = self.level + 1
            print("BLAMED")
        elif self.level <= block.level:
            self.level = block.level + 1
            self.proposed = None
            enter = Enter(self, block.level + 1, block)
            self.broadcast(enter)
            leader = self.level % self.protocol.n
            if leader == self.id:
                self.propose(block)

    def create_block(self):
        self.commands_lock.acquire()
        if len(self.commands_queue) == 0:
            uid = str(uuid.uuid4())
            commands = [uid for i in range(0, self.batch_size)]
            # FILLER BLOCK
        else:
            commands = self.commands_queue.pop(0)
        self.commands_lock.release()
        block = Block(commands, self.level, self.qc_ref, self.hqc)
        return block

    def propose(self, previous):
        print("PROPOSING", flush=True)
        self.propose_lock.acquire()
        previous_cert = None
        if previous is not None:
            self.qc_ref = previous
            self.hqc = previous.level
            previous_cert = previous.qc_ref
        block = self.create_block()
        self.proposed = block
        sig = self.sign_blk(block)
        block.sign(self, sig)
        proposal = Proposal(block, self.level, previous_cert, {})
        self.proposals.append(proposal)
        self.proposal_hashes.append(proposal.get_hash())
        self.broadcast(proposal.get_proto())
        self.vote(block)
        self.propose_lock.release()

    def receive_proposal(self, proposal):
        print("Receive proposal", flush=True)
        if proposal.get_hash() in self.proposal_hashes:
            return
        self.proposal_hashes.append(proposal.get_hash())
        bnew = proposal.block
        if bnew.qc_ref is not None:
            self.update_hqc(bnew)
        if bnew.level in self.blockchain and self.blockchain[bnew.level].get_hash() != bnew.get_hash():
            self.blame()
            return
        self.blockchain[bnew.level] = bnew
        if bnew.get_hash() not in self.blocks:
            self.blocks[bnew.get_hash()] = bnew
        self.lock(bnew)
        self.vote(bnew)

    def update_hqc(self, bnew):
        if (self.hqc is None and bnew.hqc is not None) or bnew.hqc > self.hqc:
            self.blockchain[bnew.level-1].qc_ref = bnew.qc_ref
            self.qc_ref = bnew.qc_ref
            self.hqc = bnew.level
            self.level = bnew.level
            self.unlock()

    def vote(self, block):
        print("Vote", flush=True)
        signature = self.sign_blk(block)
        # Conditionally Sign Block
        leader_id = block.level % self.protocol.n
        if self not in block.signatures:
            block.sign(self, signature)
            if leader_id != self.id:
                vote = Vote(block, self.level, signature, self)
                self.protocol.direct_message(vote.get_proto(), leader_id)

    def receive_vote(self, vote):
        print("RECEIVE VOTE", flush=True)
        block = vote.block
        sender_id = vote.sender
        signature = vote.signature
        block_hash = block.get_hash()
        if block.get_hash() in self.blocks:
            local_block = self.blocks[block_hash]
            local_block.sign(sender_id, signature)
        else:
            self.blocks[block_hash] = block
            block.sign(sender_id, signature)
            local_block = block
        if block.level % self.protocol.n != self.id:
            # NOT LEADER
            return
        if self.level != block.level:
            # Done with that level
            return
        if block.qc_ref is None and len(local_block.signatures) >= self.qr:
            local_block.certify()
            self.propose(local_block)
            # self.view_change(block)
            if block.previous_hash in self.blocks and self.blocks[block.previous_hash].qc_ref is not None:
                minusOne = self.blocks[block.previous_hash]
                if minusOne.previous_hash in self.blocks and self.blocks[minusOne.previous_hash].qc_ref is not None:
                    minusTwo = self.blocks[minusOne.previous_hash]
                    self.commit(minusTwo)

    def commit(self, block):
        new_update = self.update_commit_tracking(block)
        if not new_update:
            return
        current = block
        for i in range(0, block.height):
            previous_hash = current.previous_hash
            if previous_hash not in self.blocks:
                break
            current = self.blocks[previous_hash]
            if current.commit_cert is None:
                current.certify()
            new_update = self.update_commit_tracking(current)
            if not new_update:
                break

    def update_commit_tracking(self, block):
        if block not in self.committed:
            self.committed.append(block)
            command = block.commands[0]
            if command in self.command_start_times:
                commit_time = time() - self.command_start_times[command]
                self.command_commit_times.append(commit_time)
            print("COMMITTED BLOCK")
            self.protocol.log()
            return True
        else:
            return False

    def receive_enter(self, message):
        if message.level < self.level or message.sender == self:
            return
        self.view_change(message.block)

    def lock(self, block):
        if self.locked == block:
            return
        self.locked = block

    def unlock(self):
        self.locked = None

    def blame(self):
        self.view_change(None)

    def receive_msg(self, message, msg_id):
        print("RECEIVED MESSAGE", msg_id, flush=True)
        if message.type == MessageType.PROPOSE:
            self.receive_proposal(message)
        elif message.type == MessageType.VOTE:
            self.receive_vote(message)
        elif message.type == MessageType.BLAME:
            self.receive_blame(message)
        elif message.type == MessageType.ENTER:
            self.receive_enter(message)

    def receive_blame(self, message):
        raise NotImplementedError

    def broadcast(self, message):
        print("BROADCASTING", flush=True)
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
