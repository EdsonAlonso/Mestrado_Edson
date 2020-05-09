import matplotlib.pyplot as plt
import pyshtools as pysh
from pyshtools import constant

pysh.utils.figstyle(rel_width=0.75)

#Reading the gravitational potential coefficients and errors for the planet Mars:
clm = pysh.SHGravCoeffs.from_file('gmm3_120_sha.tab', errors=True, header_units='km')

print( clm.info() )

#Setting the angular rotation of the planet, semimajor axis and flatteing fot the reference ellipsoid:
clm.set_omega(constant.omega_mars.value)

a = constant.a_mars.value
f = constant.f_mars.value
u0 = constant.u0_mars.value

#Plotting the spectrum of the function:
#function can be geoid, potential, radial , total
fig1, ax1 = clm.plot_spectrum(function='geoid', show=False)
fig2, ax2 = clm.plot_spectrum2d(function='total', show=False)

#plt.show( )
plt.close( )
plt.close( )

#Expading to a grid the potential, the three vector components fo the g_field and the g_disturbance:
#Also plotting it:

grav = clm.expand(lmax=95, a=a, f=f)
fig2, ax2 = grav.plot(show=False)
#plt.show( )
plt.close( )

#Plotting each component individually:
#We can use plot_pot, plot_rad, plot_theta, plot_phi, plot_total

fig3, ax3 = grav.plot_total(cmap='terrain', show=False)
#plt.show( )
plt.close( )

#Saving and plotting the geoid:

mars_geoid = clm.geoid(u0, lmax=719)
fig4, ax4 = mars_geoid.plot(cmap='terrain', show=False)
#plt.show( )
plt.close( )

# To calculate the geoid height with respect to a flattened ellipsoid, just specify the optional parameters a and f:

mars_geoid_ellipsoid = clm.geoid(u0, a=a, f=f, lmax=719)
fig5, ax5 = mars_geoid_ellipsoid.plot(cmap='terrain', cmap_limits=[-750, 1200], show=False)
plt.show( )

