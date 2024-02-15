import socket
import threading
import sys
import tenseal as ts
import numpy as np
import time

#  创建socket
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#  监听端口
soc.bind(('127.0.0.1', 3333))
soc.listen(5)
print('waiting for connection...')

def Tcplink(sock, addr):
    publicKey = sock.recv(40000000)
    pk = ts.context_from(publicKey)

    data_m1 = sock.recv(40000000)
    data_m2 = sock.recv(40000000)

    m1 = ts.ckks_vector_from(pk, data_m1)
    m2 = ts.ckks_vector_from(pk, data_m2)

    ans = m1 + m2
    time.sleep(1)
    sock.send(ans.serialize())


sock, addr = soc.accept()
Tcplink(sock, addr)

# while True:
#     #  接受一个新连接：
#     sock, addr = soc.accept()
#     #  创建新线程来处理连接
#     t = threading.Thread(target=Tcplink(sock, addr), args=(sock, addr))
#     t.start()