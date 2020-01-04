import matplotlib.animation as animation
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime as dt
import numpy as np
import calendar
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

    

class Plot:
    def __init__ (self, punkts):
        self.punkts = punkts
        self.month_association={'Январь':1,'Февраль':2,'Март':3,'Апрель':4,'Май':5,'Июнь':6,'Июль':7,'Август':8,
                                                        'Сентябрь':9,'Октябрь':10,'Ноябрь':11,'Декабрь':12}

    
    def set_data (self,frame,punkt_name, month_name = 'Январь'):

        self.month_name = month_name
        
        # some prerequirements for clalculations
        self.day_for_calculate = dt.datetime.now().replace(day = 1, month = self.month_association[month_name])
        month = self.day_for_calculate.month

        # init variables
        self.days_of_week = np.array([])
        self.week_of_month = np.array([])
        self.regular_punkts_quantity = np.array([])
        self.annual_punkts_quantity = np.array([])
        
        # calculation to draw a plot
        for i in range(calendar.mdays[month]):
            self.days_of_week = np.append(self.days_of_week, self.day_for_calculate.weekday())
            self.week_of_month = np.append(self.week_of_month, self.day_for_calculate.isocalendar()[1] - self.day_for_calculate.replace(day=1).isocalendar()[1])
            self.regular_punkts_quantity = np.append(self.regular_punkts_quantity, len(self.punkts.today_punkts(self.day_for_calculate,annual = False)))
            self.annual_punkts_quantity = np.append(self.annual_punkts_quantity, len(self.punkts.today_punkts(self.day_for_calculate,annual = True)))
            self.day_for_calculate+= dt.timedelta(1)
        self.alpha = [0 if i==0 else 1 for i in self.annual_punkts_quantity ]


    def draw_plot_for_month(self,frame):

        # select style in which draw a plot
        with plt.style.context('seaborn-white'):
            
            self.fig = plt.figure()
            self.ax = plt.axes(projection='3d')
            self.ax.set_title(self.month_name)

            # view settings
            self.ax.invert_yaxis()
            self.ax.view_init(50,103)
            self.ax.set_zlim((0,40))

            # actualy draw a plot
            for i in range(len(self.regular_punkts_quantity)):
                self.ax.bar3d(self.days_of_week[i], self.week_of_month[i], 0, 0.3, 0.3, self.regular_punkts_quantity[i], color='paleturquoise')
                self.ax.bar3d(self.days_of_week[i], self.week_of_month[i], self.regular_punkts_quantity[i], 0.3, 0.3,
                             self.annual_punkts_quantity[i], color='orange', alpha = self.alpha[i],zsort='max')
            
            # set intendents from edges
            self.fig.subplots_adjust(left=0.02, right=0.99, bottom=0.03, top=0.99)

            # post plot to tk.frame
            canvas = FigureCanvasTkAgg(self.fig, master=frame)
            canvas.get_tk_widget().pack()
            self.ax.get_children()[-1].set_edgecolor('r')
            return self.fig
            
    def update(self):

        # redraw to update plot when new data comes
        self.ax.cla()
        self.ax.set_title(self.month_name)
        self.ax.invert_yaxis()
        self.ax.view_init(50,103)
        self.ax.set_zlim((0,40))
        for i in range(len(self.regular_punkts_quantity)):
                self.ax.bar3d(self.days_of_week[i], self.week_of_month[i], 0, 0.3, 0.3, self.regular_punkts_quantity[i], color='paleturquoise')
                self.ax.bar3d(self.days_of_week[i], self.week_of_month[i], self.regular_punkts_quantity[i], 0.3, 0.3,
                             self.annual_punkts_quantity[i], color='orange', alpha = self.alpha[i],zsort='max')

    def destroy(self):
        del(self)