def diagdet(M):
    return sum(M[i][i] for i in range(len(M)))


def det(M, sign=1):
    """
    Compute the determinant of matrix M using the Dodgson condensation method.
    https://www.gutenberg.org/files/37354/37354-pdf.pdf
    """

    step = 0
    A = [M]

    while step < len(M) * len(M[0]):
        rows = len(A[step][0])-1
        cols = len(A[step])-1

        if rows <= 0 or cols <= 0:
            break

        # Cycle rows and try from scratch if zero elements found
        for i in range(1, cols):
            for j in range(1, rows):
                if A[step][i][j] == 0:
                    # NB: still iffy about this, best to fallback to Gauss if zero detected
                    M_new = A[0][:i+step] + A[0][i+step+1:] + [A[0][i+step]]
                    return det(M_new, -sign)
        
        # New sub-matrix
        # TODO memoize and re-use if needed
        B = [[None]*cols for _ in range(rows)]
        for i in range(cols):
            for j in range(rows):
                B[i][j] = (A[step][i][j] * A[step][i+1][j+1]) - (A[step][i][j+1] * A[step][i+1][j])
                
                if step > 0:
                    B[i][j] = B[i][j] // A[step-1][i+1][j+1]

        A.append(B)
        step += 1

    return sign * A[-1][0][0]


print(det([[-2,-1,-1,-4],[-1,-2,-1,-6],[-1,-1,2,4],[2,1,-3,-8]]))
print(det([[3,1,4,1],[5,9,2,6],[0,7,1,0],[2,0,2,3]]))
print(det([[2,-1,2,1,-3], [1,2,1,-1,2], [1,-1,-2,-1,-1], [2,1,-1,-2,-1], [1,-2,-1,-1,2]]))
