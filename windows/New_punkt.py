import tkinter as tk
from tkinter import ttk

class New_Punkt(tk.Toplevel):

    def __init__ (self, main):
        self.main = main
        super().__init__ (self.main)
        self.Punkts = self.main.Punkts
        self.bind('<Escape>', lambda e: self.destroy())
        self.init_new_punkt()


    def on_entry_click(self,event):
        """function that gets called whenever entry is clicked"""
        if self.entry_de1.get() == 'п 1.5 ':
            self.entry_de1.delete(0, "end") # delete all the text in the entry
            self.entry_de1.insert(0, '') #Insert blank for user input
            self.entry_de1.configure(style="Black.TEntry")
            
    def on_focusout(self,event):
        if self.entry_de1.get() == '':
            self.entry_de1.insert(0, 'п 1.5  ')
            self.entry_de1.configure(style="Red.TEntry")

    def on_entry_click1(self,event):
        """function that gets called whenever entry is clicked"""
        if self.entryInst.get() == 'ЦШ 0065  ':
            self.entryInst.delete(0, "end") # delete all the text in the entry
            self.entryInst.insert(0, '') #Insert blank for user input
            self.entryInst.configure(style="Black.TEntry")
    def on_focusout1(self,event):
        if self.entryInst.get() == '':
            self.entryInst.insert(0, 'ЦШ 0065  ')
            self.entryInst.configure(style="Red.TEntry")

    def on_entry_click2(self,event):
        """function that gets called whenever entry is clicked"""
        if self.entryComand.get() == '(приказ 043-Ц/од)  ':
            self.entryComand.delete(0, "end") # delete all the text in the entry
            self.entryComand.insert(0, '') #Insert blank for user input
            self.entryComand.configure(style="Black.TEntry")
    def on_focusout2(self,event):
        if self.entryComand.get() == '':
            self.entryComand.insert(0, '(приказ 043-Ц/од)  ')
            self.entryComand.configure(style="Red.TEntry")
            
    def on_entry_click3(self,event):
        """function that gets called whenever entry is clicked"""
        if self.entryMaker.get() == 'ШН  ':
            self.entryMaker.delete(0, "end") # delete all the text in the entry
            self.entryMaker.insert(0, '') #Insert blank for user input
            self.entryMaker.configure(style="Black.TEntry")
    def on_focusout3(self,event):
        if self.entryMaker.get() == '':
            self.entryMaker.insert(0, 'ШН  ')
            self.entryMaker.configure(style="Red.TEntry")
            
    def on_entry_click4(self,event):
        """function that gets called whenever entry is clicked"""
        if self.entryOborud.get() == 'Go Global АРМ NE – UniGate  ':
            self.entryOborud.delete(0, "end") # delete all the text in the entry
            self.entryOborud.insert(0, '') #Insert blank for user input
            self.entryOborud.configure(style="Black.TEntry")
    def on_focusout4(self,event):
        if self.entryOborud.get() == '':
            self.entryOborud.insert(0, 'Go Global АРМ NE – UniGate  ')
            self.entryOborud.configure(style="Red.TEntry")

    def init_new_punkt(self):
        self.var = tk.IntVar()
        self.title("Добавить пункт")
        self.geometry("432x411+550+250")
        self.config(background = "white")
        #self.resizable(False,False)
        self.minsize(432,411)

        style = ttk.Style()
        style.configure("Red.TEntry", foreground="gray")
        style = ttk.Style()
        style.configure("Black.TEntry", foreground="black")
        
        self.weekday = tk.StringVar()
        self.whatday = tk.StringVar()
        self.whatnumber = tk.StringVar()

        label_desctiption = tk.Label(self, background = "white", text="Номер пункта")
        label_desctiption.grid(row=1, column=1, sticky=tk.W, pady=3)
        label_desctiption = tk.Label(self, background = "white", text="Переодичность")
        label_desctiption.grid(row=2, column=1, sticky=tk.W, pady=3)
        label_desctiption = tk.Label(self, background = "white", text="День выполнения")
        label_desctiption.grid(row=3, column=1, sticky=tk.W, pady=3)
        label_year_date = tk.Label(self, background = "white", text="Месяц")
        label_year_date.grid(row=4, column=1, sticky=tk.W, pady=3)
        label_desctiption = tk.Label(self, background = "white", text="Инструкция")
        label_desctiption.grid(row=5, column=1, sticky=tk.W, pady=3)
        label_desctiption = tk.Label(self, background = "white", text="Приказ")
        label_desctiption.grid(row=6, column=1, sticky=tk.W, pady=3)
        label_desctiption = tk.Label(self, background = "white", text="Исполнитель")
        label_desctiption.grid(row=7, column=1, sticky=tk.W, pady=3)
        label_desctiption = tk.Label(self, background = "white", text="Оборудование")
        label_desctiption.grid(row=8, column=1, sticky=tk.W, pady=3)
        label_desctiption = tk.Label(self, background = "white", text="Описание")
        label_desctiption.grid(row=9, column=1, sticky=tk.W, pady=3)

        self.entry_de1 = ttk.Entry(self, textvariable =self.whatnumber)
        self.entry_de1.insert(0, 'п 1.5 ')
        self.entry_de1.bind('<FocusIn>', self.on_entry_click)
        self.entry_de1.bind('<FocusOut>', self.on_focusout)
        self.entry_de1.configure(style="Red.TEntry")
        self.entry_de1.grid(row=1, column=2, sticky=tk.W, padx=2)

        self.combobox1 = ttk.Combobox(self,values=[' ежедневно',' раз в неделю',' раз в 2 недели',' раз в 4 недели'], textvariable=self.weekday)
        self.combobox1.current(0)
        self.combobox1.grid(row=2, column=2, sticky=tk.W, padx=2)

        self.combobox2 = ttk.Combobox(self,values=[' пн.',' вт.',' ср.',' чт.',' пт.'], textvariable=self.whatday)
        self.combobox2.current(0)
        self.combobox2.grid(row=3, column=2, sticky=tk.W, padx=2)

        self.comboboxYear = ttk.Combobox(self,values=[' Январь',' Февраль',' Март',' Апрель',' Май',' Июнь',' Июль',
                                                        ' Август', ' Сентябрь',' Октябрь',' Ноябрь',' Декабрь'])
        self.comboboxYear.current(0)
        self.comboboxYear.grid(row=4, column=2, sticky=tk.W, padx=2)

        self.entryInst = ttk.Entry(self)
        self.entryInst.insert(0,'ЦШ 0065  ')
        self.entryInst.bind('<FocusIn>', self.on_entry_click1)
        self.entryInst.bind('<FocusOut>', self.on_focusout1)
        self.entryInst.configure(style="Red.TEntry")
        self.entryInst.grid(row=5, column=2, sticky=tk.W, padx=2)

        self.entryComand = ttk.Entry(self)
        self.entryComand.insert(0,'(приказ 043-Ц/од)  ')
        self.entryComand.bind('<FocusIn>', self.on_entry_click2)
        self.entryComand.bind('<FocusOut>', self.on_focusout2)
        self.entryComand.configure(style="Red.TEntry")
        self.entryComand.grid(row=6,column=2,sticky = tk.W,padx=2)

        self.entryMaker = ttk.Entry(self)
        self.entryMaker.insert(0,'ШН  ')
        self.entryMaker.bind('<FocusIn>', self.on_entry_click3)
        self.entryMaker.bind('<FocusOut>', self.on_focusout3)
        self.entryMaker.configure(style="Red.TEntry")
        self.entryMaker.grid(row=7, column=2, sticky=tk.W,padx=2)

        self.entryOborud = ttk.Entry(self)
        self.entryOborud.insert(0, 'Go Global АРМ NE – UniGate  ')
        self.entryOborud.bind('<FocusIn>', self.on_entry_click4)
        self.entryOborud.bind('<FocusOut>', self.on_focusout4)
        self.entryOborud.configure(style="Red.TEntry")
        self.entryOborud.grid(row=8, column=2, sticky=tk.W, padx=2)


        def lurker2(event):
            self.entry_de2.insert("insert", self.selection_get(selection='CLIPBOARD'))
            
        def lurker(event_obj):
            self.clipboard_clear()
            self.clipboard_append(self.entry_de2.get('1.0', tk.END))
        
        self.entry_de2 = tk.Text(self,height=5,width=35,font='Times_New_Roman 10',wrap=tk.WORD)
        self.entry_de2.grid(row=9,column=2,sticky = tk.W,padx=2,columnspan=5)
        self.entry_de2.bind('<Control-c>')
        self.entry_de2.bind('<Control-v>')
        self.entry_de2.bind('<Control-igrave>', lurker2)
        self.entry_de2.bind('<Control-ntilde>', lurker)
        
        self.comboboxYear.config(state=tk.DISABLED)
        
        def activateCheck():
            if self.var.get() == 1:          #whenever checked
                self.comboboxYear.config(state=tk.NORMAL)
                self.combobox1.config(values=[' раз в 3 месяца',' раз в 6 месяцев',' раз 12 месяцев'])
                self.combobox1.current(0)

            elif self.var.get() == 0:        #whenever unchecked
                self.comboboxYear.config(state=tk.DISABLED)
                self.combobox1.config(values=[' ежедневно',' раз в неделю',' раз в 2 недели',' раз в 4 недели'])
                self.combobox1.current(0)
        
        self.c = tk.Checkbutton(self, background="white", text="годовой", variable=self.var,command=activateCheck)
        self.c.grid(row=1,column=3)#place(x=277,y =20)

        button_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        button_cancel.place(x=100,y =377)

        button_del = ttk.Button(self, text='Удалить', command= lambda:(self.Punkts.delete_punkt_by_name(self.entry_de1.get()+' '),self.main.refresh_tree_view(),self.Punkts.re_read()))
        button_del.place(x=270,y =377)

        button_add = ttk.Button(self,text = "Добавить",command= lambda :(self.main.refresh_tree_view(),self.Punkts.re_read()))
        button_add.place(x=13,y =377)
        button_add.bind('<Button-1>', lambda event1: self.Punkts.insert_punkt(self.entry_de1.get()+' ',
                                                                        self.entry_de2.get('1.0', tk.END),
                                                                        self.combobox1.get(),
                                                                        self.combobox2.get(),
                                                                        self.comboboxYear.get(),
                                                                        self.entryInst.get(),
                                                                        self.entryComand.get(),
                                                                        self.entryMaker.get(),
                                                                        self.entryOborud.get(),
                                                                        0))

        self.grab_set()
        self.focus_set()
  