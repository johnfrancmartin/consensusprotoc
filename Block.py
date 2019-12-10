from Certificate import Certificate
import hashlib
from time import time
import BFT_pb2

class Block:
    def __init__(self, command, height, view, previous_hash):
        self.command = command
        if type(command) is list:
            self.commands = command
        elif command is not None:
            self.commands = [command]
        else:
            self.commands = []
        self.height = height
        self.view = view
        self.previous_hash = previous_hash
        if height > 0 and previous_hash is None:
            raise NotImplementedError
        self.signatures = {}
        self.lock_cert: str = None
        self.commit_cert: str = None

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
        if self.lock_cert is not None:
            proto.lock_cert = self.lock_cert
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
        lock_cert = proto.lock_cert
        if lock_cert is not None and lock_cert != "":
            block.lock_cert = str(proto.lock_cert)
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
        else:
            self.commit_cert = cert

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