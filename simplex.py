#!/usr/bin/python


def simplex(nb_vars, b_vars, A, b, log=True):
	"""Simplex method solver
	
	Sources used:
		- https://sites.oxy.edu/lengyel/M372/xxx%20oldSTUFF/chap04.pdf
	"""

	# All variables
	vars = nb_vars[:] + b_vars[:]
	# C_b
	C_b = b_vars[:]
	# Z_j
	z_j = [0]*len(vars)
	# Final coefficient
	ans = sum([c*b_ for c,b_ in zip(C_b, b)])
	# Diff between variables and z_j
	cj_zj = [v-z for v,z in zip(vars,z_j)]

	if log:
		print('>> Iteration 0:')
		print(cj_zj, ans, b)

	iter = 0
	while any(e > 0 for e in cj_zj):
		iter += 1

		# Pivot column
		pcol = cj_zj.index(max(cj_zj))
		ratios = [b_ / A[i][pcol] for i,b_ in enumerate(b)]
		# Pivot row
		prow = 0
		for i,r in enumerate(ratios):
			if r > 0 and r < ratios[prow]:
				prow = i

		pivot = A[prow][pcol]
		if log:
			print(f'Pivot: ({pcol}, {prow}) -> {pivot}')

		# Next iteration
		C_b[prow] = vars[pcol]

		# Update pivot row (set col to 1) and b.
		# Use this new pivot row in next step
		for v in A[prow]:
			v *= 1/pivot

		b[prow] *= 1/pivot

		# Update other rows (set col to 0) and b.
		for i,row in enumerate(A):
			if i == prow:
				continue

			# For each other row, check if pivot col value is neg or pos
			# TODO double-check factor choice
			for j,v in enumerate(row):
				pcoef = row[pcol]
				if pcoef < 0:
					A[i][j] += abs(pcoef) * A[prow][j]
					b[i] += abs(pcoef) * b[prow]
				else:
					A[i][j] -= pcoef * A[prow][j]
					b[i] -= pcoef * b[prow]
			
		# Recalculate bottom rows
		z_j = [sum(cb_*A[j][i] for j,cb_ in enumerate(C_b)) for i,v in enumerate(vars)]
		ans = sum([c*b_ for c,b_ in zip(C_b, b)])
		cj_zj = [v-z for v,z in zip(vars,z_j)]

		if log:
			print(f'\n>> Iteration {iter}:')
			for c_,row,b_ in zip(C_b,A,b):
				print(c_,row,b_)
			print(z_j)
			print(cj_zj, ans)

	return (ans,b,C_b)


if __name__ == '__main__':
	nb_vars = [2, 1, -1]
	b_vars = [0, 0, 0]
	b = [4, 3, 1]
	A = [[1, 2, 0, 1, 0, 0], 
		 [1, 1, 1, 0, 1, 0], 
		 [1, -1, 0, 0, 0, 1]]

	ans,b,C_b = simplex(nb_vars, b_vars, A, b)
	print('\n>>>> Output:') 
	print(f'ANS = {ans}\nB   = {b}\nC_b = {C_b}')

