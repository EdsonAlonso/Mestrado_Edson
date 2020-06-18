import numpy as np

def get_H_matrix( nrows, order ):

    H1 = np.eye( nrows )
    if order == 0:
        return H1

    H2 = 2*np.eye( nrows )

    H2[ 0, 0 ] = 1
    H2[ nrows - 1, nrows - 1 ] = 1

    for i in range( nrows ):
        for j in range( nrows ):
            if j == i + 1 or i == j + 1:
                H2[ i, j ] = - 1

    return H1 + H2

