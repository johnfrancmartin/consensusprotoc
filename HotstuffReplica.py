from HotstuffBlock import Block
from time import time, sleep
from MessageType import MessageType, Proposal, Vote, Blame, Enter
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from BLSHelper import BLSHelper
from threading import Lock


class HotstuffReplica:
    def __init__(self, protocol, id, qr, bls_proto):
        # Replica Core
        self.protocol = protocol
        self.id = id
        self.level = 0
        self.leader = False
        self.bls_helper = BLSHelper(0, 0, bls_proto)
        self.sk = self.bls_helper.sk[id]
        self.vk = self.bls_helper.vk[id]
        # Lock
        self.locked = None
        self.lock_time = None
        self.proposed = None
        # Blocks
        self.blocks = {}
        self.certified = []
        # Votes
        self.changes = {}
        # Voting
        self.qr = qr
        # View Change
        self.status = {}
        # Proposals
        self.proposals = []
        self.proposed = None
        # Pending
        self.pending_proposals = []
        # Stop
        self.stop = False
        # QC
        self.qc_ref = None
        self.hqc = None
        #
        self.propose_lock = Lock()

    # REPLICA FUNCTIONS

    def stop(self):
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
        while len(self.protocol.commands_queue) == 0 and not self.stop:
            self.protocol.update_commands()
            sleep(0.1)
        command = self.protocol.commands_queue.pop(0)
        block = Block(command, self.level, self.qc_ref, self.hqc)
        return block

    def propose(self, previous):
        self.propose_lock.acquire()
        if previous is not None:
            self.qc_ref = previous
            self.hqc = previous.level
        if self.proposed is None:
            block = self.create_block()
            self.proposed = block
            sig = self.sign_blk(block)
            block.sign(self, sig)
            proposal = Proposal(block, self.level, block.commit_certification, {}, self, sig)
            self.proposals.append(proposal)
            self.broadcast(proposal)
        self.propose_lock.release()

    def receive_proposal(self, proposal):
        if proposal in self.proposals:
            return
        bnew = proposal.block
        if bnew.certification is None:
            if bnew.qc_ref is not None:
                self.update_hqc(bnew)
            if bnew.level in self.blocks and self.blocks[bnew.level] != bnew:
                self.blame()
                return
            self.blocks[bnew.level] = bnew
            self.lock(bnew)
            self.vote(bnew)
        elif self.locked == bnew:
            self.vote(bnew)

    def update_hqc(self, bnew):
        if (self.hqc is None and bnew.hqc is not None) or bnew.hqc > self.hqc:
            self.qc_ref = bnew.qc_ref
            self.hqc = bnew.level
            self.unlock()

    def vote(self, block):
        signature = self.sign_blk(block)
        # Conditionally Sign Block
        leader_id = block.level % self.protocol.n
        if self not in block.signatures:
            block.sign(self, signature)
            self.protocol.send_msg_to_replica_with_id(leader_id, Vote(block, self.level, signature, self))

    def receive_vote(self, vote):
        block = vote.block
        if block.level % self.protocol.n != self.id:
            # NOT LEADER
            return
        if self.level != block.level:
            # Done with that level
            return
        if block.certification is None and len(block.signatures) >= self.qr:
            block.certify(self.bls_helper)
            block.signatures = {}
            leader_sig = self.sign_blk(block)
            proposal = Proposal(block, self.level, block.qc_ref, {}, self, leader_sig)
            block.sign(self, leader_sig)
            self.proposals.append(proposal)
            self.broadcast(proposal)
        elif len(block.signatures) >= self.qr and block.commit_certification is None:
            block.certify(self.bls_helper)
            self.protocol.certify_block(block)
            self.view_change(block)

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

    def receive_msg(self, message):
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
        self.protocol.broadcast(self, message)

    def sign_blk(self, block):
        hash_str = block.get_hash()
        signature = self.bls_helper.get_signature(self.sk, str.encode(hash_str, 'utf-8'))
        return signature

    def verify_signature(self, block, signature, signer):
        signer_vk = signer.vk
        hash_str = block.get_hash()
        return self.bls_helper.verify_signature(signature, signer_vk, str.encode(hash_str, 'utf-8'))
