import numpy as np
from Utils.Spherical import R_matrix, rij_vector

def magnetic_moment( theta, phi, intensity, declination, inclination ):
    """
    Docstring:
    Calculate the magnetic moment vector of a dipole based on its intensity, declination and inclination.

    :param theta: float
        Second axis value in a spherical coordinate system.
    :param phi: float
        Third axis value in a spherical coordinate system.
    :param intensity: float
        Intensity
    :param declination: float
        Declination
    :param inclination: float
        Inclination

    :return:
    magnetic_vector: array_like
        Magnetic moment vector in cartesian coordinates.

    """

    R = R_matrix( theta, phi )

    m = [ -np.sin( inclination ), -np.cos( inclination )*np.cos( declination ), np.cos( inclination )*np.sin(declination) ]

    magnetic_vector = intensity*np.dot( R, np.array( m ) )

    return magnetic_vector

def H_matrix( ri, rj, vi, vj ):
    """
    Docstring:
    Calculates the H matrix for computing the field from magnetization.

    :param ri: float
        First axis value in a spherical coordinate system for the observer.
    :param rj: float
        First axis value in a spherical coordinate system for the source.
    :param vi: python dictionary
        Dictionary where each key is one of the unit vectors in a spherical coordinate system for the observer.
        See funcntion unit_spherical_vectors
    :param vj: python dictionary
        Dictionary where each key is one of the unit vectors in a spherical coordinate system for the source.
        See funcntion unit_spherical_vectors

    :return:
    H: ndarray
        3x3 array for computing the field from magnetization.
    """

    coordenadas = [ 'r', 'theta', 'phi' ]

    rij = np.linalg.norm( rij_vector( ri, vi['r'], rj, vj['r'] ) )

    H_1, H_2 = np.empty( ( 3,3,) ),np.empty( ( 3,3,) )

    H1_linha = [ ( ri - rj*np.dot( vi['r'], vj['r'] ) ),
                 ( -rj*np.dot( vi['theta'], vj['r'] ) ),
                 ( -rj*np.dot( vi['phi'], vj['r'] ) ) ]

    H1_coluna = [ ( ri*np.dot( vi['r'], vj['r'] ) - rj ),
                  ( ri*np.dot( vi['r'], vj['theta'] ) ),
                  ( ri * np.dot( vi['r'], vj['phi'] ) ) ]

    for i in range( 3 ):
        for j in range( 3 ):
            H_1[ i ][ j ] = H1_linha[ i ]*H1_coluna[ j ]
            H_2[ i ][ j ] = np.dot( vi[ coordenadas[ i ] ], vj[ coordenadas[ j ] ] )

    H = ( 3*( 1/rij)**2 )*(H_1 - H_2)
    return H