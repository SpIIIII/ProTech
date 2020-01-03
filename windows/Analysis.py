import datetime as dt
import tkinter as tk
from tkinter import ttk


class Analysis(tk.Toplevel):
    def __init__(self,root,punkts,plot):
        super().__init__(root)
        self.title("Анализ")
        self.geometry("640x530")
        self.minsize(600,350)
        self.bind('<Escape>', lambda e: self.destroy())

        self.plot = plot
        self.punkts = punkts
        
        self.curent_date = dt.datetime.now()
        
        self.init_analysis()

    

    def init_analysis(self):
        
        # function to darw plot and post it to bottom_frame
        def draw_plot(event):
            self.plot.draw_plot_for_month(bottom_frame,combox_punkts.get(), combox_month.get())

        # add frames
        top_frame = ttk.Frame(self,height=50)
        top_frame.pack(side=tk.TOP,fill=tk.BOTH, expand=True)

        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(side=tk.BOTTOM,fill=tk.BOTH, expand=True)

        # Draw MenuBar
        menubar = tk.Menu()
        filemenu = tk.Menu(menubar, tearoff=0)
          
        filemenu.add_separator()
        filemenu.add_command(label="Выход", command=self.destroy)
        
        menubar.add_cascade(label="Файл", menu=filemenu)
        self.config(menu=menubar)

        # fill top_frame
        combox_month = ttk.Combobox(top_frame,values=['Январь','Февраль','Март','Апрель','Май','Июнь','Июль','Август',
                                                         'Сентябрь','Октябрь','Ноябрь','Декабрь', 'Год'],justify='center')
        combox_month.current(self.curent_date.month-1)
        combox_month.place(x=470,y=10)
        combox_month.bind("<<ComboboxSelected>>", draw_plot)

        combox_punkts = ttk.Combobox(top_frame, values=[i.name for i in self.punkts],justify='center',width = 15)
        combox_punkts.current(0)
        combox_punkts.place(x=340,y=10)
        combox_punkts.bind("<<ComboboxSelected>>", draw_plot)

        def create_combox_punkts(event):
            period = combox_periods.get()
            if period == ' Все':
                combox_punkts.config(values=[i.name for i in self.punkts])
                combox_punkts.current(0)
            else:
                combox_punkts.config(values=[i.name for i in self.punkts if i.period == period])
                combox_punkts.current(0)
            
            
        periods = [i for i in set(i.period for i in self.punkts)]
        periods.append(' Все')
        combox_periods = ttk.Combobox(top_frame,values=periods,justify='center')
        combox_periods.current(len(periods)-1)
        combox_periods.place(x=470,y=30)

        combox_periods.bind("<<ComboboxSelected>>", create_combox_punkts)
        
        # init drawing plot
        draw_plot(None)
        
        
        self.grab_set()
        self.focus_set()
