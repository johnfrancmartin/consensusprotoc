from bls.scheme import *


class Certificate:
    def __init__(self, block, view, signatures):
        self.block = block
        self.view = view
        self.signatures = signatures


    def graveyard(self):
        m = [3] * 2  # messages
        t, n = 2, 3  # number of authorities
        params = setup()  # generate the public parameters.
        (sk, vk) = ttp_keygen(params, t, n)  # generate key
        aggr_vk = aggregate_vk(params, vk)  # aggregate verification keys
        sigs = [sign(params, ski, m) for ski in sk]  # sign
        sigma = aggregate_sigma(params, sigs)  # aggregate credentials
        assert verify(params, aggr_vk, sigma, m)  # verify signature

# class Vote:
#     def __init__(self, replica, signature):
#         self.replica = replica
#         self.signature = signature