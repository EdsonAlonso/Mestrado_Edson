import numpy as np
from Mestrado.Sources import Dipole
from Mestrado.Layer import Layer
from Mestrado.Utils.Auxiliaries import generate_random


class Spherical( Layer ):

    def __init__( self, radius, n_phi, n_theta ):
        Layer.__init__( Layer, n_phi, n_theta)
        self.radius = radius
        self.dipoles = [ ]
        self.intialize( )

    def _add_dipole_from_class( self, dipole ):
        self.dipoles.append( dipole )

    def _add_dipole_from_properties( self, theta, phi, inclination, declination ):
        d = Dipole( self.radius, theta, phi, inclination, declination, 1 )
        self.dipoles.append( d )

    def __create_B_matrix( self, observers ):
        Br_layer = []
        Btheta_layer = []
        Bphi_layer = []
        for dipole in self.dipoles:
            Br_layer.append( dipole.r_component( observers ) )
            Btheta_layer.append( dipole.theta_component( observers ) )
            Bphi_layer.append( dipole.phi_component( observers ) )

        return np.c_[ Br_layer, Btheta_layer, Bphi_layer ].T

    def intialize( self ):
        self.phi, self.theta = self.regular_layer( -np.pi, np.pi, 0, np.pi )
        self.inclination = generate_random( 0, np.pi, ( self.nx, self.ny ) )
        self.declination = generate_random( 0, 2*np.pi, ( self.nx, self.ny ) )
        for i in range( self.ny ):
            for j in range( self.nx ):
                self._add_dipole_from_properties( self.theta[ i ][ j ], self.phi[ i ][ j ],
                                                  self.inclination[ j ][ i ], self.declination[ j ][ i ] )

    def expand( self, observers ):
        if not self.__fitted__:
            return 'Need to fit the model first!!'
        self.observers = observers
        self.B_r, self.B_theta, self.B_phi = 0,0,0
        for dipole in self.dipoles:
            self.B_r += dipole.r_component( self.observers )
            self.B_theta += dipole.theta_component( self.observers )
            self.B_phi += dipole.phi_component( self.observers )

        return self



    def fit( self, observers, data ):
        self.__fitted__ = True
        A = self.__create_B_matrix( observers )
        b = data
        try:
            x = np.array( np.linalg.lstsq( A, b ) )[ 0 ]
            for index, dipole in enumerate(self.dipoles):
                dipole.intensity *= x[index]
        except Exception as e:
            self.__fitted__ = False

    def show(self):
        pass


if __name__ == '__main__':

    radius = 6000
    nphi = 30
    ntheta = 30
    eqly  = Spherical( 6000, 20, 30 )

    h = 4
    nobs = 50
    obs_theta = np.linspace(np.radians(0), np.radians(180), nobs)
    obs_phi = np.linspace(np.radians(-180), np.radians(180), nobs)
    observers = []
    for i in range(nobs):
        for j in range(nobs):
            observers.append([radius + h*1000, obs_theta[i], obs_phi[j]])

    components = eqly.expand( observers )

    from Mestrado.Plots import plot_mag

    plot_mag( np.reshape( components.B_r , (nobs,nobs) ), 'Componente radial', 'B_r (nT)', show = True, save = False )

#
# def from_array( self, magnetic_intensity, inclination, declination ):
#     self.inclination, self.declination = inclination, declination
#     self.phi, self.theta = self.regular_layer( np.radians( -180 ), np.radians( 180 ), np.radians( 0 ), np.radians( 180 ) )
#     for i in range( self.n_theta ):
#         for j in range( self.n_phi ):
#             self._add_dipole_from_properties( self.radius, self.theta[i][j], self.phi[i][j],inclination, declination,
#                                               magnetic_intensity[ j ][ i ] )
#
#     self.property = np.reshape( magnetic_intensity, (np.shape( self.theta ) ) )
#
# def from_random( self, inclination, declination ):
#     self.inclination, self.declination = inclination, declination
#     self.theta = np.empty( self.n_theta )
#     self.phi = np.empty( self.n_phi )
#
#     self.property = np.random.uniform( low = 1, high = 1.5, size = (self.n_phi, self.n_theta ) )
#
#     for i in range( self.nx ):
#         phi = np.random.choice(np.linspace(np.radians(-180), np.radians(180), 200))
#         self.phi[i] = phi
#         for j in range( self.ny ):
#             theta = np.random.choice(np.linspace(np.radians(0), np.radians(180), 200))
#             self.theta[j] = theta
#             self._add_dipole_from_properties( self.radius, theta, phi,inclination, declination,
#                                               self.property[ i ][ j ] )
#
#     self.phi, self.theta = self.defined_layer( self.phi, self.theta )
#
# def from_positions( self, theta, phi, intensity, inclination, declination ):
#     self.inclination, self.declination = inclination, declination
#
#     variables = [ theta, phi, intensity ]
#
#     for i in range( len( variables ) ):
#         if not isinstance( variables[ i ], (list, tuple, np.ndarray ) ):
#             variables[ i ] = np.array( [ variables[ i ] ] )
#
#     self.theta = variables[ 0 ]
#     self.phi = variables[ 1 ]
#     self.property = variables[ 2 ]
#
#     for i in range( len( self.theta ) ):
#         for j in range( len( self.phi ) ):
#             self._add_dipole_from_properties( self.radius, self.theta[ i ], self.phi[ j ],
#                                               self.inclination, self.declination,
#                                               self.property[ i + j ] )
