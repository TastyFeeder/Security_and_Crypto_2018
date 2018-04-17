from pwn import *
from Crypto.Cipher import AES
import base64
import gmpy
from hashlib import sha1
HOST = "140.112.31.96"
PORT = 10123

def Register(name, password):
    r = remote(HOST, PORT)
    r.recvuntil("> ")
    r.sendline(str(0))
    r.recvuntil('Your user name: ')
    r.sendline(name)
    r.recvuntil('Your password: ')
    r.sendline(password)
    r.recvuntil("[+] Your token: ")
    token = r.recv()
    r.close()
    return token
def Login(r, token, username, password):
    r.recvuntil("> ")
    r.sendline(str(1))
    r.recvuntil('Provide your token: ')
    r.sendline(token)
    r.recvuntil('Provide your username: ')
    r.sendline(username)
    r.recvuntil("Provide your password: ")
    r.sendline(password)
    r.recv()
    return token

def get_transaction(r):
    r.sendline(str(0))
    r.recvuntil('sig')
    t1 = r.recvline()
    t1 = t1.split(' ')[:-1]
    t1[0] = t1[0][2:-3]
    r.recvuntil('sig')
    t2 = r.recvline()
    t2 = t2.split(' ')[:-1]
    t2[0] = t2[0][2:-3]
    r.recv()
    return (t1[0], int(t1[1]), int(t1[2])), (t2[0], int(t2[1]), int(t2[2]))

def get_pub(r):
    r.sendline(str(1))
    r.recvuntil('p = ')
    p = r.recvline()[:-1]
    r.recvuntil('q = ')
    q = r.recvline()[:-1]
    r.recvuntil('g = ')
    g = r.recvline()[:-1]
    r.recvuntil('y = ')
    y = r.recvline()[:-1]
    return (int(p),int(q),int(g),int(y))
def veri(t1, pub):
    #m3 = int(sha.hexdigest(), 16)
    r = t1[1]
    s = t1[2]
    m = t1[0]
    p = pub[0]
    q = pub[1]
    g = pub[2]
    y = pub[3]
    sha = sha1()
    sha.update(m)
    w = gmpy.invert(s, q)
    u1 = (int(sha.digest().encode('hex'), 16) * w) % q 
    u2 = ( r * w ) % q
    v = ((pow(g,u1,p)*pow(y,u2,p)) %p ) % q
    print(v, r % q)
    if v % q  == r % q:
        print(" usung SHA1") 
    return True

def solve_share_k(t1, t2, pub):
    r1 = t1[1]
    s1 = t1[2]
    m1 = t1[0]
    r2 = t2[1]
    s2 = t2[2]
    m2 = t2[0]
    p = pub[0]
    q = pub[1]
    g = pub[2]
    y = pub[3]
# use two sign to solve share k 
    sha = sha1()
    sha.update(m1)
    hm1 = int(sha.digest().encode('hex'), 16)
    sha = sha1()
    sha.update(m2)
    hm2 = int(sha.digest().encode('hex'), 16)
    dhm = hm1 - hm2
    ds = s1 - s2
    invds = gmpy.invert(ds, q)
    k = (invds * dhm) % q
    tmp = (k * s1 - hm1) % q
    x = (tmp * gmpy.invert(r1, q)) % q
    return x, k

def sign(m, pub, x, k):
    p = pub[0]
    q = pub[1]
    g = pub[2]
    y = pub[3]
    sha = sha1()
    sha.update(m)
    hm = int(sha.digest().encode('hex'), 16)
    r = pow(g, k, p) % q
    s = ((hm + x * r) * gmpy.invert(k, q)) % q
    return (r,s)
def main():
# login=1234&role= guest&pwd=admin
    token1 = Register('1234','admin')
    print token1
# login=1234567890 admin&role=gues tpwd=admin
    token2 = Register('1234567890admin','admin')
    print token2
    #print(len(base64.b64decode(token1)))
    #print(len(base64.b64decode(token2)))
# login=1234&role= admin&role=gues tpwd=admin
    token = base64.b64encode(base64.b64decode(token1)[:16] + base64.b64decode(token2)[16:48])
    name = '1234'
    password = 'admin'
    r = remote(HOST, PORT)
    mess = Login(r, token, name, password)
    print(mess)
    t1,t2 = get_transaction(r)
    pub = get_pub(r)
    print(t1)
    print(t2)
    print(pub)
    if veri(t1,pub):
        x,k = solve_share_k(t1, t2, pub)
        print x,k
        transaction = sign("FLAG", pub, x, k)
        print str(transaction[0]), str(transaction[1])
        r.sendline(str(2))
        r.recv()
        r.sendline(str(transaction[0]))
        r.recv()
        r.sendline(str(transaction[1]))
    else:
        print "Only support SHA1 for now!!!"
    r.interactive()
    
    

if __name__ == "__main__":
    main()
