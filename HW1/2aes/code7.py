tooaes = __import__('2aes')
def int2bytes(n):
    return bytes.fromhex('{0:032x}'.format(n))

p_ex = 'NoOneUses2AES_QQ'
c_ex = int2bytes(int('0e46d393fdfae760f9d4c7837f47ce51',16))
c_flag = int2bytes(int('3e3a9839eb6331aa03f76e1a908d746bfccaf7acb22265b725a9f1fc0644cdda',16))

from Crypto.Cipher import AES

def brute_force_step(key, plain, cipher):
    aes128 = AES.new(key=key, mode=AES.MODE_ECB)
    return {aes128.encrypt(plain):key}, {aes128.decrypt(cipher):key}

def brute_force(p_ex, c_ex, c_flag):
    step1_dic = {}
    step2_dic = {}
    for i in range(2**23):
        if i % 10000 == 0:
            print ("building table [{}/{}]".format(i,2**23))
        a, b = brute_force_step(int2bytes(i), p_ex, c_ex)
        step1_dic.update(a)
        step2_dic.update(b)
    key0 = 0
    key1 = 0
    for x in step1_dic:
         if x in step2_dic:
            key0 = step1_dic[x]
            key1 = step2_dic[x]
            print(key0, key1)
            break
    print("key", key0, key1)
    aes2 = tooaes.DoubleAES(key0, key1)
    FLAG = aes2.decrypt(c_flag)
    print(FLAG)

if __name__ == "__main__":
    brute_force(p_ex, c_ex, c_flag)
