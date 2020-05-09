import numpy as np
from Mestrado.Sources import Dipole
from Mestrado.Layer import Layer


class EqLayer( Layer, Dipole ):

    def __init__( self, radius, n_theta, n_phi ):
        Layer.__init__( Layer, n_theta, n_phi)
        self.radius = radius
        self.property = None
        self.n_theta = self.nx
        self.n_phi = self.ny
        self.dipoles = [ ]
        self.observers = None
        self.r = 0
        self.theta = None
        self.phi = None


    def from_array( self, magnetic_intensity, inclination, declination ):
        self.inclination, self.declination = inclination, declination
        self.theta, self.phi = self.regular_layer( np.radians( 0 ), np.radians( 180 ), np.radians( -180 ), np.radians( 180 ) )

        if type( magnetic_intensity ) != np.ndarray:
            magnetic_intensity = np.array( magnetic_intensity )
        self.property = np.reshape( magnetic_intensity, (np.shape( self.theta ) ) )

    def from_positions( self, theta, phi, magnetic_intensity, inclination, declination ):
        self.theta, self.phi = [ ], [ ]
        self.inclination, self.declination = inclination, declination
        if len( np.shape( theta ) ) == 1:
            theta = [ theta ]
        if len( np.shape( phi ) ) == 1:
            phi = [ phi ]
        self.theta = np.array( theta )
        self.phi = np.array( phi )

        self.theta, self.phi = np.meshgrid( self.theta, self.phi )

        if type( magnetic_intensity ) != np.ndarray:
            magnetic_intensity = np.array( magnetic_intensity )
        self.property = np.reshape( magnetic_intensity, (np.shape( self.theta ) ) )

    def r_component( self, observers ):
        if self.observers is None:
            self.observers = observers
        for i in range( self.n_phi ):
            for j in range( self.n_theta ):
                d = Dipole( self.radius, self.theta[ i ][ j ], self.phi[ i ][ j ], self.inclination,\
                                             self.declination, self.property[ i ][ j ] )
                self.dipoles.append( d )
                self.r += d.r_component( self.observers )


    def theta_component( self, observers ):
        if self.observers is None:
            self.observers = observers

        for i in range( self.n_phi ):
            for j in range( self.n_theta ):
                d = Dipole( self.radius, self.theta[ i ][ j ], self.phi[ i ][ j ], self.inclination,\
                                             self.declination, self.property[ i ][ j ] )
                self.dipoles.append( d )
                self.r += d.theta_component( self.observers )

    def phi_component( self, observers ):
        if self.observers is None:
            self.observers = observers

        for i in range( self.n_phi ):
            for j in range( self.n_theta ):
                d = Dipole( self.radius, self.theta[ i ][ j ], self.phi[ i ][ j ], self.inclination,\
                                             self.declination, self.property[ i ][ j ] )
                self.dipoles.append( d )
                self.r += d.phi_component( self.observers )
