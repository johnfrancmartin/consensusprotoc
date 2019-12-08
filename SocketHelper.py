from google.protobuf.internal.encoder import _EncodeVarint
from google.protobuf.internal.decoder import _DecodeVarint32
import google.protobuf
import socket
from time import time
import BFT_pb2
import select


class SocketDisconnectedException(Exception):
    def __init__(self, message=None):
        message = "Replica disconnected, trying to reconnect."
        super().__init__(message)


def send_msg(s, protoType):
    if protoType is not None:
        msg = None
        try:
            msg = protoType.SerializeToString()
        except:
            print("ERROR SERIALIZING TO STRING")
        if msg is None:
            raise Exception
        _EncodeVarint(s.sendall, len(msg), None)
        try:
            s.sendall(msg)
        except:
            print("SOCKET DISCONNECTED EXCEPTION")
            raise SocketDisconnectedException("Socket Disconnected")


def recv_msg(sock, prototype):
    var_int_buff = []
    while True:
        buf = sock.recv(1)
        if not buf:
            print("RETURNING DUE TO EMPTY BUF")
            return
        var_int_buff += buf
        try:
            msg_len, new_pos = _DecodeVarint32(var_int_buff, 0)
            if new_pos != 0:
                break
        except Exception as e:
            print("ERROR RECEIVING MSG", e)
            pass
    print(msg_len)
    try:
        whole_msg = sock.recv(msg_len)
        prototype.ParseFromString(whole_msg)
        print("RECEIVED", prototype.id)
        return prototype
    except BlockingIOError:
        return recv_blocked_msg(sock, prototype, msg_len)


def recv_blocked_msg(sock, prototype, msg_len):
    attempts = 0
    while True:
        try:
            whole_msg = sock.recv(msg_len)
            prototype.ParseFromString(whole_msg)
            print("RECEIVED", prototype.id)
            return prototype
        except:
            attempts += 1
            if attempts > 10:
                return None
            pass