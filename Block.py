from Certificate import Certificate
import hashlib
from time import time

class Block:
    def __init__(self, command, height, view, previous_hash):
        self.command = command
        if command is not None:
            self.commands = command.commands
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

    def clone_for_view(self, view):
        return Block(self.command, self.height, view, self.previous_hash)

    def get_hash(self):
        previous = self.previous_hash
        if previous is None:
            previous = ""
        commands_str = " ".join([str(i) for i in self.commands])
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