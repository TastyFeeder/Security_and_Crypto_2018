import base64
import sys
import os
import time
import string
import hashlib
digs = string.digits + string.letters
def int2base(x, base):
  if x < 0: sign = -1
  elif x == 0: return digs[0]
  else: sign = 1
  x *= sign
  digits = []
  while x:
    digits.append(digs[x % base])
    x /= base
  if sign < 0:
    digits.append('-')
  digits.reverse()
  return ''.join(digits)
PORT = 10127
HOSTNAME = '140.112.31.96'
from pwn import *
context(arch = 'i386', os = 'linux')
p = 262603487816194488181258352326988232210376591996146252542919605878805005469693782312718749915099841408908446760404481236646436295067318626356598442952156854984209550714670817589388406059285064542905718710475775121565983586780136825600264380868770029680925618588391997934473191054590812256197806034618157751903

pwr = [None]*3
#pwr = [16, 15, 7, 17, 16, 1, 4, 16, 8, 9, 20, 11, 8, 8, 13, 14]
for pw in range(3):
	if pwr[pw] != None:
		continue
	for i in range(1,21):
		r1 = remote(HOSTNAME, PORT)
		r2 = remote(HOSTNAME, PORT)
		num1 = None
		num2 = None
		for ro in range(3):
			t1 = r1.recvuntil('Server sends: ',drop=True)
			print t1
			t2 = r2.recvuntil('Server sends: ',drop=True)
			print t2
			data1 = r1.recvline()
			data2 = r2.recvline()
			#print 'data1--->',data1
			#print 'data2--->',data2
			r1.recv()
			r2.recv()
			g1 = int(data1)
			g2 = int(data2)
			if ro != pw:
				r1.sendline(str(g2))
				r2.sendline(str(g1))
			else:
				x = pow(int(hashlib.sha512(str(i)).hexdigest(), 16),2,p)
				r1.sendline(str(x))
				r2.sendline(str(x))
				num1 = int(hashlib.sha512(str(g1)).hexdigest(), 16)
				num2 = int(hashlib.sha512(str(g2)).hexdigest(), 16)
				#print 'inside job',num1,'<<>>',num2
		#print 'Hello',pw,i
#-------------------------------------------------
		r1.recvuntil('FLAG is: ',drop=True)
		#print 'FLAG1 is: '
		data1 = int(r1.recvline())
		#print data1
		r2.recvuntil('FLAG is: ',drop=True)
		#print 'FLAG2 is: '
		data2 = int(r2.recvline())
		#print data2
		r1.close()
		r2.close()
		#print data1,'<<>>',data2
		#print num1,'<<>>',num2
		if data1 ^ num1 == data2 ^ num2:
			print 'get password',pw,'-->',i
			pwr[pw] = i
			print pwr
			break 
print pwr

r = remote(HOSTNAME, PORT)
the_key = []
for i in range(3):
	r.recvuntil('Server sends: ',drop=True)
	data = r.recvline()
	g = int(data)
	the_key.append(g)
	num = pow(int(hashlib.sha512(str(pwr[i])).hexdigest(), 16),2,p)
	r.sendline(str(num))
r.recvuntil('FLAG is: ',drop=True)
data = int(r.recvline())
for x in the_key:
	num = int(hashlib.sha512(str(x)).hexdigest(), 16)
	data ^=num
r.close()
print 'FLAG is: '
st_r = int2base(int(data),16)
print st_r.decode('hex')
