import shelve
import numpy as np
from Mestrado.Sources import Dipole
from Mestrado.Utils.Auxiliaries import generate_random

class Single_model:

    def __init__(self, r_center, theta_center, phi_center, inclination, declination, intensity ):
        self.r = r_center
        self.theta = theta_center
        self.phi = phi_center
        self.inclination = inclination
        self.declination = declination
        self.intensity = intensity
        self.ndipoles = 1
        self.dipoles = [ Dipole( self.r, self.theta, self.phi, self.inclination, self.declination, self.intensity)]

    def __update_dipoles_number( self ):
        self.ndipoles += 1
        if self.ndipoles > 1000:
            self.ndipoles = 1000

    def __clean_dipoles(self):
        dipoles = [ ]
        for dipole in self.dipoles:
            dipoles.append( Dipole( dipole.radius, dipole.theta, dipole.phi, dipole.inclination, dipole.declination, dipole.intensity ) )

        self.dipoles = dipoles

    def add_dipole( self, r, theta, phi, intensity , inclination = None, declination = None):
        self.__update_dipoles_number( )
        if inclination is None and declination is None:
            d = Dipole( r,theta, phi, self.inclination, self.declination, intensity )
        elif inclination is not None and declination is None:
            d = Dipole( r,theta, phi, inclination, self.declination, intensity )
        elif inclination is None and declination is not None:
            d = Dipole( r,theta, phi, self.inclination, declination, intensity )
        elif inclination is not None and declination is not None:
            d = Dipole( r,theta, phi, inclination, declination, intensity )

        self.dipoles.append( d )

    def expand( self, observers ):
        result = { }
        self.B_r, self.B_theta, self.B_phi = 0,0,0
        for dipole in self.dipoles:
            B_r, B_theta, B_phi = dipole.expand( observers )
            self.B_r += B_r
            self.B_theta += B_theta
            self.B_phi += B_phi

        result['Radial'] = self.B_r
        result['Theta'] = self.B_theta
        result['Phi'] = self.B_phi
        self.__clean_dipoles()
        return result

    def r_component( self, observers ):
        self.B_r = 0
        for dipole in self.dipoles:
            self.B_r += dipole.r_component( observers )

    def theta_component( self, observers ):
        self.B_theta = 0
        for dipole in self.dipoles:
            self.B_theta += dipole.theta_component( observers )

    def phi_component( self, observers ):
        self.B_phi = 0
        for dipole in self.dipoles:
            self.B_phi += dipole.phi_component( observers )


    def save( self, name ):
        s = shelve.open( name )
        s['model'] = self
        s.close()


if __name__ == "__main__":
    ndip = 50
    model = Single_model( 6000, np.radians( 70 ) , np.radians( 50 ), 0, np.pi/4, 2e10  )
    rad = generate_random( 5500, 6000, ndip )
    theta = generate_random( np.radians( 70 ), np.radians( 70 ), ndip )
    phi = generate_random( np.radians( 50 ), np.radians( 50 ), ndip )
    intensities = generate_random( 1e10, 3e10, ndip )
    declinations = generate_random( 0, 2*np.pi,1 )
    for i in range( ndip ):
        model.add_dipole( rad[ i ], theta[ i ], phi[ i ], intensities[ i ], inclination=0, declination = np.pi/4 )

    model.save('Bodies/'+str(ndip)+'_dip_6000_70_40')

    # body = shelve.open('Bodies/50_dip_6000_70_40')['model']
    # #source_components = body.expand(observers)
    # for d in body.dipoles:
    #     print(d.radius)

    # body = shelve.open('Bodies/100_dip_6000_70_40')['model']
    #
    # h = 1
    # nobs = 50
    # obs_theta = np.linspace(np.radians(0), np.radians(180), nobs)
    # obs_phi = np.linspace(np.radians(-180), np.radians(180), nobs)
    # observers = []
    # for i in range(nobs):
    #     for j in range(nobs):
    #         observers.append([6371 + h * 1000, obs_theta[i], obs_phi[j]])
    #
    # from time import time
    #
    # t1 = time()
    # body.r_component( observers )
    # print( time() - t1 )
    # from Mestrado.Plots import plot_mag
    #
    # plot_mag( np.reshape( body.B_r, (nobs, nobs ) ), 'B_r', 'B_r (nT)', show = True, save = False )

