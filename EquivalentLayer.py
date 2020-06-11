import numpy as np
from Mestrado.Sources import Dipole
from Mestrado.Layer import Layer
from Mestrado.Utils.Auxiliaries import generate_random
from Mestrado.Erros import NotFittedError

class Spherical( Layer ):

    def __init__( self, radius, n_phi, n_theta, inclination = None, declination = None ):
        Layer.__init__( Layer, n_phi, n_theta)
        self.radius = radius
        self.inclination = inclination
        self.declination = declination
        self.dipoles = [ ]
        self._intialize_( )
        self.intensities = np.empty( self.nx*self.ny )
        self.__fitted__ = False



    def __clean_dipoles(self):
        dipoles = [ ]
        for dipole in self.dipoles:
            dipoles.append( Dipole( dipole.radius, dipole.theta, dipole.phi, dipole.inclination, dipole.declination, dipole.intensity ) )

        self.dipoles = dipoles

    def _add_dipole_from_class_( self, dipole ):
        self.dipoles.append( dipole )

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
            self.inclination = np.ones( ( self.nx, self.ny ) )*self.inclination
        if self.declination is None:
            self.declination = generate_random( 0, 2*np.pi, ( self.nx, self.ny ) )
        else:
            self.declination = np.ones( ( self.nx, self.ny ) )*self.declination

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
            x = np.array( np.linalg.lstsq( A, b,rcond=None ) )[ 0 ]
            for index, dipole in enumerate(self.dipoles):
                self.intensities[ index ] = x[ index ]
        except Exception as e:
            self.__fitted__ = False

    def show(self):
        pass