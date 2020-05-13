from palettable import scientific as scm
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


mycmap = scm.diverging.Vik_20.mpl_colormap

def plot_mag( data, title, label, show = False, save = True ):
    """
    Plot a Magnetic data on a rectangular latitude x longitude grid.

    :param data: Array_like
        Array representing the magnetic data.
    :param title: string
        The title of the plot.
    :param label: string
        The label of the data.
    :param show: bool
        If True, matplotlib.pyplot.show() will be included in the code.
    :param save: bool
        If True, matplotlib.pyplot.savefig() will the included and the figure will be saved, as .png, with the title name.
     """

    nlats, nlongs = np.shape( data )

    plt.figure()
    plt.title(title, fontsize=20)
    plt.contourf( data, 50, cmap=mycmap)
    plt.xticks(np.arange(0, nlongs, nlongs // 12), labels=np.arange(-180, 180, 30))
    plt.yticks(np.arange(0, nlats, nlats // 6), labels=np.arange(0, 181, 30)[::-1])
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

    if save == True:
        plt.savefig(save_title+'.png', dpi = 300, bbox_inches = 'tight')
    if show == True:
        plt.show( )

def plot_meshgrid( meshgrid, xlims = None, ylims = None, show = True):
    gridx, gridy = meshgrid[ 0 ], meshgrid[ 1 ]
    figure, axis = plt.subplots()

    if xlims == None:
        axis.vlines(gridx[0], min(gridy[:, 0]) - abs(min(gridy[:, 0])) / 5,
                    max(gridy[:, 0]) + abs(max(gridy[:, 0])) / 5, colors='r')
        axis.set_xlim(min(gridx[0]) - abs(min(gridx[0]))/10, max(gridx[0]) + abs(max(gridx[0]))/10 )
    else:
        axis.vlines(gridx[0], min(ylims), max(ylims), colors='r')
        axis.set_xlim( min( xlims ), max( xlims ) )

    if ylims == None:
        axis.hlines(gridy[:, 0], min(gridx[0]) - abs(min(gridx[0])) / 5,
                    max(gridx[0]) + abs(max(gridx[0])) / 5, colors='r')
        axis.set_ylim(min(gridy[:, 0]) - abs(min(gridy[:, 0])) / 10, max(gridy[:, 0]) + abs(max(gridy[:, 0])) / 10)
    else:
        axis.hlines(gridy[:,0],min(xlims), max(xlims), colors='r')
        axis.set_ylim( min( ylims ), max( ylims ) )

    if show == True:
        plt.show()
    return figure, axis


def scatter_3d( x, y, z, show = True ):

    figure = plt.figure( )
    axis = figure.add_subplot( 111, projection = '3d' )
    axis.scatter( x, y, z, marker = 'D', c = 'b' )
    if show == True:
        plt.show( )

    return figure, axis



