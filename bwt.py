#! /usr/bin/python3


ts = 'THE.MAN.AND.THE.DOG.WAITED.AT.THE.STATION.FOR.THE.TRAIN.TO.THE.CITY'


def naive_BWT(s, start='^', end='$'):
    s = start + s + end
    ls = len(s)
    # All rotations
    rr = sorted([s[ls-i:] + s[:ls-i] for i in range(ls)], key=str.upper)
    # Last column
    return ''.join([c[-1] for c in rr])


def inverse_naive_BWT(s, start='^', end='$'):
    ls = len(s)
    r = ['']*ls
    for i in range(ls):
        for ii in range(ls):
            r[ii] = s[ii] + r[ii]

        r = sorted(r, key=str.upper)

    # Find row that ends with 'end' char
    return r[[rr.endswith(end) for rr in r].index(True)].replace(start, '').replace(end, '')

 

print(inverse_naive_BWT(naive_BWT(ts)))

def BWT(s, eof='\0'):
    s = s + eof
    return s


def inverse_BWT(s, eof='\0'):
    return s


print(inverse_BWT(BWT(ts)))
