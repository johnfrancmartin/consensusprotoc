from Certificate import Certificate
import hashlib
from time import time

class Block:
    def __init__(self, command, level, qc_ref, hqc):
        self.command = command
        if command is not None:
            self.commands = command.commands
        else:
            self.commands = []
        self.level = level
        self.qc_ref = None
        self.hqc = None
        if qc_ref is not None:
            self.qc_ref = qc_ref
        if hqc is not None:
            self.hqc = hqc
        #
        self.signatures = {}
        self.certification = None
        self.commit_certification = None

    def get_hash(self):
        previous = self.qc_ref
        if previous is None:
            previous_hash = ""
        else:
            previous_hash = previous.get_hash()
        commands_str = " ".join([str(i) for i in self.commands])
        hash_str = commands_str + ":" + str(self.level) + ":" + previous_hash
        hash_bytes = str.encode(hash_str)
        return hashlib.sha256(hash_bytes).hexdigest()

    def sign(self, sender, signature):
        self.signatures[sender.id] = signature

    def certify(self, bls_helper):
        sigs = [sig for sender, sig in self.signatures.items()]
        if self.certification is None:
            self.certification = bls_helper.aggregate_sigs(sigs)
        elif self.commit_certification is None:
            self.certification = bls_helper.aggregate_sigs(sigs)