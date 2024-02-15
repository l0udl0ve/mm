import tenseal as ts
import numpy as np

# CKKS 算法参数涉及三种（系数模（coeff_modulus）、多项式模度（poly_modulus_degree）、缩放因子（scale））
# 下面方法用于生成密文
# 伽罗瓦密钥：用来在同一个密文中移动明文
def context():
    context = ts.context(ts.SCHEME_TYPE.CKKS, poly_modulus_degree=8192, coeff_mod_bit_sizes=[41, 40, 40, 40])
    # 多项式的度数维8192，这个参数同时也指定了一个密文中最多可以加密4096个明文
    # 系数模的大小直接影响了密文元素的大小，是一个向量，向量的长度指定了最多可以进行同态乘法的次数，本例可以算4次
    context.global_scale = pow(2, 40)
    context.generate_galois_keys()
    return context

# 返回加密后的张量
def encrypt(context, np_tensor):
    return ts.ckks_tensor(context, np_tensor)

# 返回解密后的张量
def decrypt(enc_tensor):
    return np.array(enc_tensor.decrypt().tolist())

if __name__ == "__main__":
    c = context()
    sk = c.secret_key()
    c.make_context_public()

    bytes_str_c = c.serialize(save_public_key=True,
                                           save_secret_key=False,
                                           save_relin_keys=True,
                                           save_galois_keys=True)

    bytes_str_sk = c.serialize(save_public_key=False,
                                           save_secret_key=True,
                                           save_relin_keys=False,
                                           save_galois_keys=False)


    print(type(bytes_str_c))
    print(type(bytes_str_sk))
    c1 = ts.context_from(bytes_str_c)
    sk1 = ts.context_from(bytes_str_sk)

    # 加法和乘法直接使用+, *, @ 即可
    m1 = [2, 5, 2]
    m2 = [4, 5, 6]
    p1, p2 = ts.plain_tensor(m1), ts.plain_tensor(m2)

    e1, e2 = ts.ckks_vector(c1, p1), ts.ckks_vector(c1, p2)
    #e1, e2 = ts.ckks_vector(c, p1), ts.ckks_vector(c, p2)
    print("[2, 5, 2] + [4, 5, 6]:", (e1 + e2).decrypt(secret_key=sk))



