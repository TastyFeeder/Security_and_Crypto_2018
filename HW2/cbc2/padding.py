import base64
import sys
from pwn import *
import time
PORT = 10125
HOSTNAME = '140.112.31.96'
#PORT = 8000
#HOSTNAME = "127.0.0.1"
#init socket
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect(( HOSTNAME, PORT ))
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[:-ord(s[-1])]


flag = ''
key = []
#Implementation of oracle padding for 1 block(16 byte)
def read_menu(r):
    data=r.recvuntil('> ')
    print data
    return
# decrypt option
def opt1(r, index):
    global flag
    r.sendline('1')
    r.recvuntil('IV:\n')
    IV = r.recvline()[:-1]
    print repr(IV)
    r.recvuntil('Encrypted_FLAG:\n')
    e_FLAG = r.recvline()[:-1]
    block = len(e_FLAG.decode('hex')) /16
    print repr(block)
    print repr(e_FLAG)
    e_FLAG = e_FLAG.decode('hex')
    assert(len(IV)==16)
    cipher = IV+e_FLAG
    print repr(cipher) ,len(cipher)
    r.recv()
    if index >block:
        print flag
        exit()
    # start padding oracle attack
    block_plain_text = []
    for j in range(BS):
        block_plain_text.append(padding(r,j+1,cipher[index*BS:],block_plain_text))
        print block_plain_text
        #if j >=2:
        #    exit()
    s = ''.join(chr(x) for x in block_plain_text[::-1])
    print s
    flag+=s
    print flag
    r.close()

def padding(r, pad_n, tar_block, plain):
    iv = tar_block[:16]
    block = tar_block[16:32]
    guess = 0
    while True:
        if guess>=256:
            guess-=1
            print 'padding fail cause no pad fit record as 255'
            print '<==>', chr(guess)
            return guess
        xor = []
        for i in range(BS - pad_n):
            xor.append(iv[i])
#            xor.append('\x00')
        xor.append(chr(guess ^ pad_n ^ ord(iv[-1 * pad_n])))
        for i in range(1, pad_n):
            #print i, pad_n, plain[0-i], iv[0-pad_n+i], iv, 0-pad_n+i
            xor.append(chr(plain[0-i] ^ pad_n ^ ord(iv[0-pad_n+i])))
        #print len(xor)
        to_send = ''.join(xor) + block
        to_send = to_send.encode('hex')
#send
        r.sendline(to_send)
        tmp=r.recvline().strip()
        #print pad_n, guess,len(to_send), repr(to_send[:32]), repr(tmp)
        if tmp.startswith('Fail'):
            guess+=1
#    print tmp_iv
        elif tmp.startswith('Success'):
            print "yoyoyo {}".format(guess)
            break
    print chr(guess), '<==>', guess, iv[-1 * pad_n], pad_n
    return guess

# do string xor (from stackoverflow)
def sxor(s1,s2):    
    return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))

# exploit script
def main():
    for i in range(4):
        r = remote(HOSTNAME,PORT)
        read_menu(r)
        opt1(r,i)
    pass

if __name__ == "__main__":
    main()
