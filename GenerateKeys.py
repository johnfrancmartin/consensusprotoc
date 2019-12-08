from Crypto.PublicKey import RSA
import json
import sys
import os
import Crypto.Util.number as CUN
import base64
import hashlib

def main():
    args = sys.argv[1:]
    # n = int(args[0])
    n = 4
    privates = {}
    publics = {}
    signatures = {}
    hash_bytes = b"iodaiosnfluisbrui23"
    hash_str = hashlib.sha256(hash_bytes).hexdigest()
    hash_enc = hash_str.encode()
    K = CUN.getRandomNumber(128, os.urandom)
    for i in range(1, n+1):
        private_key = RSA.generate(1024)
        public_key = private_key.publickey()

        decpriv = private_key.exportKey(format='PEM').decode('utf-8')
        decpub = public_key.exportKey(format='PEM').decode('utf-8')

        privates[i] = decpriv
        publics[i] = decpub

        # K = CUN.getRandomNumber(128, os.urandom)
        # signature = private_key.sign(hash_enc, K)
        # signatures[i] = signature

    # signatures = {2: 52122305835952393389763858239316475166940469701550659201410370778856081411060679191883948509748113591994617443583940650927522258172343412540867544430119100258587726190061832488878422674455560950502535783982967464229002978187239277635648816593578523822181563258687889753614868906418916409589219495107082657736, 4: 100276436334669927647240215983561751109132430747823420309115635261624460467275811876954080057268478010027481948074966205384710449403118290115601682563048367970995760021001337143386004977556820628860335501468425466831957574344356820669183269247241338464014005192864247982580614353032867252418106158277834241400, 3: 104754787007924194633019868648864254437540005359829546417495969099456676420430444513766390855418416194164597087406875419001260892908789522895064742263261376352513930968930941246303500458578220836950155429977617673708932550979781681538998999081000410131902452287269399470311861466256936321327472943252900952204}
    # sigs = [str(sig) for sender, sig in signatures.items()]
    # unique_cert = ":".join(sigs)
    # print(sigs)
    # print(unique_cert)

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