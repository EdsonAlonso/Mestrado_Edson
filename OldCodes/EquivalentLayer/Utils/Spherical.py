from Mestrado.EquivalentLayer.Utils.Mag import delta_mag
import numpy as np

def distance( p1, p2 ):

    if len( np.shape( p1 ) ) > 1:
        r1, theta1, phi1 = p1[:, 0], p1[:, 1], p1[:, 2]
        r2, theta2, phi2 = p2[0], p2[1], p2[2]

        factor1 = r1 ** 2 + r2 ** 2
        factor2 = 2 * r1 * r2
    else:
        r1, theta1, phi1 = p1[0], p1[1], p1[2]
        r2, theta2, phi2 = p2[0], p2[1], p2[2]

        factor1 = r1 ** 2 + r2 ** 2
        factor2 = 2 * r1 * r2

    d = factor1 - factor2 * delta_mag(p1, p2)

    return np.sqrt(d)
