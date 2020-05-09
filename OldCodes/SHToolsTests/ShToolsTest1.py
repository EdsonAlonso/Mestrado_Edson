import pyshtools as pysh
import numpy as np
import matplotlib.pyplot as plt

pysh.utils.figstyle(rel_width=0.75)

#Creating a power spectrum that follow a power law with exponet -2

degrees = np.arange(101, dtype=float)
degrees[0] = np.inf
power = degrees**(-2)

#Creating a random realization of spherical harmonic coefficients whose expected power is the onde we just created

clm = pysh.SHCoeffs.from_random( power, seed = 12345 )

#Calculating the power spectrum and ploting it:

fig, ax = clm.plot_spectrum( show=False )
#plt.show( )
plt.close( ) #This functions does not close the figure, so imd doing it manually

#Visualizing the power asociated with each spherical-harmonic coefficient:

fig, ax = clm.plot_spectrum2d(vrange=(1.e-7,0.1), show=False)
#plt.show( )
plt.close( )

#Converting the coeffients to the orthonormalized convention using the Condon-Shortley phase:

clm_ortho = clm.convert(normalization='ortho', csphase=-1, lmax=50)

#If you ever forget how your data are normalized, you can just print the variable:

print( clm_ortho )

#Calculating the power spectra of our two functions and plot them along with our input expectation spectrum:

fig, ax = clm.plot_spectrum(legend='Orthonormalized', show=False)
clm_ortho.plot_spectrum(ax=ax, linestyle='dashed', legend='4$\pi$ normalized')
ax.plot(clm.degrees(), power, '-k', label = 'Expected')
ax.legend( )
limits = ax.set_xlim(0, 100)
#plt.show( )
plt.close( )

#Expanding the data onto a grid and ploting it:

grid = clm.expand()
fig, ax = grid.plot(show=False)
#plt.show( )
plt.close( )

#Expanding the spherical harmonic coefficents onto a Gauss-Legendre-Quadrature grid:

grid_glq = clm.expand(grid='GLQ')

#Ploting it, and outputing lists that contain the latitudes and longitudes for each row and column of the grid:

grid_glq.plot(show=False)
#plt.show( )
plt.close( )

lats = grid_glq.lats()
lons = grid_glq.lons()

#The info method provides information about an object:
grid_glq.info()

#Setting the coeficient to a specified value:

clm.set_coeffs(ls=2,
               ms=0,
               values=0.)
grid_dh2 = clm.expand()
fig, ax = grid_dh2.plot(colorbar='right',
                        cb_label='My data',
                        show=False)

#plt.show( )
plt.close( )

#Extracting the coefficients or the grid to a file:

#clm.to_file( 'name')
coeff = clm.to_array( lmax = 2 )
print( coeff )

#Calculating the spherical harmonic coefficients from a grid is as easy as expanding the coefficients onto a grid:

clm_new = grid_dh2.expand()


#Evaluating the spherical harmonic coefficients at a specific set of points:
print( clm.expand(lat=[90., 10., -45., -90.],
           lon=[0., 90., 275., 0.]) )

