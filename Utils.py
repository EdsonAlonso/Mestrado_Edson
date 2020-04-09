import numpy as np

#TODO: UM SCRIPT PARA TODOS OS UTILS? DEVO SEPARAR EM PELO MENOS 2

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

def Carterian2Spherical( r, theta, phi ):
    """
    Docstring:
    Converts cartesian to spherical coordinates.
     
    :param r: float
            R-axis value
    :param theta: float
            Theta-axis value
    :param phi: float
            Phi-axis value

    :return:
    x: float
        X-axis value.
    y: float
        Y-axis value.
    z: float
        Z-axis value.

    """
    x = r * np.sin( theta ) * np.cos( phi )
    y = r * np.sin( theta ) * np.sin( phi )
    z = r * np.cos( theta )

    return x,y,z

def Spherical2Cartesian( x, y, z ):
    """
    Docstring:
    Converts spherical to cartesian coordinates.

    :param x: float
        X-axis value.
    :param y: float
        Y-axis value.
    :param z: float
        Z-axis value.

    :return:
    r: float
        R-axis value
    theta: float
        Theta-axis value
    phi: float
        Phi-axis value

    """
    r = np.sqrt( x**2 + y**2 + z**2 )
    theta = np.arctan( np.sqrt( x**2 + y**2)/z )
    phi = np.arctan( y/x )

    return r, theta, phi