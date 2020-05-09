from Mestrado.OldCodes.SHToolsTests.SHMag import FromCoeffFile
import numpy as np

file = '../SHToolsTests/CrustalMagneticMarsCoeff.txt'
r = 50

R = 3393500.0 + r*1000

rho = 3393500.0

dif_sqrd = ( R**2 - rho**2 )/( 4*np.pi*R**2 )

def TrapezoidalRule2D( grid ):

    step = 1
    xrange = np.shape( grid )[ 0 ]
    yrange = np.shape( grid )[ 1 ]

    integral = 0

    for x in range( xrange - 1 ):
        for y in range( yrange - 1 ):
            f_lower_left = grid[ x ][ y ]
            f_lower_right = grid[ x + step ][ y ]
            f_upper_left = grid[ x ][ y + step ]
            f_upper_right = grid[ x + step ][ y + step ]

            sum = f_lower_left + f_lower_right + f_upper_left + f_upper_right
            volume = 0.25*step**2*sum
            integral += volume

    return integral




def lSphere( r,theta,phi, R, theta_prime, phi_prime ):

    factor_1 = r**2 + R**2
    factor_2 = 2*r*R
    factor_3 = np.cos(theta)*np.cos(theta_prime) + np.sin(theta)*np.sin(theta_prime)*np.cos( phi - phi_prime )

    return factor_1 - factor_2*factor_3

def Integral( r, theta, phi, shape ):

    xrange, yrange = shape


    for x in range( xrange ):
        for y in range( yrange ):
            grid[ x ][ y ] = np.sin( np.radians( x ) )*pot0[ x ][ y ]/lSphere( r, theta,phi, R ,np.radians( x ), np.radians( y )  )

    return TrapezoidalRule2D( grid )




if __name__ == '__main__':
    pot0 = FromCoeffFile( file, 'pot' )
    #pot1 = FromCoeffFile( file, 'pot', h = r )
    theta,phi = 0, 0
    grid = np.empty( pot0.shape )
    integrand = np.empty( pot0.shape )

    #
    # for x in range( pot0.shape[ 0 ] ):
    #     for y in range( pot0.shape[ 1 ] ):
    #         grid[ x ][ y ] = np.sin( np.radians( x ) )*pot0[ x ][ y ]/lSphere( rho, theta,phi, R ,np.radians( x ), np.radians( y )  )

    for i in range( 0, pot0.shape[ 0 ] ):
        for j in range( pot0.shape[ 1 ] ):
            integrand[ i ][ j ] = Integral( rho, np.radians( i ), np.radians( j ), pot0.shape )

    print( integrand )
    #PlotMag( integrand, show=True, save = False )

    #print( (R/1000)**2*dif_sqrd*TrapezoidalRule2D( grid ) )
    #print( pot1[ 0 ][ 0 ] )
    #pot1 = FromCoeffFile( file, 'pot', h = r )
    # print( pot0.shape )
    # X,Y = np.meshgrid( range( 271 ), range( 501 ) )
    #
    # grid = (X + Y)/1000
    #
    # print( TrapezoidalRule2D( grid ))

    # plt.scatter( X,Y )
    # plt.show( )
    #pot01 = IntegratePot( rho, np.pi/4, np.pi/4, R, pot0 )
    #print( dif_sqrd*pot01 )
    #PlotMag( pot0, 'Potencial 1', 'U', show = False, save = True )
    #PlotMag( pot1, 'Potencial 2', 'U', show = False, save = True )
