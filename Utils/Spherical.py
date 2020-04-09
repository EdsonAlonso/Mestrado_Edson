import numpy as np

def unit_spherical_vectors( theta, phi ):
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

    r_hat = [ np.sin( theta )*np.cos( phi ), np.sin( theta)*np.sin( phi ), np.cos( theta ) ]

    theta_hat = [ np.cos( theta )*np.cos( phi ), np.cos( theta)*np.sin( phi ), -np.sin( theta ) ]

    phi_hat = [ -np.sin( phi ), np.cos( phi ), 0 ]

    unit_vectors = { 'r': np.array( r_hat ), 'theta': np.array( theta_hat ), 'phi': np.array( phi_hat ) }

    return unit_vectors

def rij_vector( ri, ri_hat, rj, rj_hat ):
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

    Ri = ri*ri_hat

    Rj = rj*rj_hat

    rij = Ri - Rj

    return rij

def R_matrix( theta, phi ):
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

    R0 = [ np.sin(theta)*np.cos(phi), np.cos(theta)*np.cos(phi), -np.sin(phi) ]

    R1 = [ np.sin(theta)*np.sin(phi), np.cos(theta)*np.sin(phi), np.cos(phi) ]

    R2 = [ np.cos(theta), -np.sin(theta), 0 ]

    R = [ np.array( R0 ), np.array( R1 ), np.array( R2 ) ]

    return R
