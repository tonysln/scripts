#! /usr/bin/python3


ts = 'THE.MAN.AND.THE.DOG.WAITED.AT.THE.STATION.FOR.THE.TRAIN.TO.THE.CITY'


def naive_BWT(s, start='^', end='$'):
    s = start + s + end
    ls = len(s)
    # All rotations
    rr = sorted([s[ls-i:] + s[:ls-i] for i in range(ls)], key=str.upper)
    # Last column
    return ''.join([c[-1] for c in rr])


def naive_IBWT(s, start='^', end='$'):
    ls = len(s)
    r = ['']*ls
    for i in range(ls):
        for ii in range(ls):
            r[ii] = s[ii] + r[ii]

        r = sorted(r, key=str.upper)

    # Find row that ends with 'end' char
    return r[[rr.endswith(end) for rr in r].index(True)].replace(start, '').replace(end, '')

 

print(naive_IBWT(naive_BWT(ts)))


def sort_cyclic_shifts(s):
    # https://cp-algorithms.com/string/suffix-array.html
    n = len(s)
    ab = 256

    p = [None]*n
    c = [None]*n
    cnt = [0]*max(ab, n)

    for i in range(0, n, 1):
        cnt[ord(s[i])] += 1

    for i in range(1, ab, 1):
        cnt[i] += cnt[i-1]

    for i in range(0, n, 1):
        cnt[ord(s[i])] -= 1
        p[cnt[ord(s[i])]] = i

    c[p[0]] = 0
    cc = 1
    for i in range(1, n, 1):
        if s[p[i]] != s[p[i-1]]:
            cc += 1

        c[p[i]] = cc-1

    pn = [None]*n
    cn = [None]*n

    h = 0
    while (1 << h) < n:
        h += 1

        for i in range(0, n, 1):
            pn[i] = p[i] - (1 << h)
            if pn[i] < 0:
                pn[i] += n

        cnt[0:cc] = [0]*cc

        for i in range(0, n, 1):
            cnt[c[pn[i]]] += 1

        for i in range(1, cc, 1):
            cnt[i] += cnt[i-1]

        for i in range(n-1, -1, -1):
            cnt[c[pn[i]]] -= 1
            p[cnt[c[pn[i]]]] = pn[i] if pn[i] >= 0 else pn[i]+n

        cn[p[0]] = 0
        cc = 1

        for i in range(1, n, 1):
            cur = (c[p[i]], c[(p[i] + (1 << h)) % n])
            prev = (c[p[i-1]], c[(p[i-1] + (1 << h)) % n])

            if cur != prev:
                cc += 1

            cn[p[i]] = cc-1

        c[:],cn[:] = cn[:],c[:]

    return p


def suffix_array(s, eof='$'):
    # s += eof
    ss = sort_cyclic_shifts(s)
    return ss[1:]


def BWT(s, eof='$'):
    # https://www.csbio.unc.edu/mcmillan/Comp555S18/Lecture13.pdf
    s += eof
    return ''.join(s[i-1] for i in suffix_array(s))


def IBWT(s, eof='$'):
    # https://www.csbio.unc.edu/mcmillan/Comp555S18/Lecture13.pdf
    table = ['' for c in s]
    for j in range(len(s)):
        table = sorted([c + table[i] for i,c in enumerate(s)])

    return table[s.index(eof)]


a = BWT(ts)
# a = BWT('mississippi')
print(a)
print(IBWT(a))
# print(naive_IBWT(a))
