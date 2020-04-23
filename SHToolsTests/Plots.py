from palettable import scientific as scm
import numpy as np
import matplotlib.pyplot as plt

mycmap = scm.diverging.Vik_20.mpl_colormap

def PlotMag( data, title, label, show = False, save = True ):
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

    if save == True:
        plt.savefig(save_title+'.png', dpi = 300, bbox_inches = 'tight')
    if show == True:
        plt.show( )