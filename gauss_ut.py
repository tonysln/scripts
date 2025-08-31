#!/usr/bin/env python3

import numpy as np
from numpy import array

# Source: https://mathwiki.cs.ut.ee/linear_algebra/03_gaussian_elimination
# Updated for py3
 

def cmp(a, b):
    return bool(a > b) - bool(a < b)


def swap_rows(M, i, j):                              # function for swapping rows i and j
    if i > len(M) or j > len(M):               
        raise ValueError('The rows do not exist')
    else:
        R = M                                    
        R[[i,j],:] = R[[j,i],:]                  

    return R                                               
 
def add_row_multiples(M, i, j, l, k):                # function for adding l times row i and k times row j
    if i > len(M) or j > len(M):               
        raise ValueError('The rows do not exist')
    else:
        R = M                                      
        R[i,:] = l*M[i,:] + k*M[j,:]              

    return R
 
def general_gaussian_step(M, i, j):                  # function for general gaussian step, row i and col j
    if i < 0 or i > len(M)-1 or j < 0 or j > len(M.T)-2:
        raise ValueError('No such step in this matrix')
 
    R = array(M) 
    if any(R[range(i,len(R)),j] != 0):
        s = i + 1
        while R[i,j] == 0 and s < len(R): 
            R = swap_rows(R, i, s)
            s = s + 1
            # print(R)

        for t in range(len(R)): 
            if R[t,j] != 0 and t != i:
                l = R[i,j]
                k = R[t,j]
                if cmp(l,0) != cmp(k,0):
                    R = add_row_multiples(R, t, i, abs(l), abs(k))
                else: 
                    R = add_row_multiples(R, t, i, l, -k)

                # print(R)
    return R
 
#############################################################################################################
 
def general_gaussian(M): 
    R = array(M)                                      # the result matrix
    i = 0                                             # row index
    j = 0                                             # column index
    while j < len(M.T)-1 and i < len(R):
        R = general_gaussian_step(R,i,j)              # general gaussian step for row i and column j
        if R[i,j] != 0: i = i+1                       # criteria for changing row index
        j = j+1                                       # in every step changes column index
 
 
    rowind = array(range(len(R)))                     # vector of row indexes in R
    R = R[(rowind < i) | (R[:,len(R.T)-1] != 0),:]    # leaving out rows consisting only of zeros
    # print(R)
 
    if all(R[len(R)-1,range(len(R.T)-1)] == 0):     # enough to check the last row for contradiction
        raise ValueError('The system has no solution')
 

    R = R.astype(float)                              
    t = 0                                             # row index
    s = 0                                             # column index
    while s < len(R.T) and t < len(R):
        if R[t,s] != 0:                               # if the leading element is not zero
            R[t,:] = (float(1)/R[t,s])*R[t,:]         # the leading el. one by mult. the row with the inverse 
            # print(R)
            t = t+1
        s = s+1
 

    if len(R) == len(R.T)-1:                          # precisely one solution, return the last column
        # print(R[:,len(R.T)-1])
        return R[:,len(R.T)-1]
    else:
        print('The system has more then one solution')
        S = [0]*(len(R.T)-1)                          # we take the free variables equal to 0
        for m in range(len(R)):
            for n in range(len(R.T)):
                if R[m,n] == 1:                       #if leading el., the variable equals to constant term 
                    S[n] = R[m,len(R.T)-1]
                    break
        print('One of the solutions is', S)
        return


# M = array([[0,1,-10,0],[3,-1,-5,9],[-2,1,3,-6]]) 
# general_gaussian(M)
