import sys
import ctypes
sys.path.append('build/lib.linux-x86_64-2.7/')
def gen_num_from_state(state_num):
    tmp = ctypes.c_uint32(state_num).value
    print bin(tmp)
    tmp ^= (tmp >> 11)
    print bin(tmp)
    tmp ^= ctypes.c_uint32(tmp << 7).value & 0x9d2c5680
    print bin(tmp)
    tmp ^= ctypes.c_uint32(tmp << 15).value & 0xefc60000
    print bin(tmp)
    print bin(tmp)
    tmp ^= (tmp >> 18)
    print bin(tmp)
    return tmp
def get_random_number(r):
    y = r
    y = y^(y>>11)
    y = y^((y<<7)&0x9D2C5680)
    y = y^((y<<15)&0xEFC60000)
    y = y^(y>>18)
    return int_32(y)
def int_32(number):
    return int(0xFFFFFFFF & number)
a = int('afd9475c',16)
import revers_state
x = ctypes.c_uint32(revers_state.revers(a)).value
x = revers_state.revers(a)
print x
y = get_random_number(x)
print '{0:0{1}x}'.format(y, 8)
