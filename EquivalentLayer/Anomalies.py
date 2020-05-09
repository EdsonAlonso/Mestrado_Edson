import numpy as np
from time import time

def dircos( inc, dec ):

    # Calculates the projected cossine values
    A = -np.sin( inc )
    B = -np.cos( inc ) * np.cos( dec )
    C = np.cos( inc ) * np.sin( dec )

    # Return the final output
    return A, B, C

def delta_mag( observer, source ):
    theta, phi = observer[ :,1 ], observer[ :,2 ]
    theta1, phi1 = source[ 1 ], source[ 2 ]

    factor1 = np.cos( theta )*np.cos( theta1 )
    factor2 = np.sin( theta )*np.sin( theta1 )

    return factor1 + factor2*np.cos( phi - phi1 )

def distance( p1, p2 ):
    r1, theta1, phi1 = p1[ :,0 ], p1[ :,1 ], p1[ :,2 ]
    r2, theta2, phi2 = p2[ 0 ], p2[ 1 ], p2[ 2 ]

    factor1 = r1**2 + r2**2
    factor2 = 2*r1*r2

    d = factor1 - factor2*delta_mag( p1, p2 )

    return np.sqrt( d )

def Fr( inclination, declination, observers, source ):

    mr, mtheta, mphi = dircos( inclination, declination )
    observers = np.array( observers )

    r, theta, phi = observers[:,0], observers[:,1], observers[:,2]
    r1, theta1, phi1 = source[0], source[1], source[2]
    cos_delta = delta_mag(observers, source)

    A = r - r1 * cos_delta

    R = distance(observers, source)

    A1 = r1 - r * cos_delta
    B1 = r * (np.cos(theta) * np.sin(theta1) - np.cos(theta1) * np.sin(theta) * np.cos(phi - phi1))
    C1 = -r * np.sin(theta) * np.sin(phi - phi1)

    factor1 = (-1 / R ** 3)
    factor_r = (3 * A * A1 / R ** 2 + cos_delta)
    factor_theta = (3 * A * B1 / R ** 2 - B1 / r)
    factor_phi = (3 * A * C1 / R ** 2 - C1 / r)

    result = factor1 * (factor_r * mr + factor_theta * mtheta + factor_phi * mphi)

    return result

def Ftheta( inclination, declination, observers, source ):

    mr, mtheta, mphi = dircos( inclination, declination )
    observers = np.array( observers )

    r, theta, phi = observers[:,0], observers[:,1], observers[:,2]
    r1, theta1, phi1 = source[0], source[1], source[2]

    cos_delta = delta_mag( observers, source )

    B = r1*( np.sin( theta )*np.cos( theta1 ) - np.cos( theta )*np.sin( theta1 )*np.cos( phi - phi1 ) )

    R = distance( observers, source )

    A1 = r1 - r*cos_delta
    B1 = r*( np.cos( theta )*np.sin( theta1) - np.cos( theta1 )*np.sin( theta )*np.cos( phi - phi1 ) )
    C1 = -r*np.sin( theta )*np.sin( phi - phi1 )

    D = np.sin( theta )*np.sin( theta1 ) +np.cos( theta )*np.cos( theta1 )*np.cos( phi - phi1 )
    E = np.cos( theta )*np.sin( phi - phi1 )

    factor1 = ( -1/R**3 )
    factor_r = ( 3*B*A1/R**2 - B/r1  )
    factor_theta = ( 3*B*B1/R**2  + D  )
    factor_phi = ( 3*B*C1/R**2 + E  )

    result = factor1*( factor_r*mr + factor_theta*mtheta + factor_phi*mphi )

    return result

def Fphi( inclination, declination, observers, source ):

    mr, mtheta, mphi = dircos( inclination, declination )
    observers = np.array( observers )

    r, theta, phi = observers[:,0], observers[:,1], observers[:,2]
    r1, theta1, phi1 = source[0], source[1], source[2]

    cos_delta = delta_mag( observers, source )
    C = r1*np.sin( theta1 )*np.sin( phi - phi1 )

    R = distance( observers, source )

    A1 = r1 - r*cos_delta
    B1 = r*( np.cos( theta )*np.sin( theta1) - np.cos( theta1 )*np.sin( theta )*np.cos( phi - phi1 ) )
    C1 = -r*np.sin( theta )*np.sin( phi - phi1 )

    F = np.cos( theta1 )*np.sin( phi - phi1 )
    G = np.cos( phi - phi1 )

    factor1 = ( -1/R**3 )
    factor_r = ( 3*C*A1/R**2 - C/r1  )
    factor_theta = ( 3*C*B1/R**2  - F  )
    factor_phi = ( 3*C*C1/R**2 + G  )

    result = factor1*( factor_r*mr + factor_theta*mtheta + factor_phi*mphi )

    return  result
