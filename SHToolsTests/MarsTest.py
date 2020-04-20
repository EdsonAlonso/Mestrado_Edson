import matplotlib.pyplot as plt
import pyshtools as pysh
from pyshtools import constant
from palettable import scientific as scm
import numpy as np


pysh.utils.figstyle(rel_width=0.75)
mycmap = scm.diverging.Vik_20.mpl_colormap

clm = pysh.SHMagCoeffs.from_file( 'CrustalMagneticMarsCoeff.txt')

#print( clm.info( ) )

fig1, ax1 = clm.plot_spectrum(function='total', show=False)
fig2, ax2 = clm.plot_spectrum2d(function='total', show=False)

#plt.show( )
plt.close( )
plt.close( )

a = constant.a_mars.value
f = constant.f_mars.value
u0 = constant.u0_mars.value

try:
    mag = clm.expand( a = a, f = f )
except Exception as e:
    print(e)

total_mag = mag.total

fig2, ax2 = mag.plot( cmap = mycmap, show=False)
#plt.show( )
plt.close( )


fig3, ax3 = mag.plot_total(cmap=mycmap, show=False)
#plt.show( )
plt.close( )

# print( type( total_mag.data ) )
# nlats,nlongs = np.shape( total_mag.data )
# print( nlats, nlongs )
#
# plt.figure( )
# plt.title( 'Campo Total', fontsize = 20 )
# plt.contourf( total_mag.data, 500, cmap = mycmap )
# plt.xticks( np.arange( 0, nlongs, nlongs//12 ), labels = np.arange( 0, 361, 30 ) )
# plt.yticks( np.arange( 0, nlats, nlats//6 ), labels = np.arange( -90, 91, 30 )[ ::-1 ] )
# plt.gca( ).invert_yaxis( )
# plt.colorbar( label = '|B| (nT)' )
# plt.xlabel( 'Longitude (°)', fontsize = 20 )
# plt.ylabel( 'Latitude (°)', fontsize = 20 )
#
# plt.show( )

def plot_mag( data, title, label ):
    nlats, nlongs = np.shape( data )
    print(nlats, nlongs)

    plt.figure()
    plt.title(title, fontsize=20)
    plt.contourf( data, 500, cmap=mycmap)
    plt.xticks(np.arange(0, nlongs, nlongs // 12), labels=np.arange(0, 361, 30))
    plt.yticks(np.arange(0, nlats, nlats // 6), labels=np.arange(-90, 91, 30)[::-1])
    plt.gca().invert_yaxis()
    plt.colorbar(label=label)
    plt.xlabel('Longitude (°)', fontsize=20)
    plt.ylabel('Latitude (°)', fontsize=20)
    Title = title.split()
    save_title = ''
    for index, word in enumerate( Title ):
        save_title += word
        if index < len( Title ) - 1:
            save_title += '_'

    plt.savefig(save_title+'.png', dpi = 300, bbox_inches = 'tight')

#plot_mag( total_mag.data, 'Campo Total', '|B| (nT)' )

# mag_radial = mag.rad
# mag_theta = mag.theta
# mag_phi = mag.phi
potential_mag = mag.pot

# plot_mag( total_mag.data, 'Campo Total', '|B| (nT)' )
# plot_mag( mag_radial.data, 'Componente Radial', '|$B_r$| (nT)' )
# plot_mag( mag_theta.data, 'Componente Theta', '|$B_\Theta$| (nT)' )
# plot_mag( mag_phi.data, 'Componente Phi', '|$B_\phi$| (nT)' )
plot_mag( potential_mag.data, 'Potencial', ' ' )

