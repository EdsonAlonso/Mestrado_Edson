import numpy as np
from Mestrado.Sources import Dipole
from Mestrado.Layer import Layer
from time import time
import matplotlib.pyplot as plt
from Mestrado.Plots import plot_mag
from datetime import datetime


#TODO: Refactor. This class is to big. Maybe a factory to return the components in just 1 function. Or maybe just one
#function to return all the components and, maybe, the potential(I dont think Im gonna use it).

class Spherical( Layer, Dipole ):

    def __init__( self, radius, n_phi, n_theta ):
        Layer.__init__( Layer, n_phi, n_theta)
        self.radius = radius
        self.property = None
        self.n_theta = self.ny
        self.n_phi = self.nx
        self.dipoles = [ ]
        self.observers = None
        self.B_r = 0
        self.B_theta = 0
        self.B_phi = 0
        self.theta = None
        self.phi = None


    def _add_dipole_from_class( self, dipole ):
        self.dipoles.append( dipole )

    def _add_dipole_from_properties( self, radius, theta, phi, inclination, declination, intensity ):
        d = Dipole( radius, theta, phi, inclination, declination, intensity )
        self.dipoles.append( d )


    def from_array( self, magnetic_intensity, inclination, declination ):
        self.inclination, self.declination = inclination, declination
        self.phi, self.theta = self.regular_layer( np.radians( -180 ), np.radians( 180 ), np.radians( 0 ), np.radians( 180 ) )
        #print(np.rad2deg(self.phi))
        for i in range( self.n_theta ):
            for j in range( self.n_phi ):
                self._add_dipole_from_properties( self.radius, self.theta[i][j], self.phi[i][j],inclination, declination,
                                                  magnetic_intensity[ j ][ i ] )

        self.property = np.reshape( magnetic_intensity, (np.shape( self.theta ) ) )

    def from_random( self, inclination, declination ):
        self.inclination, self.declination = inclination, declination
        self.theta = np.empty( self.n_theta )
        self.phi = np.empty( self.n_phi )

        self.property = np.random.uniform( low = 1, high = 1.5, size = (self.n_phi, self.n_theta ) )

        for i in range( self.nx ):
            phi = np.random.choice(np.linspace(np.radians(-180), np.radians(180), 200))
            self.phi[i] = phi
            for j in range( self.ny ):
                theta = np.random.choice(np.linspace(np.radians(0), np.radians(180), 200))
                self.theta[j] = theta
                self._add_dipole_from_properties( self.radius, theta, phi,inclination, declination,
                                                  self.property[ i ][ j ] )

        self.phi, self.theta = self.defined_layer( self.phi, self.theta )

    def from_positions( self, theta, phi, intensity, inclination, declination ):
        self.inclination, self.declination = inclination, declination

        variables = [ theta, phi, intensity ]

        for i in range( len( variables ) ):
            if not isinstance( variables[ i ], (list, tuple, np.ndarray ) ):
                variables[ i ] = np.array( [ variables[ i ] ] )

        self.theta = variables[ 0 ]
        self.phi = variables[ 1 ]
        self.property = variables[ 2 ]

        for i in range( len( self.theta ) ):
            for j in range( len( self.phi ) ):
                self._add_dipole_from_properties( self.radius, self.theta[ i ], self.phi[ j ],
                                                  self.inclination, self.declination,
                                                  self.property[ i + j ] )


    def r_component( self, observers = None ):
        if self.observers is None:
            self.observers = observers
        for dipole in self.dipoles:
            # print( np.rad2deg( dipole.theta ), np.rad2deg( dipole.phi ) )
            self.B_r += dipole.r_component( self.observers )

    def theta_component( self, observers = None ):
        if self.observers is None:
            self.observers = observers

        for dipole in self.dipoles:
            self.B_theta += dipole.theta_component( self.observers )

    def phi_component( self, observers = None ):
        if self.observers is None:
            self.observers = observers

        for dipole in self.dipoles:
            self.B_phi += dipole.phi_component( self.observers )

    def show_layer( self, save = False ):
        self.gridy = np.rad2deg( self.theta )
        self.gridx = np.rad2deg( self.phi )
        self.figure, self.axis = self.show( xlims = [-180, 180], ylims = [0,180], show = False )
        self.axis.invert_yaxis( )

        self.axis.scatter( np.rad2deg( self.phi ), np.rad2deg( self.theta ), marker = 'D', s = 40, color = 'blue')
        if save == True:
            now = datetime.now()
            self.figure.savefig( f'Layer_{str(now)}' )
        plt.show( )

    def show_component( self, name, save = False ):
        shape = int( np.sqrt( len( self.observers ) ) )
        if name == 'Radial':
            plot_mag( self.B_r.reshape( shape,shape ), 'Radial Component', 'B_r (nT)', show = True, save = save )
        elif name == 'Theta':
            plot_mag( self.B_theta.reshape( shape,shape ), 'Theta Component', '$B_\Theta$ (nT)', show = True, save = save )
        elif name == 'Phi':
            plot_mag( self.B_phi.reshape( shape,shape ), 'Phi Component', '$B_\phi$ (nT)', show = True, save = save )
