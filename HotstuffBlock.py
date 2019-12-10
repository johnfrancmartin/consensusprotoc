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

    def sign(self, sender_id, signature):
        self.signatures[sender_id] = signature

    def certify(self):
        siggies = []
        for sender, sig in self.signatures.items():
            str_sig = str(sig)
            siggies.append(str_sig)
        cert: str = ":".join(siggies)
        if self.certification is None:
            self.certification = cert

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
