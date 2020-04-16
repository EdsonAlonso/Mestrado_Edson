import numpy as np
import sys
sys.path.insert(0, '../')

def unit_spherical_vectors( theta, phi, mode = 'radians' ):
    """
    Docstring:
    Calculate the unit vectors in the spherical coordinate system in a dictionary format.

    Construct the unit_vectors dictionary where r,theta and phi are the keys.

    :param theta: float
        Second axis value in a spherical coordinate system.
    :param phi: float
        Third axis value in a spherical coordinate system.

    :return:
    unit_vectors: python dictionary
        A dictionary containing the 3 unitary vectors in the spherical coordinate system.
        Keys: r, theta and phi.

    """

    if mode == 'degree':
        theta,phi = np.radians( theta ), np.radians( phi )

    r_hat = [ np.sin( theta )*np.cos( phi ), np.sin( theta)*np.sin( phi ), np.cos( theta ) ]

    theta_hat = [ np.cos( theta )*np.cos( phi ), np.cos( theta)*np.sin( phi ), -np.sin( theta ) ]

    phi_hat = [ -np.sin( phi ), np.cos( phi ), 0 ]

    unit_vectors = { 'r': np.array( r_hat ), 'theta': np.array( theta_hat ), 'phi': np.array( phi_hat ) }

    return unit_vectors


def inverse_distance_function( ri, rj, mode = 'radians' ):
    """
    Calculates the inverse distance function between two vectors, ri and rj.
    Its mathematics is
    \frac{1}{rij} = \frac{1}{sqrt{ (r_i)^2 + (r_j)^2 + 2r_ir_j\mu_{ij} } }

    :param ri: array_like
        First vector.
    :param rj: array_like
        Second vector.
    :param mode: string
        String meaning the unit system used for the angles, i.e., degrees or radians.
    :return:


    """

    muij = np.dot( unit_spherical_vectors( ri[ 1 ], ri[ 2 ], mode=mode)['r'], unit_spherical_vectors( rj[ 1 ], rj[ 2 ], mode=mode)['r']  )

    rij = np.sqrt( ri[ 0 ]**2 + rj[ 0 ]**2 - 2*ri[ 0 ]*rj[ 0 ]*muij )

    return 1/rij


def rij_vector( ri, rj, mode = 'radians' ):
    """
    Docstring:
    Calculates the difference between ri and rj vectors in a spherical coordinate system.

    :param ri: float
        First axis valuee in a spherical coordinate system for the observer.
    :param ri_hat: array_like
        Unitary vector for the first axis in a spherical coordinate system for the observer.
    :param rj: float
        First axis valuee in a spherical coordinate system for the source.
    :param rj_hat: array_like
        Unitary vector for the first axis in a spherical coordinate system for the source.

    :return:
    rij: array_like
        An array meaning the difference between the vectors ri*ri_hat and rj*rj_hat.
    """

    Ri = ri[ 0 ]*unit_spherical_vectors( ri[ 1 ], ri[ 2 ] , mode )['r']
    Rj = rj[ 0 ]*unit_spherical_vectors( rj[ 1 ], rj[ 2 ] , mode )['r']

    rij = Ri - Rj

    return rij

def R_matrix( theta, phi, mode = 'radians'):
    """
    Docstring:
    Construct a matrix where each column is one of the unit vector in a spherical coordinate system.

    :param theta: float
        Second axis value in a spherical coordinate system.
    :param phi: float
        Third axis value in a spherical coordinate system.

    :return:
    R: Matrix
        A matrix where each column is one of the unitary vectors in a spherical coordinate system.

    """
    if mode == 'degree':
        theta, phi = np.radians( theta), np.radians( phi )

    R0 = [ np.sin(theta)*np.cos(phi), np.cos(theta)*np.cos(phi), -np.sin(phi) ]

    R1 = [ np.sin(theta)*np.sin(phi), np.cos(theta)*np.sin(phi), np.cos(phi) ]

    R2 = [ np.cos(theta), -np.sin(theta), 0 ]

    R = [ np.array( R0 ), np.array( R1 ), np.array( R2 ) ]

    return R


