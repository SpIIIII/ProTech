import matplotlib.animation as animation
import datetime as dt
import tkinter as tk
from tkinter import ttk
from random import randrange
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Analysis(tk.Toplevel):
    def __init__(self,main):
        self.main = main
        super().__init__(self.main)
        self.title("Анализ")
        self.geometry("640x550")
        self.resizable(False,False)
        self.minsize(600,350)
        self.bind('<Escape>', lambda e: self.exit())
        self.protocol("WM_DELETE_WINDOW", self.exit)
        self.plot = self.main.plot
        self.punkts = self.main.punkts
        
        self.curent_date = dt.datetime.now()
        
        self.init_analysis()
        

    def exit(self):
        self.destroy()
    
    def update_plot(self,event):
            # inject data that need to be plotted
            self.plot.set_data(self.combox_punkts.get(), self.combox_month.get())
            # update plot
            self.plot.update_plot()

    def init_analysis(self):
        if len(self.punkts)==0:
            tk.messagebox.showerror('Пусто',"Похоже пока нету ни одного пункта.\n Пожалуйста сначала добавьте пункты для выполнения")
            self.destroy()
        else:
        
            ## add frames
            top_frame = ttk.Frame(self, height=68)
            top_frame.pack(side=tk.TOP,fill=tk.BOTH, expand=True)

            bottom_frame = ttk.Frame(self)
            bottom_frame.pack(side=tk.BOTTOM,fill=tk.BOTH, expand=True)

            ## Draw MenuBar
            menubar = tk.Menu()
            filemenu = tk.Menu(menubar, tearoff=0)
            
            filemenu.add_separator()
            filemenu.add_command(label="Выход", command=self.destroy)
            
            menubar.add_cascade(label="Файл", menu=filemenu)
            self.config(menu=menubar)

            ## fill top_frame
            #create label
            label = ttk.Label(top_frame, text = 'Выбранный пункт будет отмечен красным на графике')
            label.place(x=55, y=5)

            # create combox_month
            self.combox_month = ttk.Combobox(top_frame,values=['Январь','Февраль','Март','Апрель','Май','Июнь','Июль','Август',
                                                            'Сентябрь','Октябрь','Ноябрь','Декабрь'],justify='center')
            self.combox_month.current(self.curent_date.month-1)
            self.combox_month.bind("<<ComboboxSelected>>", self.update_plot)
            self.combox_month.place(x=470,y=25)

            # create combox_punkts
            self.combox_punkts = ttk.Combobox(top_frame, justify='center',width = 15)
            self.combox_punkts.bind("<<ComboboxSelected>>", lambda x: self.update_plot(None))
            self.combox_punkts.place(x=340,y=45)
            def create_combox_punkts(period):
                if period == ' Все':
                    punkts_to_fill = [i.name for i in self.punkts]
                    self.combox_punkts.config(values=punkts_to_fill)
                    self.combox_punkts.current(randrange(0,len(punkts_to_fill)))
                else:
                    punkts_to_fill = [i.name for i in self.punkts if i.period == period]
                    self.combox_punkts.config(values=punkts_to_fill)
                    self.combox_punkts.current(randrange(0,len(punkts_to_fill)))
            create_combox_punkts(' Все')
                
            # create period_combobox
            periods = sorted([i for i in set(i.period for i in self.punkts)])
            periods.append(' Все')
            self.combox_periods = ttk.Combobox(top_frame,values=periods,justify='center')
            self.combox_periods.current(len(periods)-1)
            self.combox_periods.place(x=470,y=45)
            self.combox_periods.bind("<<ComboboxSelected>>", lambda x: (create_combox_punkts(self.combox_periods.get()),self.update_plot(None)))

            # create buttons
            self.show_punkt_botton = ttk.Button(top_frame, text = 'Просмотреть пункт', command = self.open_show_punkt)
            self.show_punkt_botton.place(x=115, y=41.5)

            # set data and plot it initialy
            self.plot.set_data(self.combox_punkts.get(), self.combox_month.get())
            self.plot.init_plot(bottom_frame)
                

            self.grab_set()
            self.focus_set()

    def open_show_punkt(self):
        self.main.Show_punkt(self.main,self.punkts.get_punkt(self.combox_punkts.get()))
