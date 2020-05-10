from Mestrado.EquivalentLayer import Spherical
import numpy as np
from Mestrado.Plots import plot_mag
from time import time

ndip_theta = 40
ndip_phi = 40

l = Spherical( 6371, ndip_phi, ndip_theta )
intensities = np.random.uniform( low = 1, high = 2, size = (ndip_phi, ndip_theta ) )
#l.from_array( intensities, 0, 0 )
l.from_random( np.radians( 0 ), np.radians( 0 ) )
#l.from_positions( np.radians( 90 ), [ np.radians(-50), np.radians(50)], [1,1], np.radians(0), np.radians(0) )
h = 5
nobs = 50
obs_theta = np.linspace(np.radians(0), np.radians(180), nobs)
obs_phi = np.linspace(np.radians(-180), np.radians(180), nobs)
observers = []
for i in range(nobs):
    for j in range(nobs):
        observers.append([6371 + h * 1000, obs_theta[i], obs_phi[j]])

t1 = time( )
l.r_component( observers )
l.theta_component( )
l.phi_component( )
print( time( ) - t1 )
#l.show_layer()
#l.show_component('Theta')

Total = np.sqrt( l.B_r**2 + l.B_theta**2 + l.B_phi**2 )


plot_mag( np.reshape( l.B_r , (nobs,nobs) ), 'Campo Total', '|B| (nT)', show = True, save = False )
