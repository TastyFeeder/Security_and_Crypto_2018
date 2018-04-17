from pwn import *
import string
import time
import gmpy
from langdetect import detect_langs
import base64
FLAG_P = []
def start(r):
    get = r.recvuntil("m1 = ")
    print(get)
    ans = r.recvline()
    print(ans)
    get = r.recvuntil("Your answer:")
    r.send(ans)

def crpto1(r):
    get = r.recvuntil("c1 = ")
    print(get)
    c = r.recvline()
    print(c)
    get = r.recvuntil("Your answer:")
    print(get)
    dic = string.ascii_lowercase
    c = c.split(' ')
    m = ''
    for s in c:
        for i in range(len(s)/2): # len(s) should be even
            m += dic[int(s[2*i:2*i+2])-1]
        m+= ' '
    print(m[:-1])
    r.send(m[:-1]+'\n')

def crpto2(r):
    get = r.recvuntil('m1 = ')
    print(get)
    m1 = r.recvline()
    print(m1)
    get = r.recvuntil('c1 = ')
    print(get)
    c1 = r.recvline()
    print(c1)
    get = r.recvuntil('c2 = ')
    print(get)
    c2 = r.recvline()
    print(c2)
    low = string.ascii_lowercase
    upper = string.ascii_uppercase
    diff = ord(m1[0]) - ord(c1[0])
    m2 = ''
    for c in c2:
        if c in low:
#            print(ord(c)- 97 - diff)
            m2+=low[(ord(c)- 97 + diff)%26]
        if c in upper:
            m2+=upper[(ord(c)- 97 + diff)%26]
        elif c == ' ':
            m2+= ' '
        else:
            continue
    print(m2)
    get = r.recvuntil("Your answer:")
    r.send(m2+'\n')

def crpto3(r):
    get = r.recvuntil("c1 = ")
    print get
    c1 = r.recvline()
    print("c1:",c1)
    get = r.recvuntil("Your answer:")
    low = string.ascii_lowercase
    upper = string.ascii_uppercase
    option = []
    for diff in range(26):
        m = ''
        for c in c1:
            if c in low:
                m+=low[(ord(c)- 97 + diff)%26]
            if c in upper:
                m+=upper[(ord(c)- 97 + diff)%26]
            elif c == ' ':
                m+= ' '
            else:
                continue
        option.append(m)
        print(diff, m)
#    opt = int(raw_input("Give me ans\n"))
    ans = 0
    for opt in range(len(option)):
        if detect_langs(option[opt])[0].lang == 'en' and detect_langs(option[opt])[0].prob > 0.9:
            ans = opt

    print option[ans]
    r.send(option[ans]+"\n")

def crpto4(r):
    get = r.recvuntil('m1 = ')
    print(get)
    m1 = r.recvline()
    print(m1)
    get = r.recvuntil('c1 = ')
    print(get)
    c1 = r.recvline()
    print(c1)
    get = r.recvuntil('c2 = ')
    print(get)
    c2 = r.recvline()
    print(c2)
    low = string.ascii_lowercase
    upper = string.ascii_uppercase
    m1 = m1.lower()
    c1 = c1.lower()
    dic = {}
    m = ''
    a = 0
    i = 1
    while a ==0:
        if c1[i] != ' ':
            y_diff = (ord(c1[i]) - ord(c1[0]))
            x_diff = (ord(m1[i]) - ord(m1[0]))
            print x_diff, y_diff
            a = gmpy.invert(x_diff, 26) * y_diff % 26
            b = (ord(c1[0]) - 97 - a * (ord(m1[0])- 97)) % 26
            i+=1
    a_inv = gmpy.invert(a, 26)
    print a , b
    def rev(a_inv, b, c):
        return chr(97 + ((c - b) * a_inv % 26))

    for c in c2 :
        if c in low:
            m+=rev(a_inv, b, ord(c) - 97).lower()
        elif c in upper:
            m+=rev(a_inv, b, ord(c) - 97).upper()
        elif c == ' ':
            m+= ' '
        else:
            continue
    get = r.recvuntil("Your answer:")
    print("m==>",m)
    r.send(m + '\n')

def gcd(a,b):
    if a < b:
        tmp = a
        a = b
        b = a
    if b == 0:
        return a
    else:
        return gcd(b, a%b)

