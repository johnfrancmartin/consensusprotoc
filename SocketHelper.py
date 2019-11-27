from google.protobuf.internal.encoder import _EncodeVarint
from google.protobuf.internal.decoder import _DecodeVarint32
import google.protobuf
import socket


class SocketDisconnectedException(Exception):
    def __init__(self, message, errors):
        message = "Replica disconnected, trying to reconnect."
        # Call the base class constructor with the parameters it needs
        super().__init__(message, errors)

def sendMsg(s, protoType):
    if protoType is not None:
        msg = protoType.SerializeToString()
        _EncodeVarint(s.sendall, len(msg), None)
        try:
            s.sendall(msg)
        except:
            raise SocketDisconnectedException


def recvMsg(s, protoType):
    var_int_buff = []
    while True:
        buf = s.recv(1)
        if not buf:
            raise SocketDisconnectedException
        var_int_buff += buf
        try:
            msg_len, new_pos = _DecodeVarint32(var_int_buff, 0)
            if new_pos != 0:
                break
        except Exception as e:
            print(e)
            pass
    whole_msg = s.recv(msg_len)
    protoType.ParseFromString(whole_msg)
    return protoType


