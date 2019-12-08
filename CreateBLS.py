from BLSHelper import BLSHelper
import sys
from google.protobuf.json_format import MessageToJson

def main():
    args = sys.argv[1:]
    t = int(args[0])
    n = int(args[1])
    bls = BLSHelper(t, n)
    sk = bls.sk[0]
    message = b"aidasuihnliwe"
    sig = bls.get_signature(sk, message)
    bls_proto = bls.proto_from_helper()
    with open("bls.json", 'w') as jsfile:
        actual_json_text = MessageToJson(bls_proto)
        print(actual_json_text)
        jsfile.write(actual_json_text)



if __name__ == "__main__":
    main()