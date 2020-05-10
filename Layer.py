import numpy as np
from Mestrado.Plots import plot_meshgrid

class Layer(object):

    def __init__( self, nx = None, ny = None ):
        self.nx = nx
        self.ny = ny
        self.gridx, self.gridy = None, None

    def regular_layer( self, xmin, xmax, ymin, ymax ):
        self.x = np.linspace( xmin, xmax, self.nx )
        self.y = np.linspace( ymin, ymax, self.ny )

        self.gridx, self.gridy = np.meshgrid( self.x, self.y )

        return self.gridx, self.gridy

    def random_layer( self ):
        pass

    def defined_layer(self, x, y ):
        self.gridx, self.gridy = np.meshgrid( x,y )
        return self.gridx, self.gridy

    def show(self, xlims = None, ylims = None, show = True):
        self.figure, self.axis = plot_meshgrid([self.gridx, self.gridy], xlims, ylims,  show = show)

        return self.figure, self.axis

