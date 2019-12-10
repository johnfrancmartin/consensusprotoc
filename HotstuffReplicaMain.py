import sys
from HotstuffReplica import HotstuffReplica

def main():
    args = sys.argv[1:]
    n = int(args[0])
    id = int(args[1])
    replica = HotstuffReplica(n, id)
    print("Running Replica,", id, flush=True)
    try:
        replica.run()
    except KeyboardInterrupt:
        replica.protocol.exit()


if __name__ == "__main__":
    main()