import tkinter as tk
from tkinter import ttk

class Change(tk.Toplevel):
    def __init__ (self, main, onePunkt):
        super().__init__ (main)
        self.main=main
        self.chengebl_punkt = onePunkt
        self.punkts = self.main.punkts
        self.bind('<Escape>', lambda e: self.destroy())
        self.title("Изменение пункта")
        self.geometry("600x350")
        self.minsize(600,350)
        self.resizable(False,False)
        self.init_change(onePunkt)

    def init_change(self,onePunkt):
        
        self.config(bg='white')
        
        def lurker2(event):
            self.entry_de2.insert("insert", self.selection_get(selection='CLIPBOARD'))
            
        def lurker(event_obj):
            self.clipboard_clear()
            self.clipboard_append(self.entry_de2.get('1.0', tk.END))


        association={' пн.':0,' вт.':1,' ср.':2,' чт.':3,' пт.':4}
        association_cicle={' ежедневно':0,' раз в неделю':1,' раз в 2 недели':2,' раз в 4 недели':3,' раз в 3 месяца':4,
                           ' раз в 6 месяцев':5,' раз 12 месяцев':6}
        associationforMonth={' Январь':0,' Февраль':1,' Март':2,' Апрель':3,' Май':4,' Июнь':5,' Июль':6,' Август':7,
                                                        ' Сентябрь':8,' Октябрь':9,' Ноябрь':10,' Декабрь':11}
        

        self.lable_punkt=tk.Label(self, bg = 'white',text="Пункт")
        self.lable_punkt.place(x=15,y=20)
        self.entry_punkt=tk.Label(self, bg='white', text=self.chengebl_punkt.name)
        self.entry_punkt.place(x=100,y=20)

        self.lable_inst=tk.Label(self, bg = 'white',text="Инструкция")
        self.lable_inst.place(x=15,y=50)
        self.entry_inst=ttk.Entry(self)
        self.entry_inst.insert(0,self.chengebl_punkt.instruction)
        self.entry_inst.place(x=100,y=50)

        self.lable_prikaz=tk.Label(self, bg = 'white',text="Приказ")
        self.lable_prikaz.place(x=15,y=80)
        self.entry_prikaz=ttk.Entry(self)
        self.entry_prikaz.insert(0,self.chengebl_punkt.order)
        self.entry_prikaz.place(x=100,y=80)

        self.lable_isp=tk.Label(self, bg = 'white',text="Исполнитель")
        self.lable_isp.place(x=15,y=110)
        self.entry_isp=ttk.Entry(self)
        self.entry_isp.insert(0,self.chengebl_punkt.responsible)
        self.entry_isp.place(x=100,y=110)

        self.lable_obor=tk.Label(self, bg = 'white',text="Оборудование")
        self.lable_obor.place(x=15,y=140)
        self.entry_obor=ttk.Entry(self)
        self.entry_obor.insert(0,self.chengebl_punkt.equipment)
        self.entry_obor.place(x=100,y=140)

        if self.chengebl_punkt.period==' ежедневно' or self.chengebl_punkt.period==' раз в неделю' or self.chengebl_punkt.period==' раз в 2 недели' or self.chengebl_punkt.period==' раз в 4 недели':
            self.lable_punkt=tk.Label(self, bg = 'white',text="Периодичность")
            self.lable_punkt.place(x=240,y=50)
            self.combobox1=ttk.Combobox(self,values=[u' ежедневно',u' раз в неделю',u' раз в 2 недели',u' раз в 4 недели'])
            self.combobox1.current(association_cicle[self.chengebl_punkt.period])
            self.combobox1.place(x=360,y=50)

        self.lable_punkt=tk.Label(self, bg = 'white',text="День недели")
        self.lable_punkt.place(x=240,y=20)
        self.combobox2=ttk.Combobox(self,values=[u' пн.',u' вт.',u' ср.',u' чт.',u' пт.'])
        self.combobox2.current(association[self.chengebl_punkt.day_of_week])
        self.combobox2.place(x=360,y=20)

        self.comboboxYear=ttk.Combobox(self,values=[u' Январь',u' Февраль',u' Март',u' Апрель',u' Май',u' Июнь',u' Июль',u' Август', u' Сентябрь',u' Октябрь',u' Ноябрь',u' Декабрь'])
        self.comboboxYear.current(associationforMonth[self.chengebl_punkt.month])

        self.label_shift=tk.Label(self, bg = 'white',text="Сдвинуть на")
        self.label_shift.place(x=290,y=140)
        self.entry_shift=ttk.Entry(self)
        self.entry_shift.insert(0,self.chengebl_punkt.shift_week)
        self.entry_shift.place(x=360,y=140)
        self.label_shift2=tk.Label(self, bg = 'white',text="неделю")
        self.label_shift2.place(x=460,y=140)

       
        if self.chengebl_punkt.period==' раз в 6 месяцев' or self.chengebl_punkt.period==' раз в 3 месяца' or self.chengebl_punkt.period==' раз 12 месяцев':
            self.lable_punkt=tk.Label(self, bg = 'white',text="Месяц")
            self.lable_punkt.place(x=240,y=80)
            
            self.comboboxYear.place(x=360,y=80)

            self.lable_punkt=tk.Label(self, bg = 'white',text="Периодичность")
            self.lable_punkt.place(x=240,y=50)
            self.combobox1=ttk.Combobox(self,values=[u' раз в 3 месяца',u' раз в 6 месяцев',u' раз 12 месяцев'])
            self.combobox1.current(association_cicle[self.chengebl_punkt.period]-4)
            self.combobox1.place(x=360,y=50)

        button_cancel= ttk.Button(self, text='close', command=self.destroy)
        button_cancel.place(x=130,y =320)

        self.entry_de2=tk.Text(self,height=6,width=50,font='Times_New_Roman 10',wrap=tk.WORD)
        self.entry_de2.grid(row=9,column=2,sticky = tk.W,padx=2,columnspan=5)#place(x=150,y=260)
        self.entry_de2.bind('<Control-c>')
        self.entry_de2.bind('<Control-v>')
        self.entry_de2.bind('<Control-igrave>', lurker2)
        self.entry_de2.bind('<Control-ntilde>', lurker)
        self.entry_de2.insert("insert", self.chengebl_punkt.description)
        self.entry_de2.place(x=15, y=170)

        button_add= ttk.Button(self,text = "Изменить",command=self.main.refresh_tree_view )
        button_add.place(x=13,y =320)
        button_add.bind('<Button-1>', lambda event1: self.chengebl_punkt.update(self.entry_de2.get('1.0', tk.END),
                                                                        self.combobox1.get(),
                                                                        self.combobox2.get(),
                                                                        self.comboboxYear.get(),
                                                                        self.entry_inst.get(),
                                                                        self.entry_prikaz.get(),
                                                                        self.entry_isp.get(),
                                                                        self.entry_obor.get(),
                                                                        self.chengebl_punkt.name,
                                                                        self.entry_shift.get())
                                                                        )
                                                                        
        self.wait_visibility()
        self.grab_set()
        self.focus_set()