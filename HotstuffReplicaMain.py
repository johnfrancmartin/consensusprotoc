import sys
from HotstuffReplica import HotstuffReplica
from time import sleep

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
        sleep(2)
        raise KeyboardInterrupt


if __name__ == "__main__":
    main()