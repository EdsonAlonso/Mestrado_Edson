import AnomalyDipole
import numpy as np

def test_one( ):
    """
    Esta funcao deve fazer o primeiro teste, i.e., o teste em que a coolatitude do observador eh a mesma do dipolo.

    """
    pass


def test_two( ):
    """
    Esta funcao deve fazer o segundo teste, i.e., verificar se A = -grad(psi), ou pelo menos perto o suficiente.
    """
    eps = 1E-3

    ri, theta_i, phi_i = 2, 0, np.pi / 2
    rj, theta_j, phi_j = -5, np.pi/4, np.pi/2
    incl, decl = np.pi, np.pi/6

    dip_pos = [ rj, theta_j, phi_j ]
    obs_pos = [ ri, theta_i, phi_i ]

    A = AnomalyDipole.Anomaly_Field( dip_pos, incl, decl, obs_pos )

#TODO: FAZER A FUNCAO QUE CALCULA A PELO METODO DE -GRAD(PSI)
    assert np.linalg.norm( A - A ) < eps




