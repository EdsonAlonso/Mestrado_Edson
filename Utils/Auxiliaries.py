import numpy as np

def generate_random( min, max, size ):

    random = np.empty( size )
    if isinstance( size, ( tuple ) ):
        for i in range( size [ 0 ] ):
            for j in range( size[ 1 ] ):
                random[ i ] = ( 1 - np.random.random( ) )*min + np.random.random( )*max
    else:
        for i in range( size ):
            t = np.random.random( )
            random[ i ] = (1 - t )*min + t*max

    return random