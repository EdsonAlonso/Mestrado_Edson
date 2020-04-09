import numpy as np
from Utils import magnetic_moment, Carterian2Spherical, Spherical2Cartesian

class Dipole:

    def __init__( self, r = None, theta = None, phi = None ):
        self.r = r
        self.theta = theta
        self.phi = phi
        self.m = None

    def to_cartesian( self ):
        self.x, self.y, self.z = Spherical2Cartesian( self.r, self.theta, self.phi )

    def from_cartesian( self, x, y, z ):
        self.x = x
        self.y = y
        self.z = z

    def to_spherical( self ):
        self.r, self.theta, self.phi = Carterian2Spherical( self.x, self.y, self.z )

    def magnetic_moment( self, intensity, declination, inclination ):
        self.m = magnetic_moment( self.theta, self.phi, intensity, declination, inclination )
        return self.m