import numpy as np

def delta_mag( observer, source ):
    if len( np.shape( observer ) ) > 1:
        theta, phi = observer[ :,1 ], observer[ :,2 ]
    else:
        theta, phi = observer[ 1 ], observer[ 2 ]

    theta1, phi1 = source[ 1 ], source[ 2 ]

    factor1 = np.cos( theta )*np.cos( theta1 )
    factor2 = np.sin( theta )*np.sin( theta1 )

    return factor1 + factor2*np.cos( phi - phi1 )

def magnetization( intensity, inclination, declination ):

    Mr = -np.sin( inclination )
    Mtheta = -np.cos( inclination ) * np.cos( declination )
    Mphi = np.cos( inclination ) * np.sin( declination )

    return intensity*np.array( [ Mr, Mtheta, Mphi ] )