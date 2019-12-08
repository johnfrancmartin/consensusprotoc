from Crypto.PublicKey import RSA
import json
import sys
import os
import Crypto.Util.number as CUN
import base64

def main():
    args = sys.argv[1:]
    n = int(args[1])
    privates = {}
    publics = {}
    for i in range(1, n+1):
        private_key = RSA.generate(1024)
        public_key = private_key.publickey()

        decpriv = private_key.exportKey(format='PEM').decode('utf-8')
        decpub = public_key.exportKey(format='PEM').decode('utf-8')

        privates[i] = decpriv
        publics[i] = decpub


    with open("private.json", "w") as prv_file:
        json.dump(privates, prv_file)

    with open("public.json", "w") as pub_file:
        json.dump(publics, pub_file)

    with open("private.json", "r") as prv_file:
        privs = json.load(prv_file)

    with open("public.json", "r") as pub_file:
        pubs = json.load(pub_file)



if __name__ == "__main__":
    main()

# start = time()
# private_key = rsa.generate_private_key(
#     public_exponent=65537,
#     key_size=2048,
#     backend=default_backend()
# )
# end = time()
# print(end-start)
#
# start = time()
# message = b"A message I want to sign"
# signature = private_key.sign(
#     message,
#     padding.PSS(
#     mgf=padding.MGF1(hashes.SHA256()),
#     salt_length=padding.PSS.MAX_LENGTH
#     ),
#     hashes.SHA256()
# )
# end = time()
# print(end-start)
#
# start = time()
# public_key = private_key.public_key()
# public_key.verify(
#     signature,
#     message,
#     padding.PSS(
#     mgf=padding.MGF1(hashes.SHA256()),
#     salt_length=padding.PSS.MAX_LENGTH
#     ),
#     hashes.SHA256()
# )
# end = time()
# print(end-start)