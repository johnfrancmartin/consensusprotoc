from Certificate import Certificate
import hashlib
from time import time
import BFT_pb2

class Block:
    def __init__(self, commands, level, qc_ref, hqc):
        self.commands = commands
        self.level = level
        self.qc_ref = None
        self.hqc = None
        if qc_ref is not None and qc_ref != "":
            self.qc_ref = qc_ref
        if hqc is not None:
            self.hqc = hqc
        self.signatures = {}
        self.lock_cert = None
        self.commit_certification = None

    def get_proto(self):
        proto = BFT_pb2.Block()
        for i in self.commands:
            proto.commands.append(i)
        proto.view = self.level
        prev = self.qc_ref
        if prev == None:
            prev = ""
        proto.previous = prev
        if self.hqc is not None:
            proto.hqc = self.hqc
        if self.lock_cert is not None:
            proto.lock_cert = self.lock_cert
        proto.hotstuff = True
        return proto

    @staticmethod
    def get_from_proto(proto):
        commands = []
        for command in proto.commands:
            commands.append(command)
        block = Block(commands, proto.view, proto.previous, proto.hqc)
        lock_cert = proto.lock_cert
        if lock_cert is not None and lock_cert != "":
            block.lock_cert = str(proto.lock_cert)
        return block

    def get_hash(self):
        previous_hash = self.qc_ref
        if previous_hash is None:
            previous_hash = ""
        commands_str = " ".join([str(i) for i in self.commands])
        hash_str = commands_str + ":" + str(self.level) + ":" + previous_hash
        hash_bytes = str.encode(hash_str)
        return hashlib.sha256(hash_bytes).hexdigest()

    def sign(self, sender_id, signature):
        self.signatures[sender_id] = signature

    def certify(self):
        siggies = []
        for sender, sig in self.signatures.items():
            str_sig = str(sig)
            siggies.append(str_sig)
        cert: str = ":".join(siggies)
        if self.lock_cert is None:
            self.lock_cert = cert

    def verify_cert(self, public_keys_dict, cert, qr):
        cert_sigs = [int(s) for s in cert.split(":")]
        count = 0
        for sig in cert_sigs:
            for id, key in public_keys_dict.items():
                if self.check_signature(key, sig):
                    count += 1
                    break
            if count >= qr:
                return True
        return False

    def check_signature(self, public_key, signature):
        hash_str = self.get_hash()
        verification = public_key.verify(hash_str, (signature,))
        return verification
