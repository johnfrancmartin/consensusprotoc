from Crypto.Hash import SHA256
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from time import time
import hashlib

start = time()
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
end = time()
print(end-start)

start = time()
message = b"A message I want to sign"
signature = private_key.sign(
    message,
    padding.PSS(
    mgf=padding.MGF1(hashes.SHA256()),
    salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)
end = time()
print(end-start)

start = time()
public_key = private_key.public_key()
public_key.verify(
    signature,
    message,
    padding.PSS(
    mgf=padding.MGF1(hashes.SHA256()),
    salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)
end = time()
print(end-start)



hash_str = "akldsfhq3u4oiph15o34289213yroruibgsidlfjkhg9o134857u23p095j1n2rgpwuihelsaiut981235y012983p5htpui4rbfs9pe857312p5hnp109832512"
hash_bytes = str.encode(hash_str)

start = time()

hash = SHA256.new(hash_bytes)
print(hash.hexdigest())

end = time()
diffA = end-start
print()

start = time()
print(hashlib.sha256(hash_bytes).hexdigest())
end = time()
diffB = end-start

print(diffA-diffB)

import nacl.encoding
import nacl.signing

start = time()
# Generate a new random signing key
signing_key = nacl.signing.SigningKey.generate()

# Sign a message with the signing key
signed = signing_key.sign(b"Attack at Dawn")

# Obtain the verify key for a given signing key
verify_key = signing_key.verify_key

# Serialize the verify key to send it to a third party
verify_key_hex = verify_key.encode(encoder=nacl.encoding.HexEncoder)

import nacl.signing

# Create a VerifyKey object from a hex serialized public key
# verify_key = nacl.signing.VerifyKey(verify_key_hex,
                                    # encoder=nacl.encoding.HexEncoder)

# Check the validity of a message's signature
# The message and the signature can either be passed separately or
# concatenated together.  These are equivalent:
verify_key.verify(signed)

end = time()
print(end-start)
# verify_key.verify(signed.message, signed.signature)

# Alter the signed message text
# forged = signed[:-1] + bytes([int(signed[-1]) ^ 1])
# Will raise nacl.exceptions.BadSignatureError, since the signature check
# is failing
# verify_key.verify(forged)