import numpy as np
from Mestrado.Utils.Spherical import distance
from Mestrado.Utils.Mag import magnetization, delta_mag
import matplotlib.pyplot as plt

#TODO: Think of a method to better check if A,B,C,...etc. have been already calculated
#TODO: Maybe refactor this
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
        return np.array( self.Br )

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


if __name__ == "__main__":
    d = Dipole( 6371, np.radians(90), np.radians(0),np.radians(90), np.radians(0), 1 )

    h = 5
    nobs = 50
    obs_theta = np.linspace(np.radians(0), np.radians(180), nobs)
    obs_phi = np.linspace(np.radians(-180), np.radians(180), nobs)
    observers = []
    for i in range(nobs):
        for j in range(nobs):
            observers.append([6371 + h * 1000, obs_theta[i], obs_phi[j]])

    d._define_observers( observers )
    from time import time
    t1 = time( )
    B_r = d.r_component( )
    B_theta = d.theta_component( )
    B_phi = d.phi_component( )

    print( time( ) - t1 )

    from Mestrado.Plots import plot_mag
    plot_mag( np.reshape( B_r , (nobs,nobs) ), 'Campo Total', 'B', show = True, save = False )
