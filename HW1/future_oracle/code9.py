from pwn import *
import string
import hashlib
import random
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import base64
import hashpumpy
host = "140.112.31.96"
port = 10122
#
def first(ID,message):
    sha256 = SHA256.new()
    sha256.update(ID+"||"+message)
    digest = sha256.digest()
    return digest

def socket2(nc):
    r2 = remote(host, port)
    get = r2.recvuntil("me:")
    ID = 'admin'
    message = nc
    password = "IT'SMEPASSWORD"
    action = "printflag"
    digest = first(ID,message)
#    print(ID+'||'+message+'||'+base64.b64encode(digest))
    r2.sendline(ID+'||'+message+'||'+base64.b64encode(digest))
    get = r2.recvuntil('You')[:-4]
#    print(get)
    sp = get.split('||')
    ns = int(sp[0])
    cipher = sp[1]
#    print(ns,cipher)
    r2.recv()
    r2.close()
    return cipher


def main():
    ID = 'admin'
    message = "printflag"
    action = "login||printflag"
    L  = 21
    for i in range(L,30):
        r = remote(host, port)
        print(":QAQ")
        get = r.recvuntil("me:")
        digest = first(ID,message)
    #    print(ID+'||'+message+'||'+base64.b64encode(digest))
        r.sendline(ID+'||'+message+'||'+base64.b64encode(digest))
        get = r.recvuntil('You')[:-4]
     #   print(get)
        sp = get.split('||')
        ns = int(sp[0])
        cipher = sp[1]
    #    print(ns,cipher)
        cipher2 = socket2(str(+ns))
        
#        m1 = base64.b64encode(ID+"||"+str(ns)+"||"+action)
        #sha256 = SHA256.new()
        #sha256.update(password+"||"+ID+"||"+str(ns)+"||"+action)
        #digest = sha256.digest()
        digest = cipher2
        m2 = hashpumpy.hashpump(base64.b64decode(digest).encode('hex'), ID+"||"+str(ns)+"||login", "||printflag",i)
        print(m2)
        m1 = base64.b64encode(m2[1])
        m2 = base64.b64encode(m2[0].decode('hex'))
    #    m2 = 
        r.recv()
        #m2 = base64.b64encode(digest)
        r.sendline(m1+"||"+m2)
        print("len[{}]".format(i),r.recv())
#        r.close()
        r.interactive()

if __name__ == "__main__":
    main()
