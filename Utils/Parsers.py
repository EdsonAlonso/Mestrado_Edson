import numpy as np

def check_size( array ):
    invalid_types = [ float, None, int, bool ]
    valid_types = [ list, np.array ]
    if type( array ) in invalid_types:
        raise ValueError
    if type( array ) in valid_types:
        if len( np.shape( array ) ) == 1:
            return [ array ]
        else:
            return array
