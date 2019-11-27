from Protocol import Protocol
import random
from threading import Thread
from time import sleep, time


class TestController:
    def __init__(self, n, avg_throughput, avg_latency, total_commands, max_commands, hotstuff=False):
        self.n = n
        self.avg_throughput = avg_throughput # commands per second
        self.avg_latency = avg_latency # seconds
        self.protocol = Protocol(n, avg_latency, self, hotstuff=hotstuff)
        self.total_commands = total_commands
        self.max_commands = max_commands
        self.commands = []
        self.certified_count = 0
        self.avg_certify_time = 0

    def create_cmd(self, cmd):
        command = Command([cmd])
        self.commands.append(command)
        self.protocol.add_command(command)

    def did_certify(self, block):
        block.command.certified = time()
        time_to_cert = block.command.certified - block.command.created
        self.avg_certify_time = (self.certified_count*self.avg_certify_time + time_to_cert)/(self.certified_count+1)
        self.certified_count += 1
        if self.certified_count >= self.max_commands:
            self.protocol.pause()

    def commands_empty_notification(self):
        if len(self.commands) >= self.max_commands:
            self.protocol.pause()

    def run(self):
        for i in range(0, self.total_commands):
            self.create_cmd(random.randint(0, 1))
        print("created all commands")
        self.protocol.run()

    def calculate_avg_cert_time(self):
        cert_times = []
        for command in self.commands:
            if command.certified is not None:
                time_to_cert = command.certified - command.created
                cert_times.append(time_to_cert)
        return sum(cert_times)/len(cert_times)

class Command:
    def __init__(self, commands):
        self.commands = commands
        self.created = time()
        self.certified = None


ns = [4]

flex_avgs = {}
flex_throughputs = {}
total_commands = 200000
max_commands = 1000
# params = [0.5, 0.625, 0.75, 0.875, 1, 2, 4, 8, 16, 32, 64, 128]
params = [0]
# params = [8]
for r in ns:
    averages = []
    tps = []
    for i in params:
        print("\n\n\n I = ", i)
        begin = time()
        tc = TestController(r, 10, i, total_commands, max_commands, hotstuff=False)
        tc.run()
        averages.append(tc.avg_certify_time)
        end = time()
        throughput = tc.certified_count/(end-begin)
        tps.append(throughput)
    flex_avgs[r] = averages
    flex_throughputs[r] = tps

print(flex_avgs)
print(flex_throughputs)
import hashlib
start = time()
hash_str = "aoisnhd2[ioq34uy3289psdfjkabhru324iu23jbnrklwdjgzps9dgyh983n4ASFadsfdsf2351324"
hash_bytes = str.encode(hash_str)
hash_digest = hashlib.sha256(hash_bytes).hexdigest()
end = time()
print(end-start)
# hs_avgs = {}
# hs_throughputs = {}
# for r in ns:
#     averages = []
#     tps = []
#     for j in params:
#         print("\n\n\n I = ", j)
#         begin = time()
#         tc = TestController(r, 10, j, total_commands, max_commands, hotstuff=True)
#         tc.run()
#         averages.append(tc.avg_certify_time)
#         end = time()
#         throughput = tc.certified_count/(end-begin)
#         tps.append(throughput)
#     hs_avgs[r] = averages
#     hs_throughputs[r] = tps

print("HS")

