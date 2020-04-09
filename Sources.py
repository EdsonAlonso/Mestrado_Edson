import numpy as np
from Utils import magnetic_moment

class Dipole:

    def __init__( self, r = None, theta = None, phi = None ):
        self.r = r
        self.theta = theta
        self.phi = phi
        self.m = None

    def to_cartesian( self ):
        self.x = self.r * np.sin( self.theta ) * np.cos( self.phi )
        self.y = self.r * np.sin( self.theta ) * np.sin( self.phi )
        self.z = self.r * np.cos( self.phi )

    def from_cartesian( self, x, y, z ):
        self.x = x
        self.y = y
        self.z = z

    def to_spherical( self ):
        self.r = np.sqrt( self.x**2 + self.y**2 + self.z**2 )
        self.theta = np.arctan( np.sqrt( self.x**2 + self.y**2 )/self.z )
        self.phi = np.arctan( self.y/self.x )

    def magnetic_moment( self, intensity, declination, inclination ):
        self.m = magnetic_moment( self.theta, self.phi, intensity, declination, inclination )
        return self.m