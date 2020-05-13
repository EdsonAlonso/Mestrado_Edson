import shelve
import numpy as np
from Mestrado.Sources import Dipole
from Mestrado.Plots import scatter_3d


class Spherical:

    def __init__(self, radius, r_center, theta_center, phi_center, mode = 'meters'):
        self.radius = radius
        self.r = r_center
        self.theta = theta_center
        self.phi = phi_center
        self.mode = mode
        self.ndipoles = 1000
        self.dipoles = [ ]

    def __set_dipoles_number( self ):
        if self.mode == 'km':
            self.radius *= 1000

        self.ndipoles = int( self.radius*10 )
        if self.ndipoles > 1000:
            self.ndipoles = 1000

    def _populate( self ):
        self.__set_dipoles_number( )
        theta = np.random.uniform( 0, np.pi, self.ndipoles )
        phi = np.random.uniform( np.radians( -180 ), np.radians( 180 ), self.ndipoles )
        radius = np.ones(self.ndipoles)*30#np.random.uniform( self.r, self.r + self.radius, self.ndipoles )

        return radius, theta, phi

    def create( self, inclination, declination ):

        self.radius_array, self.theta_array, self.phi_array = self._populate( )

        self.inclination = inclination
        self.declination = declination
        self.intensities = np.random.uniform( 1, 3, self.ndipoles )

        for i in range( self.ndipoles ):
            d = Dipole( self.r + self.radius_array[ i ], self.theta + self.theta_array[ i ], self.phi +  self.phi_array[ i ],
                        inclination, declination, self.intensities[ i ] )
            self.dipoles.append( d )

    def r_component( self, observers ):
        self.B_r = 0
        for dipole in self.dipoles:
            self.B_r += dipole.r_component( observers )

    def theta_component( self, observers ):
        self.B_r = 0
        for dipole in self.dipoles:
            self.B_r += dipole.theta_component( observers )

    def phi_component( self, observers ):
        self.B_r = 0
        for dipole in self.dipoles:
            self.B_r += dipole.phi_component( observers )


    def save( self, name ):
        s = shelve.open( name )
        s['dipole'] = self
        s.close()

    def show( self ):

        self.figure, self.axis = scatter_3d( self.radius_array,
                                             self.theta_array,
                                             self.phi_array,
                                            show = False )
        plt.show( )


# if __name__ == "__main__":
#     import matplotlib.pyplot as plt
#     model = Spherical( 20, 6300, np.radians( 30 ) , np.radians( 10 ) )
#     model.create( 0, 0 )
#     model.show( )
#     h = 5
#     nobs = 50
#     obs_theta = np.linspace(np.radians(0), np.radians(180), nobs)
#     obs_phi = np.linspace(np.radians(-180), np.radians(180), nobs)
#     observers = []
#     for i in range(nobs):
#         for j in range(nobs):
#             observers.append([6371 + h * 1000, obs_theta[i], obs_phi[j]])
#
#     model.r_component( observers )



