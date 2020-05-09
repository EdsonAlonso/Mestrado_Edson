import numpy as np
from Mestrado.Utils.Spherical import distance
from Mestrado.Utils.Mag import magnetization, delta_mag

#TODO: Think of a method to better check if A,B,C,...etc. have been already calculated
#TODO: Create a Method do plot the dipole, and return the figure to be able to add another dipole in the plot.

class Dipole(object):

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


    def _define_observers( self, observers ):
        if type( observers ) == np.ndarray:
            self.observers = observers
        else:
            self.observers = np.array( observers )


    def r_component( self, observers = None ):

        mr, mtheta, mphi = magnetization( self.intensity, self.inclination, self.declination )
        if self.observers is None:
            self._define_observers( observers )

        r, theta, phi = self.observers[:, 0], self.observers[:, 1], self.observers[:, 2]

        cos_delta = delta_mag( self.observers, self.pos )

        if self._A is None:
            self._A = r - self.radius * cos_delta
        if self._R is None:
            self._R = distance(self.observers, self.pos)
        if self._A1 is None:
            self._A1 = self.radius - r * cos_delta
        if self._B1 is None:
            self._B1 = r * (np.cos(theta) * np.sin(self.theta) - np.cos(self.theta) * np.sin(theta) * np.cos(phi - self.phi))
        if self._C1 is None:
            self._C1 = -r * np.sin(theta) * np.sin(phi - self.phi)

        factor1 = (-1 / self._R ** 3)
        factor_r = (3 * self._A * self._A1 / self._R ** 2 + cos_delta)
        factor_theta = (3 * self._A * self._B1 / self._R ** 2 - self._B1 / r)
        factor_phi = (3 * self._A * self._C1 / self._R ** 2 - self._C1 / r)

        self.Br = factor1 * (factor_r * mr + factor_theta * mtheta + factor_phi * mphi)

        return self.Br

    def theta_component( self, observers = None ):

        mr, mtheta, mphi = magnetization( self.intensity, self.inclination, self.declination )

        if self.observers is None:
            self._define_observers( observers )

        r, theta, phi = self.observers[:, 0], self.observers[:, 1], self.observers[:, 2]

        cos_delta = delta_mag( self.observers, self.pos )

        if self._B is None:
            self._B = self.radius * (np.sin(theta) * np.cos(self.theta) - np.cos(theta) * np.sin(self.theta) * np.cos(phi - self.phi))
        if self._R is None:
            self._R = distance(self.observers, self.pos)
        if self._A1 is None:
            self._A1 = self.radius - r * cos_delta
        if self._B1 is None:
            self._B1 = r * (np.cos(theta) * np.sin(self.theta) - np.cos(self.theta) * np.sin(theta) * np.cos(phi - self.phi))
        if self._C1 is None:
            self._C1 = -r * np.sin(theta) * np.sin(phi - self.phi)
        if self._D is None:
            self._D = np.sin(theta) * np.sin(self.theta) + np.cos(theta) * np.cos(self.theta) * np.cos(phi - self.phi)
        if self._E is None:
            self._E = np.cos(theta) * np.sin(phi - self.phi)

        factor1 = (-1 / self._R ** 3)
        factor_r = (3 * self._B * self._A1 / self._R ** 2 - self._B / self.radius)
        factor_theta = (3 * self._B * self._B1 / self._R ** 2 + self._D)
        factor_phi = (3 * self._B * self._C1 / self._R ** 2 + self._E)

        self.Btheta = factor1 * (factor_r * mr + factor_theta * mtheta + factor_phi * mphi)

        return self.Btheta

    def phi_component( self, observers = None ):

        mr, mtheta, mphi = magnetization( self.intensity, self.inclination, self.declination )


        if self.observers is None:
            self._define_observers( observers )

        r, theta, phi = self.observers[:, 0], self.observers[:, 1], self.observers[:, 2]

        cos_delta = delta_mag( self.observers, self.pos )

        if self._C is None:
            self._C = self.radius * np.sin(self.theta) * np.sin(phi - self.phi)
        if self._R is None:
            self._R = distance(self.observers, self.pos)
        if self._A1 is None:
            self._A1 = self.radius - r * cos_delta
        if self._B1 is None:
            self._B1 = r * (np.cos(theta) * np.sin(self.theta) - np.cos(self.theta) * np.sin(theta) * np.cos(phi - self.phi))
        if self._C1 is None:
            self._C1 = -r * np.sin(theta) * np.sin(phi - self.phi)
        if self._F is None:
            self._F = np.cos(self.theta) * np.sin(phi - self.phi)
        if self._G is None:
            self._G = np.cos(phi - self.phi)

        factor1 = (-1 / self._R ** 3)
        factor_r = (3 * self._C * self._A1 / self._R ** 2 - self._C / self.radius)
        factor_theta = (3 * self._C * self._B1 / self._R ** 2 - self._F)
        factor_phi = (3 * self._C * self._C1 / self._R ** 2 + self._G)

        self.Bphi = factor1 * (factor_r * mr + factor_theta * mtheta + factor_phi * mphi)

        return self.Bphi

