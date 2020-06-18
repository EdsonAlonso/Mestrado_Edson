import numpy as np
from Mestrado.Sources import Dipole
from Mestrado.Layer import Layer
from Mestrado.Utils.Auxiliaries import generate_random
from Mestrado.Erros import NotFittedError
from Mestrado.Regularization import get_H_matrix
from sklearn.linear_model import Ridge
import shelve

class Spherical( Layer ):

    def __init__( self, radius, n_phi, n_theta, inclination = None, declination = None ):
        Layer.__init__( Layer, n_phi, n_theta)
        self.radius = radius
        self.inclination = inclination
        self.declination = declination
        self.dipoles = [ ]
        self._intialize_( )
        self.intensities = np.zeros( self.nx*self.ny )
        self.observers = None
        self.__fitted__ = False



    def __clean_dipoles(self):
        dipoles = [ ]
        for dipole in self.dipoles:
            dipoles.append( Dipole( dipole.radius, dipole.theta, dipole.phi, dipole.inclination, dipole.declination, dipole.intensity ) )

        self.dipoles = dipoles

    def _add_dipole_from_properties_( self, theta, phi, inclination, declination, intensity ):
        d = Dipole( self.radius, theta, phi, inclination, declination, intensity )
        self.dipoles.append( d )

    def __create_B_matrix__( self, observers ):
        Br_layer = []
        Btheta_layer = []
        Bphi_layer = []
        for dipole in self.dipoles:
            B_r, B_theta, B_phi = dipole.expand( observers )
            Br_layer.append( B_r )
            Btheta_layer.append( B_theta )
            Bphi_layer.append( B_phi )

        self.__clean_dipoles()

        return np.c_[ Br_layer, Btheta_layer, Bphi_layer ].T

    def _intialize_( self ):
        self.dipoles = [ ]
        self.phi, self.theta = self.regular_layer( -np.pi, np.pi, 0, np.pi )
        if self.inclination is None:
            self.inclination = generate_random( 0, np.pi, ( self.nx, self.ny ) )
        elif self.inclination is not None:
            self.inclination = np.zeros( ( self.nx, self.ny ) ) + self.inclination
        if self.declination is None:
            self.declination = generate_random( 0, 2*np.pi, ( self.nx, self.ny ) )
        elif self.declination is not None:
            self.declination = np.zeros( ( self.nx, self.ny ) ) + self.declination

        for i in range( self.ny ):
            for j in range( self.nx ):
                self._add_dipole_from_properties_( self.theta[ i ][ j ], self.phi[ i ][ j ],
                                                  self.inclination[ j ][ i ], self.declination[ j ][ i ], 1 )

    def expand( self, observers ):
        if self.__fitted__ is False:
            raise NotFittedError

        self.observers = observers

        self.B_r, self.B_theta, self.B_phi = 0,0,0
        for index,dipole in enumerate( self.dipoles ):
            B_r, B_theta, B_phi = dipole.expand( self.observers )
            self.B_r += self.intensities[index]*B_r
            self.B_theta += self.intensities[index]*B_theta
            self.B_phi += self.intensities[index]*B_phi


        self.__clean_dipoles()

        return self


    def fit( self, observers, data ):

        self.__fitted__ = True
        A = self.__create_B_matrix__( observers )
        b = data
        try:
            lstq = Ridge( alpha = 0, solver='svd' )
            lstq.fit(A, b)
            x = lstq.coef_
            for index, dipole in enumerate(self.dipoles):
                self.intensities[ index ] = x[ index ]
        except Exception as e:
            self.__fitted__ = False

    def fit_regularized( self, observer, data, lamb = 0, order = 0):

        self.__fitted__ = True
        try:
            coef = self.__get_coeff__( observer, data, lamb, order )
            for index, dipole in enumerate(self.dipoles):
                self.intensities[index] = coef[index]
        except Exception as e:
            self.__fitted__ = False

    def __get_coeff__(self, observers, data, lamb, order = 0 ):

        A = self.__create_B_matrix__( observers )
        n_col = A.shape[1]
        H = get_H_matrix( n_col, order )
        return np.linalg.lstsq(A.T.dot(A) + lamb * H, A.T.dot(data), rcond=None)[ 0 ]

    def save(self, name):
        s = shelve.open( name )
        s['layer'] = self
        s.close()