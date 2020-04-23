import AnomalyDipole
import numpy as np

def test_one( ):
    """
    Esta funcao deve fazer o primeiro teste, i.e., o teste em que a coolatitude do observador eh a mesma do dipolo.

    """
    #dipolo
    rj, theta_j, phi_j = 0, 0, 0
    incl, dec = 0,0
    #obs1
    r1, theta_1, phi_1 = 1, 90, 90

    #obs2
    r2, theta_2, phi_2 = 2, 90, 270

    dip_pos = [rj, theta_j, phi_j]

    obs1_pos = [r1, theta_1, phi_1]
    obs2_pos = [r2, theta_2, phi_2]
    obs = [obs1_pos, obs2_pos]

    A = AnomalyDipole.Anomaly_Field(dip_pos, incl, dec, obs, mode = 'degree')

    assert abs( A[0][0] - A[1][0] ) < 1e-7
    assert abs( A[0][1] - A[1][1] ) < 1e-7
    assert abs( A[0][2] - A[1][2] ) < 1e-7


def test_two( ):
    """
    Esta funcao deve fazer o segundo teste, i.e., verificar se A = -grad(psi), ou pelo menos perto o suficiente.
    """
    eps = 1E-3

    dipole = [ 1, 45, 90 ]
    inc, dec = -45, -45

    observers_theta = 45
    observers_phi = 0

    nobs = 1000
    observers = [ ]
    for i in range( nobs ):
        observers.append( [ 2+i , observers_theta, observers_phi ] )

    A1r = AnomalyDipole.Anomaly_Field( dipole, inc, dec, observers, mode = 'degree' )[:,0]
    A2r = AnomalyDipole.Anomaly_Field2( dipole, inc, dec, observers, mode = 'degree' )

    np.testing.assert_almost_equal( A1r, A2r )


def test_three( ):
    """
    Esta funcao deve fazer o terceiro teste.
    """
    eps = 1E-3

    dipole = [ 6371, 90, 0 ]
    inc, dec = -90, 90

    observer1_theta = 91

    observer2_theta = 89

    observers_phi = 0

    observers = [ [ 6371, observer1_theta, observers_phi ], [ 6371, observer2_theta, observers_phi ] ]

    A = AnomalyDipole.Anomaly_Field( dipole, inc, dec, observers, mode = 'degree' )


    np.testing.assert_almost_equal( A[0][0], A[1][0] )