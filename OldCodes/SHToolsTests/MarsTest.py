from SHMag import FromCoeffFile
from Plots import PlotMag

if __name__ == '__main__':
    data = FromCoeffFile( 'CrustalMagneticMarsCoeff.txt', Type = 'all' )
    PlotMag( data['total'], 'Campo Total', '|B| (nT)', show = True, save = False )

# plot_mag( total_mag.data, 'Campo Total', '|B| (nT)' )
# plot_mag( mag_radial.data, 'Componente Radial', '|$B_r$| (nT)' )
# plot_mag( mag_theta.data, 'Componente Theta', '|$B_\Theta$| (nT)' )
# plot_mag( mag_phi.data, 'Componente Phi', '|$B_\phi$| (nT)' )
# plot_mag( potential_mag.data, 'Potencial', ' ' )

