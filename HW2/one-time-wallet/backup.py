from pwn import *

HOST = '140.112.31.96'
PORT = 10128
state = []
c = 0
def record_state(address, password):
    global c
    tmp_state = 0
    for i in range(len(address)/8):
        if c >= 624:
            c+=1
            continue
        else:
            tmp_state = int(address[i*8:(i+1)*8],16)
            state.append(tmp_state)
        c+=1
    for i in range(len(password)/8):
        if c >= 624:
            c+=1
            continue
        else:
            tmp_state = int(password[i*8:(i+1)*8],16)
            state.append(tmp_state)
        c+=1
    return

def next_state(n_state):
    for i in range(624):
        y = (n_state[i] & 0x80000000) 
        y+= (n_state[(i+1) % 624] & 0x7fffffff)
        ne = n_state[(i + 397) % 624]
        n_state[i] = ne ^ (y >>1)
        if y % 2:
            n_state[i] ^= 0x9908b0df
    return n_state

def gen_num_from_state(s,state_num):
    tmp = s[state_num]
    tmp ^= (tmp >> 11)
    tmp ^= (tmp << 7) & 0x9d2c5680
    tmp ^= (tmp << 15) & 0xefc60000
    tmp ^= (tmp >> 18)
    return tmp
def reverse_rshift_xor(y, shift):
    i = 0;
    # iterate over every bit-shifted section
    while (i * shift < 32):
        # Get bits to shift for bit section
        unshift = y & (((0xffffffff << (32 - shift)) & 0xffffffff) >> (shift * i))
        # Reverse right shift
        unshift = unshift >> shift
        # Reverse xor
        y ^= unshift
        i += 1
    return y

def reverse_lshift_xor(y, shift, mask):
    i = 0
    # iterate over every bit-shifted section
    while (i * shift < 32):
        # Git bits to shift for bit section
        unshift = y & (((0xffffffff >> (32 - shift))) << (shift * i))
        # Reverse left shift
        unshift = (unshift << shift)
        # Reverse mask
        unshift &= mask
        # Reverse xor
        y ^=  unshift
        i += 1
    return y

def backtrack(numbers):
    """
    Returns the current state of the MT PRNG based on list of 624 numbers
    """
    assert len(numbers) == 624
    n_state = []
    for n in numbers:
        n = reverse_rshift_xor(n, 18)               # reverse: y ^= (y >> 18)
        n = reverse_lshift_xor(n, 15, 0xefc60000)   # reverse: y ^= (y << 15) & 0xefc60000
        n = reverse_lshift_xor(n,  7, 0x9d2c5680)   # reverse: y ^= (y <<  7) & 0x9d2c5680
        n = reverse_rshift_xor(n, 11)               # reverse: y ^= (y >> 11)
        n_state.append(n)
    return n_state
def main():
    global c
    r = remote(HOST, PORT)
    for i in range(100):
        info = r.recvuntil('Address: ')
        address = r.recvline()[:-1]
        print info, address
        info = r.recvuntil('Password: ')
        password = r.recvline()[:-1]
        print info, password
        record_state(address, password)
    print len(state)
#    for i in range(624):
#        state[i] = revers_state.revers(state[i])
    
    n_state = backtrack(state)
    nstate = next_state(n_state)
    s = ''
    for i in range(3):
        s = '{0:0{1}x}'.format(gen_num_from_state(n_state, c%624), 8)
        c+=1
        print c,s
    s=''
    for i in range(5):
        rand = gen_num_from_state(n_state, c%624)
        s += '{0:0{1}x}'.format(rand, 8)
        c+=1
    info = r.recv()
    print info
    r.sendline(s)
    r.interactive()

if __name__ == "__main__":
    main()
