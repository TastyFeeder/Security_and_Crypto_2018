
import gmpy
#gmpy.invert(e,n)
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m
txt = open("mersenne-rsa.txt", 'r').read().split('\n')
N = int(txt[0][4:])
e = int(txt[1][4:])
c = int(txt[2][7:])
#d = gmpy.invert()
# below is from factordb
p = (2**521)-1
q = (2**607)-1
print("N",N)
print("e",e)
print("c",c)
d = modinv(e, (p-1)*(q-1))
m = pow(c,d,N)
print "get p q from factordb:"
print("q is",q)
print("p is",p)
print("flag is: ")
print(str(hex(m))[2:-1].decode('hex'))
