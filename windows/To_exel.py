import tkinter as tk
import datetime
from tkinter import ttk


class To_Exel(tk.Toplevel):
    def __init__ (self, main):
        self.main = main
        super().__init__ (self.main)
        self.Outputter = self.main.Outputter
        self.Punkts = self.main.Punkts
        self.bind('<Escape>', lambda e: self.destroy())
        self.init_choice()

    def create_Exel_operation(self, date, *names):
        self.Outputter.operational_to_exel(date, *names)

    def create_Exel_forday(self, date, *names):
        self.Outputter.forday_to_exel(date, *names)
              
    def on_entry_click(self,event):
        """function that gets called whenever entry_utv is clicked"""
        if self.entry_utv.get() == 'ШЧУ Шинкаренко':
            self.entry_utv.delete(0, "end")                 # delete all the text in the entry
            self.entry_utv.insert(0, '')                    # Insert blank for user input
            self.entry_utv.configure(style="Black.TEntry")

    def on_entry_click1(self,event):
        """function that gets called whenever entry_set is clicked"""
        if self.entry_set.get() == 'ШЧИ Маленда':
            self.entry_set.delete(0, "end")                 # delete all the text in the entry
            self.entry_set.insert(0, '')                    # Insert blank for user input
            self.entry_set.configure(style="Black.TEntry")  # entry.config(fg = 'black')

    def on_entry_click2(self,event):
        """function that gets called whenever entry_do is clicked"""
        if self.entry_do.get('1.0', tk.END) ==self.text1:
            self.text1=self.entry_do.get('1.0', tk.END) 
            self.entry_do.delete('1.0', tk.END)             # delete all the text in the entry
            self.entry_do.insert(tk.INSERT, self.text2)     # Insert blank for user input
            self.text2=self.entry_do.get('1.0', tk.END)
            self.entry_do.config(fg = 'black')              # entry.config(fg = 'black')
            
    def on_focusout(self,event):
        if self.entry_utv.get() == '':
            self.entry_utv.insert(0, 'ШЧУ Шинкаренко')
            self.entry_utv.configure(style="Red.TEntry")

    def on_focusout1(self,event):
        if self.entry_set.get() == '':
            self.entry_set.insert(0, 'ШЧИ Маленда')
            self.entry_set.configure(style="Red.TEntry")

    def on_focusout2(self,event):
        if self.entry_do.get('1.0', tk.END) == self.text2:
            self.text2=self.entry_do.get('1.0', tk.END)
            self.entry_do.insert(tk.INSERT, self.text1)
            self.entry_do.config(fg = 'gray')

    def init_choice(self):
        self.title("Вывести в Exel")
        self.geometry("500x220+550+250")
        #self.resizable(False,False)
        self.minsize(500,220)
        self.text1=''
        self.text2=''

        style = ttk.Style()
        style.configure("Red.TEntry", foreground="gray")
        style = ttk.Style()
        style.configure("Black.TEntry", foreground="black")

        self.textForUtv= tk.StringVar()
        self.textForSet= tk.StringVar()
        self.textForDo= tk.StringVar()

        self.now1=datetime.datetime.now()
        self.month_association = {' Январь':1,' Февраль':2,' Март':3,' Апрель':4,' Май':5,' Июнь':6,' Июль':7,' Август':8,
                                                        ' Сентябрь':9,' Октябрь':10,' Ноябрь':11,' Декабрь':12}
        
        self.combox_month=ttk.Combobox(self,values=[' Январь',' Февраль',' Март',' Апрель',' Май',' Июнь',' Июль',' Август',
                                                        ' Сентябрь',' Октябрь',' Ноябрь',' Декабрь'])
        self.combox_month.current(self.now1.month-1)
        self.combox_month.place(x=270, y=20)

        years = [i for i in range(self.now1.year-5,self.now1.year+7)]
        self.combox_year=ttk.Combobox(self,values=years)
        self.combox_year.current(years.index(self.now1.year))
        self.combox_year.place(x=270, y=50)

        self.buttonOper=ttk.Button(self,text="Оперативный")
        self.buttonOper.place(x=20, y=170)
        self.buttonOper.bind('<Button-1>', lambda event: self.create_Exel_operation(datetime.datetime(int(self.combox_year.get()), 
                                                                                                self.month_association[self.combox_month.get()],
                                                                                                1), 
                                                                                    self.entry_utv.get(), 
                                                                                    self.entry_set.get(), 
                                                                                    self.entry_do.get('1.0', tk.END) ))
     
        self.buttonFor=ttk.Button(self,text="Четырёхнедельный")
        self.buttonFor.place(x=140, y=170)
        self.buttonFor.bind('<Button-1>', lambda event: self.create_Exel_forday(datetime.datetime(int(self.combox_year.get()), 
                                                                                                self.month_association[self.combox_month.get()],
                                                                                                1),
                                                                            self.entry_utv.get(), 
                                                                            self.entry_set.get(), 
                                                                            self.entry_do.get('1.0', tk.END)))

        label_utv=tk.Label(self, text="Утвердил")
        label_utv.place(x=20, y=20)
        label_set=tk.Label(self, text="Составил")
        label_set.place(x=20, y=50)
        label_do=tk.Label(self, text="Исполнители")
        label_do.place(x=20, y=80)

        
        self.entry_utv=ttk.Entry(self)
        self.entry_utv.insert(0, 'ШЧУ Шинкаренко')
        self.entry_utv.bind('<FocusIn>', self.on_entry_click)
        self.entry_utv.bind('<FocusOut>', self.on_focusout)
        self.entry_utv.configure(style="Red.TEntry")
        self.entry_utv.place(x=100, y=20)
        
        self.entry_set=ttk.Entry(self)
        self.entry_set.insert(0, 'ШЧИ Маленда')
        self.entry_set.bind('<FocusIn>', self.on_entry_click1)
        self.entry_set.bind('<FocusOut>', self.on_focusout1)
        self.entry_set.configure(style="Red.TEntry")
        self.entry_set.place(x=100, y=50)

        self.entry_do=tk.Text(self,height=3,width=35,font='Times_New_Roman 10',wrap=tk.WORD)
        
        self.entry_do.place(x=100, y=80)

        self.grab_set()
        self.focus_set()

   