#!/usr/bin/python


def simplex(nb_vars, b_vars, A, b, log=True):
	"""Simplex method solver
	
	Help used:
		- https://sites.oxy.edu/lengyel/M372/xxx%20oldSTUFF/chap04.pdf
	"""

	# Join all variables
	vars = nb_vars[:] + b_vars[:]
	C_b = b_vars[:]
	z_j = [0.0]*len(vars)
	# Final coefficient
	ans = sum([c*b_ for c,b_ in zip(C_b, b)])
	# Diff between variables and z_j
	cj_zj = [v-z for v,z in zip(vars,z_j)]

	if log:
		print('>> Iteration 0:')
		print(cj_zj, ans, b)

	iter = 0
	while iter < 1000 and any(e > 0 for e in cj_zj):
		iter += 1

		# Pivot column
		pcol = cj_zj.index(max(cj_zj))
		if all(row[pcol] < 0 for row in A):
			# All pivot column elements are negative
			print('~~ NB! Problem is unbounded! ~~')
			return (None,[],[])

		ratios = [b_ / A[i][pcol] for i,b_ in enumerate(b)]
		# Pivot row
		prow = 0
		for i,r in enumerate(ratios):
			if r >= 0 and r < ratios[prow]:
				prow = i

		pivot = A[prow][pcol]
		if log:
			print(f'Pivot: ({pcol}, {prow}) -> {pivot}')

		# Next iteration
		C_b[prow] = vars[pcol]*1.0
		
		# Update pivot row (set col to 1) and b.
		# Use this new pivot row in next step
		for i,v in enumerate(A[prow]):
			A[prow][i] *= 1.0/pivot

		b[prow] *= 1.0/pivot

		# Update other rows (set col to 0) and b.
		for i,row in enumerate(A):
			if i == prow:
				continue

			pcoef = row[pcol]

			# Calculate all remaining rows
			for j,v in enumerate(row):
				A[i][j] -= pcoef * A[prow][j]*1.0

			b[i] -= pcoef * b[prow]*1.0

		# Recalculate bottom rows
		z_j = [sum(cb_*A[j][i] for j,cb_ in enumerate(C_b)) for i,_ in enumerate(vars)]
		ans = sum([c*b_ for c,b_ in zip(C_b, b)])
		cj_zj = [v-z for v,z in zip(vars,z_j)]

		if log:
			print(f'\n>> Iteration {iter}:')
			for c_,row,b_ in zip(C_b,A,b):
				print(round(c_,1), [round(el,1) for el in row], round(b_,1))
			print([round(el,1) for el in z_j], ans)
			print([round(el,1) for el in cj_zj])

	# TODO detect in a proper way
	if iter >= 999:
		print('~~ NB! Problem is unbounded! ~~')
		return (None,[],[])

	return (ans,b,C_b)


if __name__ == '__main__':
	print('== CASE 1', '='*60)
	nb_vars = [2, 1, -1]
	b_vars  = [0, 0, 0]
	b 		= [4, 3, 1]
	A 		= [[1, 2, 0, 1, 0, 0], 
		 	  [1, 1, 1, 0, 1, 0], 
		 	  [1, -1, 0, 0, 0, 1]]

	ans,b,C_b = simplex(nb_vars, b_vars, A, b, log=False)
	print('\n>>>> Output:') 
	print(f'ANS = {ans}\nB   = {b}\nC_b = {C_b}')

	
	print('\n== CASE 2', '='*60)
	nb_vars = [12, 18, 10]
	b_vars  = [0, 0, 0]
	b 		= [50, 0, 0]
	A 		= [[2, 3, 4, 1, 0, 0], 
		 	  [-1, 1, 1, 0, 1, 0], 
		 	  [0, -1, 1.5, 0, 0, 1]]

	ans,b,C_b = simplex(nb_vars, b_vars, A, b, log=False)
	print('\n>>>> Output:') 
	print(f'ANS = {ans}\nB   = {b}\nC_b = {C_b}')

