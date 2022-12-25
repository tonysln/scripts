#!/usr/bin/python

from sys import argv, exit


def bti(b, o='big'):
    """Byte to int"""
    i = 0
    brange = b if o == 'big' else reversed(b)
    for _b in brange:
        i <<= 8
        i |= _b
    return i
    
    
def itb(i, n=8, o='big'):
    """Int to byte"""
    if n < 0:
        n = (i.bit_length() + 7) // 8 

    b = []
    for _ in range(n):
        idx = 0 if o == 'big' else len(b)
        b.insert(idx, bytes([i & 0b11111111]))
        i >>= 8
    return b''.join(b)


if __name__ == '__main__':
    if len(argv) < 3:
        print('Usage: ./bconvert.py <itb or bti> <int or bytes> [-o byteorder] [-n length]')
        exit(1)

    argv = argv[1:]
    order = 'big'
    if '-o' in argv:
        order = argv[argv.index('-o') + 1]
    length = 8
    if '-n' in argv:
        length = int(argv[argv.index('-n') + 1])

    if argv[0] == 'itb':
        out = itb(int(argv[1]), n=length, o=order)
    elif argv[0] == 'bti':
        print('Awaiting proper implementation :-)')
        exit(2)
    else:
        print('Unknown command!')
        exit(3)

    print(out)
