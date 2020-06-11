import numpy as np
from Mestrado.Utils.Mag import delta_mag

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
