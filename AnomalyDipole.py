import numpy as np
from Utils.Spherical import unit_spherical_vectors, inverse_distance_function, rij_vector
from Utils.Magnetic import magnetic_moment, H_matrix, magnetic_potential
from Utils.Parsers import check_size

#TODO: O DIPOLO DEVE SER UM OOBJETO. AS FUNCOES DEVEM ESTAR ORIENTADAS A ELE

def Anomaly_Field( dipole_pos, inclination, declination, observers_pos, mode = 'radians' ):
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
        Matrix like [ [r1,theta1,phi1], ..., [r1,theta1,phi1] ] meaning the position of the observers in a geocentric spherical coordinate system.

    :return:
    A: array_like
        Anomaly field caused by the dipole source.
    """

    m04pi = 1e-7
    A = [ ]
    vj = unit_spherical_vectors( dipole_pos[ 1 ], dipole_pos[ 2 ], mode = mode )
    m = magnetic_moment( dipole_pos[ 1 ], dipole_pos[ 2 ], 1, declination, inclination, mode = mode )

    observers_pos = check_size( observers_pos)

    for observer_pos in observers_pos:
        vi = unit_spherical_vectors( observer_pos[ 1 ], observer_pos[ 2 ], mode = mode )

        inverse_rij = inverse_distance_function( dipole_pos, observer_pos, mode = mode )


        H = ( inverse_rij**2 )*H_matrix( observer_pos[ 0 ], dipole_pos[ 0 ], vi, vj )

        A.append( ( m04pi*inverse_rij**3 )*np.dot( H, m ) )

    return np.array( A )

def Anomaly_Field2( dipole_pos, inclination, declination, observers_pos, h = 0.01, index = 0,  mode = 'radians'):
    """
    Dcostring:
    Calculates the Anomaly field produced by a unitary dipole source using the gradient method.

    :param dipole_pos: array_like
        Array like [r, theta, phi] meaning the position of a dipole in a geocentric spherical coordinate system.
    :param inclination: float
        Inclination.
    :param declination: float
        Declination.
    :param observer_pos: matrix_like
        Matrix like [ [r1,theta1,phi1], ..., [r1,theta1,phi1] ] meaning the position of the observers in a geocentric spherical coordinate system.
    :param h: float
        Value for the formula df/dx = ( f(x+h/2) - f(x-h/2) )/h.
    :param index: int
        For an observer like [r,theta,phi], over what index should the derivative should be taken.
    :return:
    A: array_like
        Anomaly field caused by the dipole source.
    """
    observers_pos = check_size( observers_pos )
    obs_behind = [ ]
    for observer_pos in observers_pos:
        observer_pos[ index ] -= h/2
        obs_behind.append( observer_pos )

    m_behind = magnetic_potential(dipole_pos, inclination, declination, obs_behind, mode = mode )

    obs_front = [ ]
    for observer_pos in observers_pos:
        observer_pos[ index ] += h
        obs_front.append( observer_pos )

    m_front = magnetic_potential(dipole_pos, inclination, declination, obs_front, mode = mode )

    if index == 0:
        factor = 1
    elif index == 1:
        factor = 1/( np.array( observers_pos )[:,0] )
    elif index == 2:
        factor = ( np.array( observers_pos )[:,0] )*( np.sin( np.array( observers_pos )[:,1] ) )
        factor = 1/factor

    A = factor*np.array( ( -m_behind + m_front )/h )

    return -A


if __name__ == "__main__":

    dipole = [ 1, 45, 90 ]
    inc, dec = -45, -45

    observers_theta = 40
    observers_phi = 0

    nobs = 1000
    razao = np.pi/nobs
    observers = [ ]
    for i in range( nobs ):
        observers.append( [ 2+i , observers_theta, observers_phi ] )

    A1 = Anomaly_Field( dipole, inc, dec, observers, mode = 'degree' )
    A2r = Anomaly_Field2( dipole, inc, dec, observers, mode = 'degree', index=0)

    import matplotlib.pyplot as plt

    # plt.figure( figsize = ( 10,10 ) )
    # plt.plot( np.arange( len(A1[:,0] ) ), A1[:,0], 'r')
    # plt.plot( np.arange( 10,len(A2r )+10 ) , A2r, 'g' )
    plt.plot( A1[:,0], A2r, 'g' )
    plt.grid( )
    plt.show( )

    # ri, theta_i , phi_i = 700, 90, 45
    # rj, theta_j, phi_j = 2, 30, 25
    # incl, decl = 10, 20
    #
    #
    # h = 0.001
    # dip_pos = [ rj, theta_j, phi_j ]
    # obs_pos = [ ri, theta_i, phi_i ]
    #
    # obs_adi = [ ri + h/2 , theta_i, phi_i ]
    # obs_atr = [ ri - h/2 , theta_i, phi_i ]
    #
    # A = Anomaly_Field( dip_pos, incl, decl, obs_pos, mode = 'degree' )
    #
    # psi_adi = Anomaly_Field2( dip_pos, incl, decl, obs_adi, mode = 'degree' )
    # psi_atr = Anomaly_Field2( dip_pos, incl, decl, obs_atr, mode = 'degree')
    #
    # print( 1e20*A )
    # print( -1e20*( ( psi_adi - psi_atr )/h ) )
