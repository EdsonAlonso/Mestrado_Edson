import pyshtools as pysh
from pyshtools import constant


def FromCoeffFile( coeff_file, Type = 'total', h = 0 ):

    """
    Function that calculates the Magnetic Field, one of its components, or Potential Magnetic Field, from a
    gauss-coefficients file. This function uses SHTools for python.

    :param coeff_file: str
        Name of the coefficients file.
    :param Type: str
        Can be any of the following values: total, radial, theta, phi, pot, all
        Return either the total magnetic field, one of its components or the potential field. If Type is all, returns
        all of the above types as a python dictionary.

    :param h: float
        Height to be added to the reference ellipsoid, in Km


    :return:Array_like or dict
        The Type chosen by the user.
    """

    clm = pysh.SHMagCoeffs.from_file(coeff_file)
    clm.info( )

    a = clm.__dict__['r0']
    #a = constant.a_mars.value
    print( f'a: {a}' )
    h *= 1000
    print( f'h: {h}')

    try:
        mag = clm.expand( a = a + h, f = 0 )
    except Exception as e:
        print(e)

    d = { }
    d['total'] = mag.total.data
    d['radial'] = mag.rad.data
    d['theta'] = mag.theta.data
    d['phi'] = mag.phi.data
    d['pot'] = mag.pot.data

    if Type == 'all':
        return d

    return d[Type]



