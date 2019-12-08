from bls.scheme import *
import petlib
from bplib.bp import G1Elem, G2Elem, BpGroup
import BFT_pb2
from time import time, sleep
import uuid
from petlib.bn import Bn
import traceback

class BLSHelper:
    def __init__(self, t, n, proto=None):
        if proto is None:
            self.t = t
            self.n = n
            self.params = setup()
            (self.sk, self.vk) = self.generate_keys()
        else:
            self.t = proto.t
            self.n = proto.n
            self.params = self.params_from_proto(proto)
            (self.sk, self.vk) = self.sk_vk_from_proto(proto)

    def proto_from_helper(self):
        helper_proto = BFT_pb2.BLSHelper()
        # Params
        (group, sk, sig, vk, method) = self.params
        # print(type(sk.hex()))
        helper_proto.sk_bytes = sk.binary()
        helper_proto.g1_bytes = sig.export()
        helper_proto.g2_bytes = vk.export()
        helper_proto.optimize_mult = group.optimize_mult
        helper_proto.group_nid = group.nid
        # Sk, Vk
        for s in self.sk:
            sb = s.binary()
            helper_proto.sk_bytes_set.append(sb)
        for v in self.vk:
            helper_proto.vk_bytes_set.append(v.export())
        return helper_proto

    def params_from_proto(self, proto):
        group = BpGroup(proto.group_nid, proto.optimize_mult)
        sk = Bn.from_binary(proto.sk_bytes)
        sig = G1Elem.from_bytes(proto.g1_bytes, group)
        vk = G2Elem.from_bytes(proto.g2_bytes, group)
        return (group, sk, sig, vk, group.pair)

    def sk_vk_from_proto(self, proto):
        group = self.params[0]
        sk = []
        for s in proto.sk_bytes_set:
            sk.append(Bn.from_binary(s))
        vk = []
        for v in proto.vk_bytes_set:
            vk.append(G2Elem.from_bytes(v, group))
        return (sk, vk)

    def proto_from_signature(self, sig):
        sig_proto = BFT_pb2.Signature()
        sig_proto.optimize_mult = sig.group.optimize_mult
        sig_proto.group_nid = sig.group.nid
        sig_proto.sig_bytes = sig.export()
        return sig_proto

    def signature_from_proto(self, proto):
        group = BpGroup(proto.group_nid, proto.optimize_mult)
        return G1Elem.from_bytes(proto.sig_bytes, group)

    def proto_from_key(self, key):
        key_proto = BFT_pb2.Key()
        key_proto.optimize_mult = key.group.optimize_mult
        key_proto.group_nid = key.group.nid
        key_proto.sig_bytes = key.export()
        return key_proto

    def key_from_proto(self, proto):
        group = BpGroup(proto.group_nid, proto.optimize_mult)
        return G2Elem.from_bytes(proto.sig_bytes, group)

    def generate_keys(self):
        (sk, vk) = ttp_keygen(self.params, self.t, self.n)
        return (sk, vk)

    def verify_signature(self, sig, vk, message):
        aggr_sigma = self.aggregate_sigs([sig])
        aggr_vk = self.aggregate_vks([vk])
        return verify(self.params, aggr_vk, aggr_sigma, message)

    def verify_signatures(self, vks, signatures, message):
        aggr_sigma = self.aggregate_sigs(signatures)
        aggr_vk = self.aggregate_vks(vks)
        return verify(self.params, aggr_vk, aggr_sigma, message)

    def verify_signatures_for_threshold(self, signatures, message, t):
        if t > self.n:
            return False
        verified = []
        for sig in signatures:
            if sig in verified:
                continue
            for vk in self.vk:
                if self.verify_signature(sig, vk, message):
                    verified.append(sig)
        return len(verified) >= t

    def aggregate_sigs(self, signatures):
        return aggregate_sigma(self.params, signatures)

    def aggregate_vks(self, vks):
        return aggregate_vk(self.params, vks)

    def get_signature(self, sk, message):
        try:
            return sign(self.params, sk, message)
        except Exception as e:
            try:
                raise TypeError("Again !?!")
            except:
                pass
            traceback.print_tb(e.__traceback__)

    def keygen(self, params, t, n):
        """ generate keys for threshold signature (executed by a TTP) """
        assert n >= t and t > 0
        (G, o, g1, g2, e) = params
        # generate polynomials
        v = [o.random() for _ in range(0, t)]
        # generate shares
        sk = self.sk
        # set keys
        vk = [xi * g2*o.random() for xi in sk]
        vk = [G2Elem.from_bytes(v.binary(), G) for v in vk]
        return (sk, vk)


# Bn(0)

# print(str(uuid.uuid4()))
# bls = BLSHelper(3, 5)
# sk1 = bls.sk[0]
# sk2 = bls.sk[1]
# sk3 = bls.sk[2]
# message = b"asoidhion"
# sig1 = bls.get_signature(sk1, message)
# sig2 = bls.get_signature(sk2, message)
# sig3 = bls.get_signature(sk3, message)
# sigma = bls.aggregate_sigs([sig1])
# verify = bls.verify_signatures(bls.vk, [sig1], message)
# print(verify)
# print(verify)
# print(type(sigma))
# print(sigma)
# h = sigma.hex()
# from_h = Bn.from_hex(h)
# print(sigma == from_h)
# print(from_h)
# print(h)
#
# print(h.encode('utf-8'))


# spl = bina.split('0'.encode())
# # blah = bina.decode()
# print(spl)
# preback = Bn.from_binary(bina)
# print(preback)
# print(bina)
# bina = bina.replace(b'x', b'')
# print(bina)
# back = Bn.from_binary(bina)
# print(back)
#
# print(back == preback)