def crpto5(r):
    get = r.recvuntil('m1 = ')
    print(get)
    m1 = r.recvline()
    print(m1)
    get = r.recvuntil('c1 = ')
    print(get)
    c1 = r.recvline()
    print(c1)
    get = r.recvuntil('c2 = ')
    print(get)
    c2 = r.recvline()[:-1]
    print(c2)
    low = string.ascii_lowercase
    upper = string.ascii_uppercase
    m2 = []
    for i in range(len(c2)):
        m2.append('*')
    off = []
    for i in range(len(c2)):
        if c1[i] == m1[1]:
            off = i
            if m1[2] == c1[(off * 2)%len(c2)]:
                break
#            if gcd(len(c2), off):
#                break
#    tmp = list(c2)
    for i in range(len(m2)):
        m2[i] = c2[(off * i)%len(c2) ]
    print(off, len(c2) ,"m==>",m2)
    get = r.recvuntil("Your answer:")
    print("m==>",''.join(m2))
    r.send(''.join(m2) + "\n")

def crpto6(r):
    get = r.recvuntil('m1 = ')
    print(get)
    m1 = r.recvline()[:-1]
    print(m1)
    get = r.recvuntil('c1 = ')
    print(get)
    c1 = r.recvline()[:-1]
    print(c1)
    get = r.recvuntil('c2 = ')
    print(get)
    c2 = r.recvline()[:-1]
    print(c2)
    low = string.ascii_lowercase
    upper = string.ascii_uppercase
    blocksize = 1
    for i in range(len(c1)):
        if c1[1] == m1[i]:
            blocksize = i
            if c1[2] == m1[2*blocksize]:
                break
    print "blocksize", blocksize
    m2 = []
    for i in range(len(c2)/blocksize):
        tmp = []
        for j in range(blocksize):
            tmp.append("*")
        m2.append(tmp)
    tmp = []
    for i in range(len(c2) - (len(c2)/blocksize) * blocksize):
        tmp.append("*")
    m2.append(tmp)
    try:
        m2.remove([]) 
    except:
        pass
    x = 0
    y = 0
    head = True
    row_number = len(c2)/blocksize
    block_len = len(m2[0])
    print row_number
    step = 0
    coun = 0
    for c in c2:
        if step == 0:
            if x > row_number:
                x = 0
                y +=1
                step = 1
            else:
                m2[x][y] = c
                x+=1
                coun+=1
        if step == 1:
            if head == True:
                try:
                    m2[x][y] = c
                    head = False
                    coun+=1
                except:
                    x = 0
                    head = True
                    y+=1
                    m2[x][y] = c
                    head = False
                    coun+=1
            else:#if head == False:
                try:
                    if y >= blocksize/2:
                        x+=1
                    m2[x][block_len - y] = c
                    head = True
                    x+=1
                    coun+=1
                except:
                    x = 0
                    head = True
                    y+=1
                    m2[x][y] = c
                    head = False
                    coun+=1
        print "step", step, x, y, head#,m2
        final_m = []
        for i in m2:
            final_m +=i
        print("m==>",''.join(final_m))


    get = r.recvuntil("Your answer:")
    print(m2)
    final_m = []
    for i in m2:
        final_m +=i
    print(blocksize, "m==>",''.join(final_m))
    r.send(''.join(final_m) + "\n")
    

def collect_pieces(r):
    time.sleep(0.3)
    get = r.recvuntil("FLAG_PIECES: ")
    piece = r.recvline()
    FLAG_P.append(piece[:-1])

if __name__ == '__main__':
    HOST = '140.112.31.96'
    PORT = 10120
    r = remote(HOST, PORT)
    start(r)
    crpto1(r)
    collect_pieces(r)
    crpto2(r)
    collect_pieces(r)
    crpto3(r)
    collect_pieces(r)
    crpto4(r)
    collect_pieces(r)
    crpto5(r)
    collect_pieces(r)
    crpto6(r)
    collect_pieces(r)
    print(FLAG_P)
    print "".join(FLAG_P)
    PNG = base64.b64decode("".join(FLAG_P))
    with open('flag.png','w') as f:
        f.write(PNG)
    r.interactive()
    
