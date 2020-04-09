import numpy as np
from Utils import unit_spherical_vectors, rij_vector, magnetic_moment, H_matrix

#TODO: O DIPOLO DEVE SER UM OOBJETO. AS FUNCOES DEVEM ESTAR ORIENTADAS A ELE

def Anomaly_Field( dipole_pos, inclination, declination, observer_pos ):
    """
    Dcostring:
    Calculates the Anomaly field produced by a unitary dipole source.

    :param dipole_pos: array_like
        Array like [r, theta, phi] meaning the position of a dipole in a spherical coordinate system.
    :param inclination: float
        Inclination.
    :param declination: float
        Declination.
    :param observer_pos: array_like
        Array like [r,theta,phi] meaning the position of a dipole in a spherical coordinate system.

    :return:
    A: array_like
        Anomaly field caused by the dipole source.
    """
    m04pi = 1 #Perguntar qual o valor desse negócio, que muda de sistema pra sistema
    vj = unit_spherical_vectors( dipole_pos[ 1 ], dipole_pos[ 2 ] )
    vi = unit_spherical_vectors( observer_pos[ 1 ], observer_pos[ 2 ] )

    rij = np.linalg.norm( rij_vector( observer_pos[ 0 ], vi['r'], dipole_pos[ 0 ], vj['r'] ) )

    m = magnetic_moment( dipole_pos[ 1 ], dipole_pos[ 2 ], 1, declination, inclination )

    H = H_matrix( observer_pos[ 0 ], dipole_pos[ 0 ], vi, vj )

    A = ( m04pi*(1/rij)**2 )*np.dot( H, m )

    return A

# if __name__ == "__main__":
#
#     ri, theta_i , phi_i = 2, 0, np.pi/2
#     rj, theta_j, phi_j = -5, np.pi/4, np.pi/2
#     incl, decl = np.pi, np.pi/6
#
#     dip_pos = [ rj, theta_j, phi_j ]
#     obs_pos = [ ri, theta_i, phi_i ]
#
#     A = Anomaly_Field( dip_pos, incl, decl, obs_pos )
#
#     print( A )