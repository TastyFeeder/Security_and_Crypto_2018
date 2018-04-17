from pwn import *
import string
import hashlib
import random

host = "140.112.31.96"
port = 10121
r = remote(host, port)
print(":QAQ")
get = r.recvuntil("Your input size should be smaller than 400 bytes.")
suffix =  r.recv()
suffix = suffix.split('=')[-1][:-1][-6:]
print(suffix)
fo1 = open('1.pdf','rb').read()[:320]
fo2 = open('2.pdf','rb').read()[:320]
S = 'tastyfeeder_sha1_test'
c =0
while(True):
    S_test = S
    for i in range(16):
        S_test += random.choice(string.letters)
    m = hashlib.sha1()
    m.update(fo1+S_test)
    shone = m.digest().encode('hex')
    c+=1
    if  c % 10000 == 0:
        print("Target is {} ,now try {}\n we have try {} times".format(suffix,shone,c))
#    print 'Now trying:',shone
    if shone.endswith(suffix):
        S = S_test
        break
r.sendline((fo1+S).encode('hex'))
r.recv()
r.sendline((fo2+S).encode('hex'))
r.interactive()
