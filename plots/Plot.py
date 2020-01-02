import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Plot:
    def __init__ (self):
        pass
    
    def draw_plot(self,frame):
        with plt.style.context('seaborn-white'):
            fig = plt.figure()
            ax = plt.axes(projection='3d')
            x, y = np.random.rand(2, 100) * 4
            hist, xedges, yedges = np.histogram2d(x, y, bins=4, range=[[0, 4], [0, 4]])

            # Construct arrays for the anchor positions of the 16 bars.
            xpos, ypos = np.meshgrid(xedges[:-1] + 0.25, yedges[:-1] + 0.25, indexing="ij")
            xpos = xpos.ravel()
            ypos = ypos.ravel()
            zpos = 0

            # Construct arrays with the dimensions for the 16 bars.
            dx = dy = 0.5 * np.ones_like(zpos)
            dz = hist.ravel()
            [print(i) for i in (xpos, ypos, zpos, dx, dy, dz)]
            ax.bar3d(xpos, ypos, zpos, dx, dy, 1, zsort='average')
        
            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.get_tk_widget().pack()
            canvas.draw()