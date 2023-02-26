#!/usr/bin/python

from math import pow, pi, e


def fft(a):
	n = len(a)
	if n == 1:
		return a

	a_e = [a[i] for i in range(0, n-2, 2)]
	a_o = [a[i] for i in range(1, n-1, 2)]
	y_e = fft(a_e)
	y_o = fft(a_o)
	w_n = pow(e, complex(2*pi).real/n)
	w = 1
	y = [None]*n
	for k in range(0, n/2-1):
		y[k] = y_e[k] + w*y_o[k]
		y[k+(n/2)] = y_e[k] - w*y_o[k]
		w = w*w_n

	return y


def ifft():
	return


if __name__ == '__main__':
	print(fft([0, 0, 0, 0]))
