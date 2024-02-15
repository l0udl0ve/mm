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
    print(type(c))
    print(c.serialize())
    input()
    # 例1：
    message = [60.5, 66.1, 73, 81, 90]
    plain_vector = ts.plain_tensor(message)
    print("明文：", plain_vector.tolist())
    encrypted_vector = ts.ckks_vector(c, plain_vector)
    print("加密后再解密：", encrypted_vector.decrypt()) # tolist是用来将多项式m(X)解码成张量的
    print()

    # 例2：
    # 加法和乘法直接使用+, *, @ 即可
    m1 = [2, 5, 2]
    m2 = [4, 5, 6]
    p1, p2 = ts.plain_tensor(m1), ts.plain_tensor(m2)
    e1, e2 = ts.ckks_vector(c, p1), ts.ckks_vector(c, p2)
    print(dir(e1))
    print()
    print(e1.serialize())
    input()
    print("[2, 5, 2] + [4, 5, 6]:", (e1 + e2).decrypt())
    print("[2, 5, 2] * [4, 5, 6]:", (e1 * e2).decrypt())


