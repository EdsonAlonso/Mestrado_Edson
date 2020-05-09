import numpy as np
import sys
sys.path.insert(0,'../')
from Utils.Parsers import check_size
from Utils.Spherical import R_matrix, rij_vector, unit_spherical_vectors, inverse_distance_function

def magnetic_moment( theta, phi, intensity, declination, inclination, mode = 'radians' ):
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
    if mode == 'degree':
        theta, phi = np.radians( theta ), np.radians( phi )
        inclination, declination = np.radians( inclination ), np.radians( declination )

    R = R_matrix( theta, phi )

    m = [ -np.sin( inclination ), -np.cos( inclination )*np.cos( declination ), np.cos( inclination )*np.sin(declination) ]

    magnetic_vector = intensity*np.dot( R, np.array( m ) )

    return m

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
    H = 3*(H_1 - H_2)
    return H

def magnetic_potential( dipole_pos, inclination, declination, observers_pos, mode = 'radians' ):
    """
    Dcostring:
    Calculates the magnetic potential produced by a unitary dipole source.

    :param dipole_pos: array_like
        Array like [r, theta, phi] meaning the position of a dipole in a spherical coordinate system.
    :param inclination: float
        Inclination.
    :param declination: float
        Declination.
    :param observer_pos: matrix_like
        Matrix like [ [r1,theta1,phi1], ..., [r1,theta1,phi1] ] meaning the position of the observers in a geocentric spherical coordinate system.

    :return:
    psi: Array_like
        Magnetic potential caused by the dipole sources.
    """

    m04pi = 1e-7

    psi = [ ]

    mj = magnetic_moment( dipole_pos[ 1 ], dipole_pos[ 2 ], 1, declination, inclination, mode = mode )

    vj = unit_spherical_vectors( dipole_pos[ 1 ], dipole_pos[ 2 ], mode = mode )

    observers_pos = check_size( observers_pos )

    for observer_pos in observers_pos:
        vi = unit_spherical_vectors( observer_pos[ 1 ], observer_pos[ 2 ], mode = mode)


        inverse_rij = inverse_distance_function( observer_pos, dipole_pos, mode = mode )

        muij = np.dot( vi['r'], vj['r'])
        deltartheta = np.dot( vi['r'], vj['theta'])
        deltarphi = np.dot( vi['r'], vj['phi'])

        mjrij = ( mj[0]*( observer_pos[0]*muij - dipole_pos[0] ) + mj[1]*observer_pos[0]*deltartheta + mj[2]*observer_pos[0]*deltarphi )

        psi.append( m04pi*( inverse_rij**3 )*mjrij )

    return np.array( psi )
