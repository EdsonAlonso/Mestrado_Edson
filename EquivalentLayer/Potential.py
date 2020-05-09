import numpy as np


def dircos( inc, dec ):

    # Calculates the projected cossine values
    A = -np.sin( inc )
    B = -np.cos( inc ) * np.cos( dec )
    C = np.cos( inc ) * np.sin( dec )

    # Return the final output
    return A, B, C

def distance( p1, p2 ):
    r1, theta1, phi1 = p1[ :,0 ], p1[ 1 ], p1[ :,2 ]
    r2, theta2, phi2 = p2[ 0 ], p2[ 1 ], p2[ 2 ]

    factor1 = r1**2 + r2**2
    factor2 = 2*r1*r2

    d = factor1 - factor2*delta_mag( p1, p2 )

    return np.sqrt( d )

def delta_mag( observer, source ):
    theta, phi = observer[ :,1 ], observer[ :,2 ]
    theta1, phi1 = source[ 1 ], source[ 2 ]

    factor1 = np.cos( theta )*np.cos( theta1 )
    factor2 = np.sin( theta )*np.sin( theta1 )

    return factor1 + factor2*np.cos( phi - phi1 )


def Pot( inclination, declination, observers, source ):

    mr, mtheta, mphi = dircos( inclination, declination )
    observers = np.array( observers )

    r, theta, phi = observers[ :,0 ], observers[ :,1 ], observers[ :,2 ]
    r1, theta1, phi1 = source[ 0 ], source[ 1 ], source[ 2 ]

    cos_delta = delta_mag( observers, source )

    A1 = r1 - r*cos_delta
    B1 = r*( np.cos( theta )*np.sin( theta1) - np.cos( theta1 )*np.sin( theta )*np.cos( phi - phi1 ) )
    C1 = -r*np.sin( theta )*np.sin( phi - phi1 )

    R3 = distance( observers, source )**3

    result =  -( mr*A1 + mtheta*B1 + mphi*C1 )/R3

    return result


