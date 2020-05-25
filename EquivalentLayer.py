import numpy as np
from Mestrado.Sources import Dipole
from Mestrado.Layer import Layer
from Mestrado.Utils.Auxiliaries import generate_random


class Spherical( Layer ):

    def __init__( self, radius, n_phi, n_theta ):
        Layer.__init__( Layer, n_phi, n_theta)
        self.radius = radius
        self.dipoles = [ ]
        self._intialize_( )
        self.intensities = np.empty( self.nx*self.ny )
        self.__fitted__ = False

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
            Br_layer.append( dipole.r_component( observers ) )
            Btheta_layer.append( dipole.theta_component( observers ) )
            Bphi_layer.append( dipole.phi_component( observers ) )

        return np.c_[ Br_layer, Btheta_layer, Bphi_layer ].T

    def _intialize_( self ):
        self.dipoles = [ ]
        self.phi, self.theta = self.regular_layer( -np.pi, np.pi, 0, np.pi )
        self.inclination = generate_random( 0, np.pi, ( self.nx, self.ny ) )
        self.declination = generate_random( 0, 2*np.pi, ( self.nx, self.ny ) )
        for i in range( self.ny ):
            for j in range( self.nx ):
                self._add_dipole_from_properties_( self.theta[ i ][ j ], self.phi[ i ][ j ],
                                                  self.inclination[ j ][ i ], self.declination[ j ][ i ], 1 )


    def expand( self, observers ):
        if not self.__fitted__:
            return 'Need to fit the model first!!'
        self.observers = observers
        self.B_r, self.B_theta, self.B_phi = 0,0,0
        for index,dipole in enumerate( self.dipoles ):
            self.B_r += self.intensities[index]*dipole.r_component( self.observers )
            self.B_theta += self.intensities[index]*dipole.theta_component( self.observers )
            self.B_phi += self.intensities[index]*dipole.phi_component( self.observers )

        return self



    def fit( self, observers, data ):
        self.__fitted__ = True
        A = self.__create_B_matrix__( observers )
        b = data
        try:
            x = np.array( np.linalg.lstsq( A, b ) )[ 0 ]
            for index, dipole in enumerate(self.dipoles):
                self.intensities[ index ] = x[ index ]
        except Exception as e:
            self.__fitted__ = False

    def show(self):
        pass