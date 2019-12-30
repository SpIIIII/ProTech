

class New_Punkt(tk.Toplevel):
    def __init__ (self,root):
        super().__init__ (root)
        self.db=db
        self.main=app
        self.init_child()


    def on_entry_click(self,event):
        """function that gets called whenever entry is clicked"""
        if self.entry_de1.get() == 'п 1.5  ':
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


    def init_child(self):
        self.var = tk.IntVar()
        self.title("Добавить пункт")
        self.geometry("432x411+550+250")
        #self.resizable(False,False)
        self.minsize(432,411)


        style = ttk.Style()
        style.configure("Red.TEntry", foreground="gray")
        style = ttk.Style()
        style.configure("Black.TEntry", foreground="black")
        self.weekday=tk.StringVar()
        self.whatday=tk.StringVar()
        self.whatnumber=tk.StringVar()

        label_desctiption=tk.Label(self, text="Номер пункта")
        label_desctiption.grid(row=1,column=1,sticky = tk.W,  pady=3)#place(x=20,y=20)
        label_desctiption=tk.Label(self, text="Переодичность")
        label_desctiption.grid(row=2,column=1,sticky = tk.W,  pady=3)#place(x=20,y=50)
        label_desctiption=tk.Label(self, text="День выполнения")
        label_desctiption.grid(row=3,column=1,sticky = tk.W, pady=3)#place(x=20,y=80)
        label_year_date=tk.Label(self, text="Месяц")
        label_year_date.grid(row=4,column=1,sticky = tk.W,  pady=3)#place(x=20,y=110)
        label_desctiption=tk.Label(self, text="Инструкция")
        label_desctiption.grid(row=5,column=1,sticky = tk.W,  pady=3)#place(x=20,y=140)
        label_desctiption=tk.Label(self, text="Приказ")
        label_desctiption.grid(row=6,column=1,sticky = tk.W,  pady=3)#place(x=20,y=170)
        label_desctiption=tk.Label(self, text="Исполнитель")
        label_desctiption.grid(row=7,column=1,sticky = tk.W,  pady=3)#place(x=20,y=200)
        label_desctiption=tk.Label(self, text="Оборудование")
        label_desctiption.grid(row=8,column=1,sticky = tk.W,  pady=3)#place(x=20,y=230)
        label_desctiption=tk.Label(self, text="Описание")
        label_desctiption.grid(row=9,column=1,sticky = tk.W,  pady=3)#place(x=20,y=260)

        self.entry_de1=ttk.Entry(self,textvariable =self.whatnumber)
        self.entry_de1.insert(0,'п 1.5  ')
        self.entry_de1.bind('<FocusIn>', self.on_entry_click)
        self.entry_de1.bind('<FocusOut>', self.on_focusout)
        self.entry_de1.configure(style="Red.TEntry")
        self.entry_de1.grid(row=1,column=2,sticky = tk.W,padx=2)#place(x=150,y=20)

        self.combobox1=ttk.Combobox(self,values=[u' ежедневно',u' раз в неделю',u' раз в 2 недели',u' раз в 4 недели'],textvariable=self.weekday)
        self.combobox1.current(0)
        self.combobox1.grid(row=2,column=2,sticky = tk.W,padx=2)#place(x=150,y=50)

        self.combobox2=ttk.Combobox(self,values=[u' пн.',u' вт.',u' ср.',u' чт.',u' пт.'],textvariable =self.whatday)
        self.combobox2.current(0)
        self.combobox2.grid(row=3,column=2,sticky = tk.W,padx=2)#place(x=150,y=80)

        self.comboboxYear=ttk.Combobox(self,values=[u' Январь',u' Февраль',u' Март',u' Апрель',u' Май',u' Июнь',u' Июль',u' Август', u' Сентябрь',u' Октябрь',u' Ноябрь',u' Декабрь'])
        self.comboboxYear.current(0)
        self.comboboxYear.grid(row=4,column=2,sticky = tk.W,padx=2)#place(x=150,y=110)

        self.entryInst=ttk.Entry(self)#textvariable =self.whatnumber)
        self.entryInst.insert(0,'ЦШ 0065  ')
        self.entryInst.bind('<FocusIn>', self.on_entry_click1)
        self.entryInst.bind('<FocusOut>', self.on_focusout1)
        self.entryInst.configure(style="Red.TEntry")
        self.entryInst.grid(row=5,column=2,sticky = tk.W,padx=2)#place(x=150,y=140)

        self.entryComand=ttk.Entry(self)#textvariable =self.whatnumber)
        self.entryComand.insert(0,'(приказ 043-Ц/од)  ')
        self.entryComand.bind('<FocusIn>', self.on_entry_click2)
        self.entryComand.bind('<FocusOut>', self.on_focusout2)
        self.entryComand.configure(style="Red.TEntry")
        self.entryComand.grid(row=6,column=2,sticky = tk.W,padx=2)#place(x=150,y=170)

        self.entryMaker=ttk.Entry(self)#textvariable =self.whatnumber)
        self.entryMaker.insert(0,'ШН  ')
        self.entryMaker.bind('<FocusIn>', self.on_entry_click3)
        self.entryMaker.bind('<FocusOut>', self.on_focusout3)
        self.entryMaker.configure(style="Red.TEntry")
        self.entryMaker.grid(row=7,column=2,sticky = tk.W,padx=2)#place(x=150,y=200)

        self.entryOborud=ttk.Entry(self)#textvariable =self.whatnumber)
        self.entryOborud.insert(0,'Go Global АРМ NE – UniGate  ')
        self.entryOborud.bind('<FocusIn>', self.on_entry_click4)
        self.entryOborud.bind('<FocusOut>', self.on_focusout4)
        self.entryOborud.configure(style="Red.TEntry")
        self.entryOborud.grid(row=8,column=2,sticky = tk.W,padx=2)#place(x=150,y=230)


        def lurker2(event):
            #print("in psate "+ self.selection_get(selection='CLIPBOARD'))
            self.entry_de2.insert("insert", self.selection_get(selection='CLIPBOARD'))
            
        def lurker(event_obj):
            self.clipboard_clear()
            self.clipboard_append(self.entry_de2.get('1.0', tk.END))
            #print("in 2clip "+self.entry_de2.get('1.0', tk.END))


        
        self.entry_de2=tk.Text(self,height=5,width=35,font='Times_New_Roman 10',wrap=tk.WORD)
        self.entry_de2.grid(row=9,column=2,sticky = tk.W,padx=2,columnspan=5)#place(x=150,y=260)
        self.entry_de2.bind('<Control-c>')
        self.entry_de2.bind('<Control-v>')
        self.entry_de2.bind('<Control-igrave>', lurker2)
        self.entry_de2.bind('<Control-ntilde>', lurker)
        

        self.comboboxYear.config(state=tk.DISABLED)
        
        def activateCheck():
            if self.var.get() == 1:          #whenever checked
                self.comboboxYear.config(state=tk.NORMAL)
                self.combobox1.config(values=[u' раз в 3 месяца',u' раз в 6 месяцев',u' раз 12 месяцев'])
                self.combobox1.current(0)

                
               
            elif self.var.get() == 0:        #whenever unchecked
                self.comboboxYear.config(state=tk.DISABLED)
                self.combobox1.config(values=[u' ежедневно',u' раз в неделю',u' раз в 2 недели',u' раз в 4 недели'])
                self.combobox1.current(0)
        
        self.c = tk.Checkbutton(self, text="годовой", variable=self.var,command=activateCheck)
        self.c.grid(row=1,column=3)#place(x=277,y =20)

        
        button_cancel= ttk.Button(self, text='close', command=self.destroy)
        button_cancel.place(x=100,y =377)

        button_del= ttk.Button(self, text='Удалить', command=self.main.view_records1)
        button_del.place(x=270,y =377)
        button_del.bind('<Button-1>', lambda event2: self.db.delet_data(self.entry_de1.get()+' '))



        button_add= ttk.Button(self,text = "add",command=self.main.view_records1)
        button_add.place(x=13,y =377)
        button_add.bind('<Button-1>', lambda event1: self.db.insert_data(self.entry_de1.get()+' ',
                                                                        self.entry_de2.get('1.0', tk.END),
                                                                        self.combobox1.get(),
                                                                        self.combobox2.get(),
                                                                        self.comboboxYear.get(),
                                                                        self.entryInst.get(),
                                                                        self.entryComand.get(),
                                                                        self.entryMaker.get(),
                                                                        self.entryOborud.get(),
                                                                        0
                                                                         ) 
                                                                        )
        



        self.grab_set()
        self.focus_set()
                