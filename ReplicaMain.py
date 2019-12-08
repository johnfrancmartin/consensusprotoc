import sys
from Replica import Replica
from BLSHelper import BLSHelper
import BFT_pb2
from google.protobuf.json_format import Parse

def main():
    args = sys.argv[1:]
    n = int(args[0])
    id = int(args[1])
    with open("bls.json", 'r') as jsfile:
        data = ''.join(jsfile.readlines())
        data.replace("\n", "")
        bls_proto = BFT_pb2.BLSHelper()
        Parse(data, bls_proto)
    replica = Replica(n, id, bls_proto)
    print("Running Replica,", id, flush=True)
    try:
        replica.run()
    except KeyboardInterrupt:
        replica.protocol.stop = True


if __name__ == "__main__":
    main()
