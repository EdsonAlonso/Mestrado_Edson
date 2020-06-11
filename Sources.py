import numpy as np
from Mestrado.Utils.Spherical import distance
from Mestrado.Utils.Mag import magnetization, delta_mag
import matplotlib.pyplot as plt
from Mestrado.Utils.Constants import Constants

class Dipole( Constants ):

    def __init__( self, radius, theta, phi, inclination, declination, intensity ):
        self.radius = radius
        self.theta = theta
        self.phi = phi
        self.declination = declination
        self.inclination = inclination
        self.intensity = intensity
        self._R, self._A, self._B, self._C, self._D, self._E, self._F, self._G, self._A1, self._B1, self._C1 = [None]*11
        self.pos = np.array( [ self.radius, self.theta, self.phi ] )
        self.observers = None
        self.mr, self.mtheta, self.mphi = magnetization( self.intensity, self.inclination, self.declination )
        self.magnetization = [ self.mr, self.mtheta, self.mphi ]


    def __clean_dipoles(self):
        dipoles = []
        for dipole in self.dipoles:
            dipoles.append(Dipole(dipole.r, dipole.theta, dipole.phi, dipole.inclination, dipole.declination,
                                  dipole.intensity))

        self.dipoles = dipoles

    def _define_observers( self, observers ):
        if type( observers ) == np.ndarray:
            self.observers = observers
        else:
            self.observers = np.array( observers )
        self.cos_delta = delta_mag( self.observers, self.pos )
        self.R = distance( self.observers, self.pos )

    def __Br__(self,r):
        factor_r = (3 * self.A * self.A1 / self.R ** 2 + self.cos_delta)
        factor_theta = (3 * self.A * self.B1 / self.R ** 2 - self.B1 / r)
        factor_phi = (3 * self.A * self.C1 / self.R ** 2 - self.C1 / r)

        self.Br = self.__factor * (factor_r * self.mr + factor_theta * self.mtheta + factor_phi * self.mphi)

    def __Btheta__(self):
        factor_r = (3 * self.B * self.A1 / self.R ** 2 - self.B / self.radius)
        factor_theta = (3 * self.B * self.B1 / self.R ** 2 + self.D)
        factor_phi = (3 * self.B * self.C1 / self.R ** 2 + self.E)
        self.Btheta = self.__factor * (factor_r * self.mr + factor_theta * self.mtheta + factor_phi * self.mphi)

    def __Bphi__(self):
        factor_r = (3 * self.C * self.A1 / self.R ** 2 - self.C / self.radius)
        factor_theta = (3 * self.C * self.B1 / self.R ** 2 - self.F)
        factor_phi = (3 * self.C * self.C1 / self.R ** 2 + self.G)

        self.Bphi = self.__factor * (factor_r * self.mr + factor_theta * self.mtheta + factor_phi * self.mphi)


    def expand( self, observers ):
        self._define_observers( observers )

        r = self.observers[:, 0]

        Constants.__init__( Constants, self.pos, self.observers )
        self.A,self.A1 = self.get_constants( 'A' ), self.get_constants( 'A1' )
        self.B,self.B1 = self.get_constants( 'B' ), self.get_constants( 'B1' )
        self.C,self.C1 = self.get_constants( 'C' ), self.get_constants( 'C1' )
        self.D, self.E = self.get_constants( 'D' ), self.get_constants( 'E' )
        self.F, self.G = self.get_constants( 'F' ), self.get_constants( 'G' )
        self.__factor = (-1 / self.R ** 3)

        self.__Br__(r)
        self.__Btheta__()
        self.__Bphi__()

        return self.Br, self.Btheta, self.Bphi

    def show( self, figure = None, axis = None ):
        if figure or axis:
            self.figure = figure
            self.axis = axis

            self.axis.scatter( self.theta, self.phi, marker = 'D', s = 40, color = 'blue' )
            plt.show( )
        else:
            self.figure = plt.figure()
            self.axis = self.figure.subplots( )
            self.axis.scatter( self.theta, self.phi, marker = 'D', s = 40, color = 'blue' )
            plt.show( )

        return self.figure, self.axis