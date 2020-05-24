import numpy as np
from Mestrado.Utils.Spherical import distance
from Mestrado.Utils.Mag import magnetization, delta_mag
import matplotlib.pyplot as plt

#TODO: Think of a method to better check if A,B,C,...etc. have been already calculated
#TODO: Maybe refactor this

class Constants:

    def __init__(self, source, observers ):
        self.source = source
        self.r = source[ 0 ]
        self.theta = source[ 1 ]
        self.phi = source [ 2 ]
        self.observers = observers
        self.observers_r = observers[ :,0 ]
        self.observers_theta = observers[ :,1 ]
        self.observers_phi = observers[ :,2 ]
        self._A, self._B, self._C, self._D, self._E, self._F, self._G, self._A1, self._B1, self._C1 = [None]*10
        self.cos_delta = delta_mag( observers, source )

    def __A__( self, r1, r2 ):
        return  r1 - r2*self.cos_delta

    def __B__( self, r, theta1, theta2, phi1, phi2 ):
        return r * ( np.sin( theta1 )*np.cos( theta2 ) - np.cos( theta1 )*np.sin( theta2 )*np.cos( phi1 - phi2 ) )

    def __C__( self, r, theta, phi1, phi2 ):
        return r*np.sin( theta ) * np.sin( phi1 - phi2 )

    def __D__( self, theta1, theta2, phi1, phi2 ):
        return np.sin( theta1 )*np.sin( theta2 ) + np.cos( theta1 )*np.cos( theta2 )*np.cos( phi1 - phi2 )

    def __E__( self, theta, phi1, phi2 ):
        return np.cos( theta )*np.sin( phi1 - phi2 )

    def __F__( self, theta, phi1, phi2 ):
        return np.cos( theta ) * np.sin( phi1 - phi2 )

    def __G__( self, phi1, phi2 ):
        return np.cos( phi1 - phi2 )

    def get_constants( self, name ):
        if name == 'A':
            if self._A is None:
                self._A =  self.__A__( self.observers_r, self.r )
            return self._A
        elif name == 'B':
            if self._B is None:
                self._B = self.__B__( self.r, self.observers_theta, self.theta, self.observers_phi, self.phi )
            return self._B
        elif name == 'C':
            if self._C is None:
                self._C = self.__C__( self.r, self.theta, self.observers_phi, self.phi )
            return self._C
        elif name == 'D':
            if self._D is None:
                self._D = self.__D__( self.observers_theta, self.theta, self.observers_phi, self.phi )
            return self._D
        elif name == 'E':
            if self._E is None:
                self._E = self.__E__( self.observers_theta, self.observers_phi, self.phi )
            return self._E
        elif name == 'F':
            if self._F is None:
                self._F = self.__F__( self.theta, self.observers_phi, self.phi )
            return self._F
        elif name == 'G':
            if self._G is None:
                self._G = self.__G__(self.observers_phi, self.phi )
            return self._G
        elif name == 'A1':
            if self._A1 is None:
                self._A1 = self.__A__( self.r, self.observers_r )
            return self._A1
        elif name == 'B1':
            if self._B1 is None:
                self._B1 = self.__B__( self.observers_r, self.theta, self.observers_theta, self.observers_phi, self.phi)
            return self._B1
        elif name == 'C1':
            if self._C1 is None:
                self._C1 = self.__C__( -self.observers_r, self.observers_theta, self.observers_phi, self.phi )
            return self._C1

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

    def _define_observers( self, observers ):
        if type( observers ) == np.ndarray:
            self.observers = observers
        else:
            self.observers = np.array( observers )
        self.cos_delta = delta_mag( self.observers, self.pos )
        self.R = distance( self.observers, self.pos )



    def expand( self, observers ):
        self._define_observers( observers )

        r, theta, phi = self.observers[:, 0], self.observers[:, 1], self.observers[:, 2]

        Constants.__init__( Constants, self.pos, self.observers )
        self.A,self.A1 = self.get_constants( 'A' ), self.get_constants( 'A1' )
        self.B,self.B1 = self.get_constants( 'B' ), self.get_constants( 'B1' )
        self.C,self.C1 = self.get_constants( 'C' ), self.get_constants( 'C1' )
        self.D, self.E = self.get_constants( 'D' ), self.get_constants( 'E' )
        self.F, self.G = self.get_constants( 'F' ), self.get_constants( 'G' )

        factor1 = (-1 / self.R ** 3)
        factor_r = (3 * self.A * self.A1 / self.R ** 2 + self.cos_delta)
        factor_theta = (3 * self.A * self.B1 / self.R ** 2 - self.B1 / r)
        factor_phi = (3 * self.A * self.C1 / self.R ** 2 - self.C1 / r)

        self.Br = factor1 * (factor_r * self.mr + factor_theta * self.mtheta + factor_phi * self.mphi)

        factor_r = (3 * self.B * self.A1 / self.R ** 2 - self.B / self.radius)
        factor_theta = (3 * self.B * self.B1 / self.R ** 2 + self.D)
        factor_phi = (3 * self.B * self.C1 / self.R ** 2 + self.E)

        self.Btheta = factor1 * (factor_r * self.mr + factor_theta * self.mtheta + factor_phi * self.mphi)

        factor_r = (3 * self.C * self.A1 / self.R ** 2 - self.C / self.radius)
        factor_theta = (3 * self.C * self.B1 / self.R ** 2 - self.F)
        factor_phi = (3 * self.C * self.C1 / self.R ** 2 + self.G)

        self.Bphi = factor1 * (factor_r * self.mr + factor_theta * self.mtheta + factor_phi * self.mphi)

        return self.Br, self.Btheta, self.Bphi


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


# if __name__ == "__main__":
#     d = Dipole( 6371, np.radians(90), np.radians(0),np.radians(30), np.radians(0), 1 )
#
#     h = 4
#     nobs = 50
#     obs_theta = np.linspace(np.radians(0), np.radians(180), nobs)
#     obs_phi = np.linspace(np.radians(-180), np.radians(180), nobs)
#     observers = []
#     for i in range(nobs):
#         for j in range(nobs):
#             observers.append([6371 + h * 1000, obs_theta[i], obs_phi[j]])
#
#     d._define_observers( observers )
#     from time import time
#     t1 = time( )
#     # B_r, Btheta, Bphi = d.expand( observers )
#     B_r = d.r_component( )
#     # B_theta = d.theta_component( )
#     # B_phi = d.phi_component( )
#
#     print( time( ) - t1 )
#
#     from Mestrado.Plots import plot_mag
#     plot_mag( np.reshape( B_r , (nobs,nobs) ), 'Campo Total', 'B', show = True, save = False )
