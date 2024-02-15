import tenseal as ts
import numpy as np

import tenseal as ts


# Context 生成与分发（密钥都在 Context 里面）
# 分发过程需要序列化操作
class TensealKeyManage:
    def __init__(self):
        self.ckks_context = ts.context(ts.SCHEME_TYPE.CKKS, 8192,
                                       coeff_mod_bit_sizes=[22, 21, 21, 21, 21, 21, 21, 21, 21, 21])
        self.ckks_context.global_scale = pow(2, 21)
        self.ckks_context.generate_galois_keys()
        self.ckks_context.generate_relin_keys()
        self.bfv_context = ts.context(ts.SCHEME_TYPE.BFV, 4096, plain_modulus=1032193)

    # 分发 CKKS 公钥
    def get_ckks_publicKey(self) -> bytes:
        return self.ckks_context.serialize(save_public_key=True,
                                           save_secret_key=False,
                                           save_relin_keys=True,
                                           save_galois_keys=True)

    # 分发 CKKS 所有密钥
    def get_ckks_secretKey(self) -> bytes:
        return self.ckks_context.serialize(save_public_key=True,
                                           save_secret_key=True,
                                           save_relin_keys=True,
                                           save_galois_keys=True)

    # 分发 BFV 公钥
    def get_bfv_publicKey(self) -> bytes:
        return self.bfv_context.serialize(save_public_key=True,
                                          save_secret_key=False,
                                          save_relin_keys=True,
                                          save_galois_keys=True)

    # 分发 BFV 所有密钥
    def get_bfv_secretKey(self) -> bytes:
        return self.bfv_context.serialize(save_public_key=True,
                                          save_secret_key=True,
                                          save_relin_keys=True,
                                          save_galois_keys=True)



class TensealCryptor:
    def __init__(self, ckks_context_ser):
        # CKKS 加密设置
        self.ckks_context = ts.context_from(ckks_context_ser)

    # 加密并序列化
    def CkksEncrypt(self, np_vector) -> bytes:
        return ts.ckks_tensor(self.ckks_context, np_vector).serialize()

    # 反序列化并解密
    def CkksDecrypt(self, enc_ser: bytes):
        ckks_enc = ts.ckks_tensor_from(self.ckks_context, enc_ser)
        return np.array(ckks_enc.decrypt().tolist())


if __name__ == '__main__':
    keyManage = TensealKeyManage()
    cryptor = TensealCryptor(keyManage.get_ckks_secretKey())

    b = np.array([0, 0, 0])

    enc_b_ser = cryptor.CkksEncrypt(b)

    print(cryptor.CkksDecrypt(enc_b_ser))