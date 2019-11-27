from BLSHelper import BLSHelper
from bplib.bp import G1Elem, G2Elem, BpGroup

bls = BLSHelper(5, 10)
m = b"AHASD"
sigs = []
for i in range(0, 7):
    sigs.append(bls.get_signature(bls.sk[i], m))

vk = bls.vk
group = bls.params[0]
for i in range(0, 1):
    vk.append(G2Elem(bls.params[0]))

print(bls.check_threshold(sigs, m, 5))

# print(bls.verify_signatures(vk, sigs, m))

