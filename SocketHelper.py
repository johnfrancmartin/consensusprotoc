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

def sendMsg(s, protoType):
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

def recvMsg(sock, prototype):
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
    whole_msg = sock.recv(msg_len)
    prototype.ParseFromString(whole_msg)
    print("RECEIVED", prototype.id)
    return prototype

def recvMsg2(s, protoType):
    var_int_buff = []
    start = time()
    s.setblocking(0)
    ready = select.select([s], [], [], 0.1)
    if ready[0]:
        while True:
            if time() - start > 0.1:
                print("RETURNING DUE TO TIMEOUT")
                return
            buf = s.recv(1)
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
        whole_msg = s.recv(msg_len)
        protoType.ParseFromString(whole_msg)
        print("RECEIVED", protoType.id)
        return protoType
    else:
        # print("RETURNING DUE TO TIMEOUT")
        return


