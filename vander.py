#!/usr/bin/env python3

from gauss_ut import general_gaussian
import numpy as np


def inter_poly(points):
	x = points[:,0]
	V = np.vander(x, increasing=False)
	y = points[:,1]

	yt = np.array([y]).T
	Vv = np.concatenate((V, yt), axis=1)

	a = general_gaussian(Vv)
	return a


def print_polynomial(points):
	coef = inter_poly(points)
	deg = coef.size
	# print(coef, deg)

	res = ''
	for i,p in enumerate(coef):
		t = []
		if i > 0:
			t.append(' ' if p < 0 else ' + ')
		else:
			t.append('')

		if p > 1 or p < -1:
			t.append(f'{int(p)}')
		elif p == -1:
			t.append('-')
		elif i == deg-1:
			t[0] = ''

		c = deg-i-1
		if c > 1:
			t.append(f'x^{c}')
		elif c == 1:
			t.append('x')

		res += ''.join(t)

	res = f'p(x) = {res}'
	# print(res)
	return res


test = [([[1,-6], [2,2], [4,12]], 'p(x) = -x^2 + 11x -16'),
		([[1,-6], [2,2], [4,12], [3,-10]], 'p(x) = 9x^3 -64x^2 + 137x -88'),
		([[0,6], [1,5], [2,6]], 'p(x) = x^2 -2x + 6'),
		([[0,5], [1,10], [2,17]], 'p(x) = x^2 + 4x + 5'),
		([[0,0], [1,1], [2,8], [3,27]], 'p(x) = x^3 + x^2 + x')]

for i,(u,v) in enumerate(test):
	res = print_polynomial(np.array(u, dtype=float))
	print(f'{i+1}\t{res.ljust(50, " ")}{res == v}')
