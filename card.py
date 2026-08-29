#!/usr/bin/env python3
import random


def match(a, b, rA, rB, n=3):
    t = [not a, a, True, b, not b]
    N = len(t)
    rA %= N
    rB %= N
    t = t[rA:] + t[:rA]
    t = t[rB:] + t[:rB]
    return any(all(t[(i+j) % N] for j in range(n)) for i in range(N))

a = [1]
b = [1]

a += [not a[0]]
b += [not b[0]]

table = [not _a for _a in a] + [1] + b

N = len(table)
rotA = random.randint(0, N-1) % N 
rotB = random.randint(0, N-1) % N 

table = table[rotA:] + table[:rotA]
table = table[rotB:] + table[:rotB]

n = 3 
flag = any(all(table[(i + j) % N] for j in range(n)) for i in range(N))

print(table)
print(flag, match(a[0], b[0], rotA, rotB))
