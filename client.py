import socket
import sys
import tenseal as ts
import time
import random
import numpy as np

class Connect:
    soc = None
    def __init__(self, IP, PORT):
        '''在这里需要为连接提供套接字'''
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.connect((IP, PORT))
        print("socket create success!")

    def __delete__(self):
        '''这只是一个套接字的关闭函数'''
        self.soc.close()
        print("socket delete success!")

    def send(self, data):                           # fixme: 有点问题
        '''在这里需要为连接提供发送的bytes类型的数据'''
        self.soc.send(data)
        if data == b'exit':
            self.__delete__()
            sys.exit()
        print("socket send success!")

    def receive(self, buf=40000000):
        return self.soc.recv(buf)

class Ckks:
    context = None
    secretKey = None
    def __init__(self):
        '''初始化ckks的相关参数'''
        self.context = ts.context(ts.SCHEME_TYPE.CKKS, poly_modulus_degree=8192, coeff_mod_bit_sizes=[41, 40, 40, 40])  # fixme: coeff_mod_bit_sizes到时候要改一下
        self.context.global_scale = pow(2, 40)
        self.context.generate_galois_keys()
        self.context.generate_relin_keys()
        self.secretKey = self.context.secret_key()


    def encrypt(self, np_tensor):
        '''加密算法'''
        return ts.ckks_tensor(self.context, np_tensor)

    def decrypt(self, enc_tensor):
        '''解密算法'''
        return np.array(enc_tensor.decrypt().tolist())

    def generalPublicKey(self):
        '''生成公钥'''
        publicKey = self.context.serialize(save_public_key=True,
                                   save_secret_key=False,
                                   save_relin_keys=True,
                                   save_galois_keys=True)
        return publicKey




# test
def main():
    soc = Connect('127.0.0.1', 3333)
    m1 = [2, 5, 2]
    m2 = [4, 5, 6]
    p1, p2 = ts.plain_tensor(m1), ts.plain_tensor(m2)
    c = Ckks()
    e1, e2 = ts.ckks_vector(c.context, p1), ts.ckks_vector(c.context, p2)
    e1_send = e1.serialize()
    e2_send = e2.serialize()

    sk = c.secretKey
    pk = c.generalPublicKey()
    p1 = ts.context_from(pk)
    soc.send(pk)
    time.sleep(1)
    # m1+m2
    soc.send(e1_send)
    time.sleep(1)
    soc.send(e2_send)
    ans_ser = soc.receive()
    ckks_enc = ts.ckks_vector_from(c.context, ans_ser)
    ans = np.array(ckks_enc.decrypt(secret_key=sk))
    print("[2, 5, 2] + [4, 5, 6]:", ans)






main()


