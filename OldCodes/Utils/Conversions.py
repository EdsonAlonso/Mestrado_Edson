import numpy as np

def Carterian2Spherical(r, theta, phi):
    """
    Docstring:
    Converts geocentric cartesian to spherical coordinates.

    :param r: float
            R-axis value
    :param theta: float
            Theta-axis value
    :param phi: float
            Phi-axis value

    :return:
    x: float
        X-axis value.
    y: float
        Y-axis value.
    z: float
        Z-axis value.

    """
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)

    return x, y, z


def Spherical2Cartesian(x, y, z):
    """
    Docstring:
    Converts spherical to geocentric cartesian coordinates.

    :param x: float
        X-axis value.
    :param y: float
        Y-axis value.
    :param z: float
        Z-axis value.

    :return:
    r: float
        R-axis value
    theta: float
        Theta-axis value
    phi: float
        Phi-axis value

    """
    r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
    theta = np.arctan(np.sqrt(x ** 2 + y ** 2) / z)
    phi = np.arctan(y / x)

    return r, theta, phi