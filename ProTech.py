from tkinter import *
from tkinter import messagebox
import textwrap
import os
import tkinter as tk
from tkinter import ttk
import sqlite3
import xlwt
import datetime
#from calendar import monthrange
import calendar
from datetime import timedelta
from updater import update
from version import version


class Main(tk.Frame):

    def __init__ (self, root):
        super().__init__ (root)
        self.db = db
        self.init_main()
        

    
    def init_main(self):
        self.now1=datetime.datetime.now()
        self.version = version.Versions()
        self.updater = update.Update(self.version)
        '''
        association1={' Январь':1,' Февраль':2,' Март':3,' Апрель':4,' Май':5,' Июнь':6,' Июль':7,' Август':8,
                                                        ' Сентябрь':9,' Октябрь':10,' Ноябрь':11,' Декабрь':12}
        '''        
        noneedframe = tk.Frame(bg = "lightgray",bd = 2)
        noneedframe.pack(side=tk.TOP,fill =tk.X)



        bottom_frame = tk.Frame(bd = 2)
        bottom_frame.pack(side=tk.BOTTOM,fill=BOTH, expand=True)

        label_on_root=tk.Label(bottom_frame, text=' Сегодня: '+''.join(self.todayPunkt()),bd=1,relief=SUNKEN,anchor=W)
        label_on_root.pack(side=tk.BOTTOM,fill =tk.X)
        label_on_root.bind('<Button-1>', lambda e:self.open_Show())

        someButton1 = ttk.Button(noneedframe,text="Добавить",command=self.open_dialog)
        someButton1.pack(side="left")
       
        someButton2 = ttk.Button(noneedframe,text="Обновить",command=self.view_records1)
        someButton2.pack(side="left")
        #someButton2.bind('<Button-1>', lambda event2: print(self.db.read_data('п 1.5')))

        someButton3 = ttk.Button(noneedframe,text="Update",command= self.updater.start)
        someButton3.pack(side="left")
        

        someButton3 = ttk.Button(noneedframe,text="в Exel",command=self.open_Choice)#,command = self.caclulateExel)
        someButton3.pack(side="right")
        #someButton3.bind('<Button-1>', lambda event: self.caclulateExel(datetime.datetime(self.now1.year,association1[self.combobox1.get()],1),self.now1))

        
        '''
        self.combobox1=ttk.Combobox(noneedframe,values=[u' Январь',u' Февраль',u' Март',u' Апрель',u' Май',u' Июнь',u' Июль',u' Август',
                                                        u' Сентябрь',u' Октябрь',u' Ноябрь',u' Декабрь'])
        self.combobox1.current(self.now1.month-1)
        self.combobox1.pack(side="right")
        '''
        #print (root.winfo_reqwidth())
    #def paint_tree(self):   
        self.tree=ttk.Treeview(bottom_frame, columns =('ID','description','day','month'),height=15,show='headings')
       
        self.tree.column('ID', width=80,anchor=tk.CENTER)
        self.tree.column('description', width=350,anchor=tk.CENTER)
        self.tree.column('day', width=100,anchor=tk.CENTER)
        self.tree.column('month', width=50,anchor=tk.CENTER)
        
        self.tree.heading('ID', text='номер')
        self.tree.heading('description', text='краткое описание')
        self.tree.heading('day', text='переодичность')
        self.tree.heading('month', text='день')
        #self.tree.bind("<<TreeviewSelect>>",self.fnStockClick)
        self.tree.bind('<Button-3>',self.select)
        self.tree.pack(side=BOTTOM,fill=BOTH, expand=YES)
        self.view_records()
        
        # create a popup menu
        self.aMenu = tk.Menu(self, tearoff=0)
        self.aMenu.add_command(label='Изменить', command=self.hello)
        self.aMenu.add_separator()
        self.aMenu.add_command(label='Удалить', command=self.delete)
        

        self.tree_item = ''

    def select(self, event):
        """action in event of button 3 on tree view"""
        # select row under mouse
        iid = self.tree.identify_row(event.y)
        #print(type(iid), iid)
        if iid:
            # mouse pointer over item
            self.tree.selection_set(iid)
            self.aMenu.post(event.x_root, event.y_root)
            
            
        else:
           pass

    def delete(self):
        item = self.tree.selection()[0]
        #print(self.tree.item(item,'values')[0])
        self.db.delet_data(self.tree.item(item,'values')[0])
        self.view_records1()

    def hello(self):
        item = self.tree.selection()[0]
        mypinkt=self.tree.item(item,'values')[0]
        self.db.c.execute('''SELECT * FROM weekSchedule WHERE id =? ''',(mypinkt,))
        for row in self.db.c.fetchall():
            pass
            #print(row)
        Change(mypinkt)
       

    def popup(self, event):
        #print ("in popUp")
        item = self.tree.selection()[0]
        #print('You clicked on', self.tree.item(item,'values')[0])
        

    def fnStockClick(self,event):
        item = self.tree.selection()[0]
        #print(type(self.tree.item(item,'values')))
        #print('You clicked on', self.tree.item(item,'values'))

    
       
    def view_records(self):
        self.db.c.execute('''SELECT * FROM weekSchedule ''')
        #self.db.c.close()
        for row in self.db.c.fetchall():
            #print(self.db.c.fetchall())
            self.tree.insert('', 'end', values=row)
        
    def view_records1(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        self.db.c.execute('''SELECT * FROM weekSchedule ''')
        for row in self.db.c.fetchall():
            #print(row)
            self.tree.insert('', 'end', values=row)
    
    def refreshTree(self):
        #print('in refreshTree')
        self.tree.delete('номер')

    def todayPunkt(self):
        self.todayToDo=[]
        for row in self.db.c.execute("SELECT id, * FROM weekSchedule"):
            #print('in ToDo',self.calculateOneDay1(row,self.now1))
            if self.calculateOneDay1(row,self.now1):
                self.todayToDo.append(row[1])
                #self.todayToDo.append(' ')
        
        return self.todayToDo


    def calculateOneDay1 (self, rowver, date):
        now= date
        now_day=(now.day)
        now_weekday=(now.weekday())
        now_month=(now.month)
        now_year=(now.year)
        now_week=(now.isocalendar()[1])
        association={' пн.':0,' вт.':1,' ср.':2,' чт.':3,' пт.':4}
        associationforMonth={' Январь':1,' Февраль':2,' Март':3,' Апрель':4,' Май':5,' Июнь':6,' Июль':7,' Август':8,
                                                        ' Сентябрь':9,' Октябрь':10,' Ноябрь':11,' Декабрь':12}
        
        if now_weekday !=6 and now_weekday !=5 :
            #print('in one day',now_week,rowver[3])
            if rowver[3] == ' ежедневно':
                return(True)
                
                        

            elif str(rowver[3]) == str(' раз в неделю'):
                #print(date,'in one day',rowver[4],now_weekday)
                if association[rowver[4]]==now_weekday:
                    #print('i work')
                    return(True)
                   
                            

            elif str(rowver[3]) == str(' раз в 2 недели'):
                if rowver[10]+now_week%2==0:
                    if association[rowver[4]]==now_weekday:
                        return(True)
                       
                                
                                
            elif str(rowver[3]) == str(' раз в 4 недели'):
                if rowver[10]+now_week%4==0:
                    if association[rowver[4]]==now_weekday:
                        return(True)



            elif str(rowver[3]) == str(' раз в 3 месяца'):
                if (rowver[10]+now_week+(4*(13-associationforMonth[rowver[5]])))%13==0:
                    if association[rowver[4]]==now_weekday:
                        #print('in 6 month', associationforMonth[rowver[5]],now_month)
                        return(True)
                       
                                
            
            elif str(rowver[3]) == str(' раз в 6 месяцев'):
                if (rowver[10]+now_week+(4*(13-associationforMonth[rowver[5]])))%26==0:
                    if association[rowver[4]]==now_weekday:
                        #print('in 6 month', associationforMonth[rowver[5]],now_month)
                        return(True)
                    
                                                          
            
            elif str(rowver[3]) == str(' раз 12 месяцев'):
                 if (rowver[10]+now_week+(4*(13-associationforMonth[rowver[5]])))%52==0:
                     if (47+now_week+associationforMonth[rowver[5]]+rowver[10])%52==0:
                        #print('in 12 month', associationforMonth[rowver[5]],now_month)
                        if association[rowver[4]]==now_weekday:
                            return(True)
                           
        return(False)


    def open_dialog(self):
        Child()

    def open_Choice(self):
        Choice()

    def open_Show(self):
        ShowOneDay()


class Change(tk.Toplevel):
    def __init__ (self, onePunkt):
        super().__init__ (root)
        self.main=app
        self.db=db
        self.init_change(onePunkt)

    def init_change(self,onePunkt):
        self.title("Изменение пункта")
        self.geometry("600x350")
        self.minsize(600,350)

        self.db.c.execute('''SELECT * FROM weekSchedule WHERE id =? ''',(onePunkt,))
        self.myPunkts = self.db.c.fetchall()
        for row in self.myPunkts:
            pass
            #print(row)
        def lurker2(event):
            #print("in psate "+ self.selection_get(selection='CLIPBOARD'))
            self.entry_de2.insert("insert", self.selection_get(selection='CLIPBOARD'))
            
        def lurker(event_obj):
            self.clipboard_clear()
            self.clipboard_append(self.entry_de2.get('1.0', END))
            #print("in 2clip "+self.entry_de2.get('1.0', END))


        association={' пн.':0,' вт.':1,' ср.':2,' чт.':3,' пт.':4}
        association_cicle={' ежедневно':0,' раз в неделю':1,' раз в 2 недели':2,' раз в 4 недели':3,' раз в 3 месяца':4,
                           ' раз в 6 месяцев':5,' раз 12 месяцев':6}
        associationforMonth={' Январь':0,' Февраль':1,' Март':2,' Апрель':3,' Май':4,' Июнь':5,' Июль':6,' Август':7,
                                                        ' Сентябрь':8,' Октябрь':9,' Ноябрь':10,' Декабрь':11}
        

        self.lable_punkt=tk.Label(self,text="Пункт")
        self.lable_punkt.place(x=15,y=20)
        self.entry_punkt=ttk.Label(self,text=self.myPunkts[0][0])
        self.entry_punkt.place(x=100,y=20)

        self.lable_inst=tk.Label(self,text="Инструкция")
        self.lable_inst.place(x=15,y=50)
        self.entry_inst=ttk.Entry(self)
        self.entry_inst.insert(0,self.myPunkts[0][5])
        self.entry_inst.place(x=100,y=50)

        self.lable_prikaz=tk.Label(self,text="Приказ")
        self.lable_prikaz.place(x=15,y=80)
        self.entry_prikaz=ttk.Entry(self)
        self.entry_prikaz.insert(0,self.myPunkts[0][6])
        self.entry_prikaz.place(x=100,y=80)

        self.lable_isp=tk.Label(self,text="Исполнитель")
        self.lable_isp.place(x=15,y=110)
        self.entry_isp=ttk.Entry(self)
        self.entry_isp.insert(0,self.myPunkts[0][7])
        self.entry_isp.place(x=100,y=110)

        self.lable_obor=tk.Label(self,text="Оборудование")
        self.lable_obor.place(x=15,y=140)
        self.entry_obor=ttk.Entry(self)
        self.entry_obor.insert(0,self.myPunkts[0][8])
        self.entry_obor.place(x=100,y=140)

        if self.myPunkts[0][2]==' ежедневно' or self.myPunkts[0][2]==' раз в неделю' or self.myPunkts[0][2]==' раз в 2 недели' or self.myPunkts[0][2]==' раз в 4 недели':
            self.lable_punkt=tk.Label(self,text="Периодичность")
            self.lable_punkt.place(x=240,y=50)
            self.combobox1=ttk.Combobox(self,values=[u' ежедневно',u' раз в неделю',u' раз в 2 недели',u' раз в 4 недели'])
            self.combobox1.current(association_cicle[self.myPunkts[0][2]])
            self.combobox1.place(x=360,y=50)

        self.lable_punkt=tk.Label(self,text="День недели")
        self.lable_punkt.place(x=240,y=20)
        self.combobox2=ttk.Combobox(self,values=[u' пн.',u' вт.',u' ср.',u' чт.',u' пт.'])
        self.combobox2.current(association[self.myPunkts[0][3]])
        self.combobox2.place(x=360,y=20)

        self.comboboxYear=ttk.Combobox(self,values=[u' Январь',u' Февраль',u' Март',u' Апрель',u' Май',u' Июнь',u' Июль',u' Август', u' Сентябрь',u' Октябрь',u' Ноябрь',u' Декабрь'])
        self.comboboxYear.current(associationforMonth[self.myPunkts[0][4]])

        self.label_shift=tk.Label(self,text="Сдвинуть на")
        self.label_shift.place(x=290,y=140)
        self.entry_shift=ttk.Entry(self)
        self.entry_shift.insert(0,self.myPunkts[0][9])
        self.entry_shift.place(x=360,y=140)
        self.label_shift2=tk.Label(self,text="неделю")
        self.label_shift2.place(x=460,y=140)

       
        if self.myPunkts[0][2]==' раз в 6 месяцев' or self.myPunkts[0][2]==' раз в 3 месяца' or self.myPunkts[0][2]==' раз 12 месяцев':
            #print (self.myPunkts[0][2])
            self.lable_punkt=tk.Label(self,text="Месяц")
            self.lable_punkt.place(x=240,y=80)
            
            self.comboboxYear.place(x=360,y=80)

            self.lable_punkt=tk.Label(self,text="Периодичность")
            self.lable_punkt.place(x=240,y=50)
            self.combobox1=ttk.Combobox(self,values=[u' раз в 3 месяца',u' раз в 6 месяцев',u' раз 12 месяцев'])
            self.combobox1.current(association_cicle[self.myPunkts[0][2]]-4)
            self.combobox1.place(x=360,y=50)

        button_cancel= ttk.Button(self, text='close', command=self.destroy)
        button_cancel.place(x=120,y =300)

        self.entry_de2=tk.Text(self,height=6,width=50,font='Times_New_Roman 10',wrap=WORD)
        self.entry_de2.grid(row=9,column=2,sticky = W,padx=2,columnspan=5)#place(x=150,y=260)
        self.entry_de2.bind('<Control-c>')
        self.entry_de2.bind('<Control-v>')
        self.entry_de2.bind('<Control-igrave>', lurker2)
        self.entry_de2.bind('<Control-ntilde>', lurker)
        self.entry_de2.insert("insert", self.myPunkts[0][1])
        self.entry_de2.place(x=15, y=170)

        button_add= ttk.Button(self,text = "Изменить",command=self.main.view_records1 )
        button_add.place(x=13,y =300)
        button_add.bind('<Button-1>', lambda event1: self.db.update_data(self.entry_de2.get('1.0', END),
                                                                        self.combobox1.get(),
                                                                        self.combobox2.get(),
                                                                        self.comboboxYear.get(),
                                                                        self.entry_inst.get(),
                                                                        self.entry_prikaz.get(),
                                                                        self.entry_isp.get(),
                                                                        self.entry_obor.get(),
                                                                        self.myPunkts[0][0],
                                                                        self.entry_shift.get()
                                                                         ) 
                                                                        )


class Child(tk.Toplevel):
    def __init__ (self):
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
        self.var = IntVar()
        self.title("Добавить пункт")
        self.geometry("432x411+550+250")
        #self.resizable(False,False)
        self.minsize(432,411)


        style = ttk.Style()
        style.configure("Red.TEntry", foreground="gray")
        style = ttk.Style()
        style.configure("Black.TEntry", foreground="black")
        self.weekday=StringVar()
        self.whatday=StringVar()
        self.whatnumber=StringVar()

        label_desctiption=tk.Label(self, text="Номер пункта")
        label_desctiption.grid(row=1,column=1,sticky = W,  pady=3)#place(x=20,y=20)
        label_desctiption=tk.Label(self, text="Переодичность")
        label_desctiption.grid(row=2,column=1,sticky = W,  pady=3)#place(x=20,y=50)
        label_desctiption=tk.Label(self, text="День выполнения")
        label_desctiption.grid(row=3,column=1,sticky = W, pady=3)#place(x=20,y=80)
        label_year_date=tk.Label(self, text="Месяц")
        label_year_date.grid(row=4,column=1,sticky = W,  pady=3)#place(x=20,y=110)
        label_desctiption=tk.Label(self, text="Инструкция")
        label_desctiption.grid(row=5,column=1,sticky = W,  pady=3)#place(x=20,y=140)
        label_desctiption=tk.Label(self, text="Приказ")
        label_desctiption.grid(row=6,column=1,sticky = W,  pady=3)#place(x=20,y=170)
        label_desctiption=tk.Label(self, text="Исполнитель")
        label_desctiption.grid(row=7,column=1,sticky = W,  pady=3)#place(x=20,y=200)
        label_desctiption=tk.Label(self, text="Оборудование")
        label_desctiption.grid(row=8,column=1,sticky = W,  pady=3)#place(x=20,y=230)
        label_desctiption=tk.Label(self, text="Описание")
        label_desctiption.grid(row=9,column=1,sticky = W,  pady=3)#place(x=20,y=260)

        self.entry_de1=ttk.Entry(self,textvariable =self.whatnumber)
        self.entry_de1.insert(0,'п 1.5  ')
        self.entry_de1.bind('<FocusIn>', self.on_entry_click)
        self.entry_de1.bind('<FocusOut>', self.on_focusout)
        self.entry_de1.configure(style="Red.TEntry")
        self.entry_de1.grid(row=1,column=2,sticky = W,padx=2)#place(x=150,y=20)

        self.combobox1=ttk.Combobox(self,values=[u' ежедневно',u' раз в неделю',u' раз в 2 недели',u' раз в 4 недели'],textvariable=self.weekday)
        self.combobox1.current(0)
        self.combobox1.grid(row=2,column=2,sticky = W,padx=2)#place(x=150,y=50)

        self.combobox2=ttk.Combobox(self,values=[u' пн.',u' вт.',u' ср.',u' чт.',u' пт.'],textvariable =self.whatday)
        self.combobox2.current(0)
        self.combobox2.grid(row=3,column=2,sticky = W,padx=2)#place(x=150,y=80)

        self.comboboxYear=ttk.Combobox(self,values=[u' Январь',u' Февраль',u' Март',u' Апрель',u' Май',u' Июнь',u' Июль',u' Август', u' Сентябрь',u' Октябрь',u' Ноябрь',u' Декабрь'])
        self.comboboxYear.current(0)
        self.comboboxYear.grid(row=4,column=2,sticky = W,padx=2)#place(x=150,y=110)

        self.entryInst=ttk.Entry(self)#textvariable =self.whatnumber)
        self.entryInst.insert(0,'ЦШ 0065  ')
        self.entryInst.bind('<FocusIn>', self.on_entry_click1)
        self.entryInst.bind('<FocusOut>', self.on_focusout1)
        self.entryInst.configure(style="Red.TEntry")
        self.entryInst.grid(row=5,column=2,sticky = W,padx=2)#place(x=150,y=140)

        self.entryComand=ttk.Entry(self)#textvariable =self.whatnumber)
        self.entryComand.insert(0,'(приказ 043-Ц/од)  ')
        self.entryComand.bind('<FocusIn>', self.on_entry_click2)
        self.entryComand.bind('<FocusOut>', self.on_focusout2)
        self.entryComand.configure(style="Red.TEntry")
        self.entryComand.grid(row=6,column=2,sticky = W,padx=2)#place(x=150,y=170)

        self.entryMaker=ttk.Entry(self)#textvariable =self.whatnumber)
        self.entryMaker.insert(0,'ШН  ')
        self.entryMaker.bind('<FocusIn>', self.on_entry_click3)
        self.entryMaker.bind('<FocusOut>', self.on_focusout3)
        self.entryMaker.configure(style="Red.TEntry")
        self.entryMaker.grid(row=7,column=2,sticky = W,padx=2)#place(x=150,y=200)

        self.entryOborud=ttk.Entry(self)#textvariable =self.whatnumber)
        self.entryOborud.insert(0,'Go Global АРМ NE – UniGate  ')
        self.entryOborud.bind('<FocusIn>', self.on_entry_click4)
        self.entryOborud.bind('<FocusOut>', self.on_focusout4)
        self.entryOborud.configure(style="Red.TEntry")
        self.entryOborud.grid(row=8,column=2,sticky = W,padx=2)#place(x=150,y=230)


        def lurker2(event):
            #print("in psate "+ self.selection_get(selection='CLIPBOARD'))
            self.entry_de2.insert("insert", self.selection_get(selection='CLIPBOARD'))
            
        def lurker(event_obj):
            self.clipboard_clear()
            self.clipboard_append(self.entry_de2.get('1.0', END))
            #print("in 2clip "+self.entry_de2.get('1.0', END))


        
        self.entry_de2=tk.Text(self,height=5,width=35,font='Times_New_Roman 10',wrap=WORD)
        self.entry_de2.grid(row=9,column=2,sticky = W,padx=2,columnspan=5)#place(x=150,y=260)
        self.entry_de2.bind('<Control-c>')
        self.entry_de2.bind('<Control-v>')
        self.entry_de2.bind('<Control-igrave>', lurker2)
        self.entry_de2.bind('<Control-ntilde>', lurker)
        

        self.comboboxYear.config(state=DISABLED)
        
        def activateCheck():
            if self.var.get() == 1:          #whenever checked
                self.comboboxYear.config(state=NORMAL)
                self.combobox1.config(values=[u' раз в 3 месяца',u' раз в 6 месяцев',u' раз 12 месяцев'])
                self.combobox1.current(0)

                
               
            elif self.var.get() == 0:        #whenever unchecked
                self.comboboxYear.config(state=DISABLED)
                self.combobox1.config(values=[u' ежедневно',u' раз в неделю',u' раз в 2 недели',u' раз в 4 недели'])
                self.combobox1.current(0)
        
        self.c = Checkbutton(self, text="годовой", variable=self.var,command=activateCheck)
        self.c.grid(row=1,column=3)#place(x=277,y =20)

        
        button_cancel= ttk.Button(self, text='close', command=self.destroy)
        button_cancel.place(x=100,y =377)

        button_del= ttk.Button(self, text='Удалить', command=self.main.view_records1)
        button_del.place(x=270,y =377)
        button_del.bind('<Button-1>', lambda event2: self.db.delet_data(self.entry_de1.get()+' '))

        def mytestFunction(self):
            massagebox.showinfo("","Готово")


        button_add= ttk.Button(self,text = "add",command=self.main.view_records1)
        button_add.place(x=13,y =377)
        button_add.bind('<Button-1>', lambda event1: self.db.insert_data(self.entry_de1.get()+' ',
                                                                        self.entry_de2.get('1.0', END),
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
                
        
class Choice(tk.Toplevel):
    def __init__ (self):
        super().__init__ (root)
        self.db=db
        self.init_choice()

    def caclulateExel(self,whatday,real_now):
        now= whatday
        now_day=(now.day)
        now_weekday=(now.weekday())
        now_month=(now.month)
        now_year=(now.year)
        now_week=(now.isocalendar()[1])
        rnow_weekday=(real_now.weekday())
        association={' пн.':0,' вт.':1,' ср.':2,' чт.':3,' пт.':4}
        associationforMonth={' Январь':1,' Февраль':2,' Март':3,' Апрель':4,' Май':5,' Июнь':6,' Июль':7,' Август':8,
                                                        ' Сентябрь':9,' Октябрь':10,' Ноябрь':11,' Декабрь':12}
        sub_dayly_punkt=[]
        self.daylypunkt=[]
        self.yearPunkt=[]
        self.subYearPunkt=[]
        textVar=''
        textYearVar=''
        #print(range(calendar.mdays[now_month]))
        
        for i in range(calendar.mdays[now_month]):
            now_weekday=(now.weekday())
            now_week=(now.isocalendar()[1])
            #print(now ,now_week)
            now_day=(now.day)
            #print(now_week,now_weekday, now_month,row[1],row[2],row[3],row[4],row[5])
            if now_weekday !=6 and now_weekday !=5 :
                sub_dayly_punkt.append(now_day)
                self.subYearPunkt.append(now_day)
                for row in self.db.c.execute("SELECT id, * FROM weekSchedule"):
                    #print('calculater punkt is '+row[1])
                   
                    if row[3] == ' ежедневно':
                        textVar+='; '+row[1]
                        

                    elif str(row[3]) == str(' раз в неделю'):
                        if association[row[4]]==now_weekday:
                            textVar+='; '+row[1]
                            

                    elif str(row[3]) == str(' раз в 2 недели'):
                        if (now_week+row[10])%2==0:
                            if association[row[4]]==now_weekday:
                                textVar+='; '+row[1]
                                
                                
                    elif str(row[3]) == str(' раз в 4 недели'):
                        if (now_week+row[10])%4==0:
                            if association[row[4]]==now_weekday:
                                textVar+='; '+row[1]
                                

                    elif str(row[3]) == str(' раз в 3 месяца'):
                         if (row[10]+now_week+(4*(13-associationforMonth[row[5]])))%13==0:
                            if association[row[4]]==now_weekday:
                                textYearVar+=row[1]+'\n'

            
                    elif str(row[3]) == str(' раз в 6 месяцев'):
                        if (row[10]+now_week+(4*(13-associationforMonth[row[5]])))%26==0:
                            if association[row[4]]==now_weekday:
                                textYearVar+=row[1]+'\n'
                                                          
            
                    elif str(row[3]) == str(' раз 12 месяцев'):
                        #print('calculater punkt is '+row[1])
                        if associationforMonth[row[5]]==now_month:
                            if (row[10]+now_week+(4*(13-associationforMonth[row[5]])))%52==0:
                                #print('in 12 month', associationforMonth[row[5]],now_month)
                                if association[row[4]]==now_weekday:
                                    textYearVar+=row[1]+'\n'
                
                                
                sub_dayly_punkt.append(textVar)
                self.daylypunkt.append(sub_dayly_punkt)
                self.subYearPunkt.append(textYearVar)
                self.yearPunkt.append(self.subYearPunkt)

            textVar=''
            textYearVar=''
            sub_dayly_punkt=[]
            self.subYearPunkt=[]
            now+=timedelta(1)

        self.CreateExel(self.daylypunkt,self.yearPunkt)
        #print (self.daylypunkt)
        #print(self.yearPunkt)

   
    def CreateExel(self,dayPunkt,yearPunkt):
        self.x=1
        self.y=1
        self.z=0
        # Создаем книку
        book = xlwt.Workbook('utf8')
        
        
        # Создаем шрифт
        font1 = xlwt.easyxf('font: height 240,name Times_New_Roman,colour_index black, bold on,\
    italic off; align: wrap off, vert top, horiz left;')
        font2 = xlwt.easyxf('font: height 280,name Times_New_Roman,colour_index black, bold on,\
    italic off; align: vertical center, horizontal center, wrap off;')
        font2_1 = xlwt.easyxf('font: height 280,name Times_New_Roman,colour_index black, bold on,\
    italic off; align: vertical center, horizontal left, wrap off;')
        font3 = xlwt.easyxf('font: height 240,name Times_New_Roman,colour_index black, bold off,\
    italic off; align: vertical top, horizontal center, wrap on;\
    borders: left thin, right thin, top thin, bottom thin;')
   
        # Добавляем лист
        sheet = book.add_sheet('sheetname',cell_overwrite_ok=True)
        self.l=0
        for i in dayPunkt:
            sheet.row(self.z+14).height_mismatch = True
            sheet.row(self.z+14).height = 1000
            sheet.write_merge(self.z+14,self.z+14, 7, 8, '',font3)
            sheet.write_merge(self.z+14,self.z+14, 9, 10, '',font3)
            sheet.write_merge(self.z+14,self.z+14, 11, 11, '',font3)
            sheet.write_merge(self.z+14,self.z+14, 12, 13, '',font3)
            sheet.write_merge(self.z+14,self.z+14, 14, 14, '',font3)
            self.z+=1
            self.l+=1

        sheet.write_merge(self.l+15,self.l+15, 1, 8, 'Составил: _____________ %s'%self.entry_set.get(),font2_1)
       
        for i in dayPunkt:
            #print(i)
            # Заполняем ячейку (Строка, Колонка, Текст, Шрифт)
            sheet.write(self.x+13,1,str(dayPunkt[self.x-1][0]),font3)
            sheet.write(self.x+13,12,'%s'%self.entry_do.get('1.0', END),font3)
            self.x+=1
        self.x=1
        
        for i in dayPunkt:
            #print(i)
            # Заполняем ячейку (Строка, Колонка, Текст, Шрифт)
            sheet.write_merge(self.x+13,self.x+13,2,5,str((dayPunkt[self.x-1][1])[1:]),font3)
            self.x+=1  
        self.x=1
        for i in yearPunkt:
            #print(i)
            # Заполняем ячейку (Строка, Колонка, Текст, Шрифт)
            sheet.write_merge(self.x+13,self.x+13,6,6,str(yearPunkt[self.x-1][1]),font3)
            self.x+=1
            


        #sheet.row(12).height = 20000
        sheet.write_merge(1, 1, 1, 7, 'Утверждаю: ________________%s'%self.entry_utv.get(),font1)
        sheet.write_merge(2, 2, 1, 5, '«__»_____________ %i г.'%self.now1.year,font1)
        sheet.write_merge(5, 5, 6, 8, 'Оперативный план',font2)
        sheet.write_merge(6, 6, 4, 10, 'работы на %s месяц %i года'%(self.combobox1.get(),self.now1.year ),font2)
        sheet.write_merge(7, 7, 1, 13, 'бригады цифровой связи участка магистральной связи  Донецкой дистанции связи',font2)
        sheet.write_merge(8, 8, 5, 9, 'Донецкой железной дороги',font2)
        sheet.write_merge(10, 13, 1, 1, 'Число месяца',font3)
        sheet.write_merge(10, 11, 2, 6, 'Работы, которые выполняются на участке по плану-графику',font3)
        sheet.write_merge(12, 13, 2, 5, 'Четырехнедельным',font3)
        sheet.write_merge(12, 13, 6, 6, 'годовым',font3)
        sheet.write_merge(10, 13, 7, 8, 'Непредвиденные работы',font3)
        sheet.write_merge(10, 13, 9, 10, 'Невыполнен-ные работы по техническому обслуживанию',font3)
        sheet.write_merge(10, 13, 11, 11, 'Вынужденные изменения в плане',font3)
        sheet.write_merge(10, 13, 12, 13, 'Исполнитель',font3)
        sheet.write_merge(10, 13, 14, 14, 'Отметка о выполнении работ (под-пись)',font3)

        # Высота строки
        sheet.row(11).height_mismatch = True
        sheet.row(11).height = 410

        # Высота строки
        sheet.row(13).height_mismatch = True
        sheet.row(13).height = 760

        # Ширина колонки
        sheet.col(0).width = 1500
        sheet.col(14).width = 3500

        # Лист в положении "альбом"
        sheet.portrait = False

        # Масштабирование при печати
        sheet.set_print_scaling(100)

        #  Сохраняем в файл
        #print(self.desktop+'/Оперативный %s %i.xls'%(self.combobox1.get(),self.now1.year))
        book.save(self.desktop+'/Оперативный %s %i.xls'%(self.combobox1.get(),self.now1.year))
                   
        
    def caclulateExelFor(self,dayPunkt,yearPunkt):

        self.punktNumber=[]
        self.textPunktNumber=''

        for row in self.db.c.execute("SELECT id, * FROM weekSchedule"):
            self.punktNumber.append(row[1])
            #print(row[1])


        self.CreateExelFor(dayPunkt,yearPunkt)


    def CreateExelFor(self,nowWithMonth,realNow):

        forNow=nowWithMonth
        book=xlwt.Workbook('utf8')
        sheet=book.add_sheet('sheetname',cell_overwrite_ok=True)

        font1 = xlwt.easyxf('font: height 240,name Times_New_Roman,colour_index black, bold on, italic off;\
       align: wrap off, vert top, horiz left;')
        font2 = xlwt.easyxf('font: height 260,name Times_New_Roman,colour_index black, bold on, italic off;\
       align: vertical center, horizontal center, wrap off;')
        font3 = xlwt.easyxf('font: height 240,name Times_New_Roman,colour_index black, bold off, italic off;\
     align: vertical top, horizontal center, wrap on;\
    borders: left thin, right thin, top thin, bottom thin;')
        font4 = xlwt.easyxf('font: height 220,name Times New Roman,colour_index black, bold off, italic off;\
     align: vertical top, horizontal center, wrap on;\
    borders: left thin, right thin, top thin, bottom thin;')
        
        sheet.row(12).height_mismatch = True
        sheet.row(12).height = 1500

        sheet.col(0).width = 1000
        for i in range(14):
            sheet.col(i+10).width_mismatch = True
            sheet.col(i+10).width = 900

        sheet.col(1).width_mismatch = True
        sheet.col(1).width = 3200
        sheet.col(2).width_mismatch = True
        sheet.col(2).width = 1800
        sheet.col(3).width_mismatch = True
        sheet.col(3).width = 6000
        sheet.col(4).width_mismatch = True
        sheet.col(4).width = 2100
        sheet.col(5).width_mismatch = True
        sheet.col(5).width = 2000
        sheet.col(6).width_mismatch = True
        sheet.col(6).width = 1800
        sheet.col(7).width_mismatch = True
        sheet.col(7).width = 2000
        sheet.col(8).width_mismatch = True
        sheet.col(8).width = 1800
        sheet.col(9).width_mismatch = True
        sheet.col(9).width = 1500

            
        self.startday=forNow.weekday()
        #print(self.startday)
        e=0
        w=0
        dayvar=1
        for i in range(3):
            for y in range (14):
                sheet.write(9+i,10+y,'',font3)
            while (10+w+self.startday) <= 23 and e in range(calendar.mdays[forNow.month]):
                #print (9+i,10+self.startday+w,'in calendar',e,i)
                
                sheet.write(9+i,10+self.startday+w,dayvar,font4)
                dayvar+=1
                e+=1
                w+=1
            w=0
            self.startday=0

        
        sheet.write_merge(1, 1, 1, 4, 'Согласовано_______________',font1)
        sheet.write_merge(2, 2, 1, 4, '%s'%self.entry_utv.get(),font1)
        sheet.write_merge(3, 3, 1, 4, '«____» _____________%s г.'%realNow.year,font1)
        
        sheet.write_merge(1, 1, 13, 20, 'Утверждено_________________ ',font1)
        sheet.write_merge(2, 2, 13, 20, 'Аношкин В.И.',font1)
        sheet.write_merge(3, 3, 13, 20, '«____» ____________%s г.'%realNow.year,font1)
        
        sheet.write_merge(5, 5, 1, 23, 'Четырехнедельный план-график технического обслуживания устройств связи на %s %s года бригады цифровой'%(self.combobox1.get(),nowWithMonth.year),font2)
        sheet.write_merge(6, 6, 2, 20, 'связи участка магистральной связи Донецькой дистанции  связи Донецкой железной дороги',font2)
        
        sheet.write_merge(8, 8, 1,9, 'Месяц/день недели',font3)
        sheet.write_merge(9, 11, 1,9, '%s'%self.combobox1.get(),font3)

        sheet.write(12,1, 'Наименовние инструкций',font4)
        sheet.write(12,2, '№ работ из Перечня работ',font4)
        sheet.write(12,3, 'Наименование устройств и наборов работ в комплексах ТО 1С и ТО 2С',font4)
        sheet.write(12,4, 'Периодичность работ',font4)
        sheet.write(12,5, 'Измеритель',font4)
        sheet.write(12,6, 'Норма времени на измеритель',font4)
        sheet.write(12,7, 'Исполнитель',font4)
        sheet.write(12,8, 'Количество объектов',font4)
        sheet.write(12,9, 'Общие затраты труда на работу',font4)

        sheet.write(8,10, 'пн',font3)
        sheet.write(8,11, 'вт',font3)
        sheet.write(8,12, 'ср',font3)
        sheet.write(8,13, 'чт',font3)
        sheet.write(8,14, 'пт',font3)
        sheet.write(8,15, 'сб',font3)
        sheet.write(8,16, 'вс',font3)
        sheet.write(8,17, 'пн',font3)
        sheet.write(8,18, 'вт',font3)
        sheet.write(8,19, 'ср',font3)
        sheet.write(8,20, 'чт',font3)
        sheet.write(8,21, 'пт',font3)
        sheet.write(8,22, 'сб',font3)
        sheet.write(8,23, 'вс',font3)
        for t in range(14):
            sheet.write(12,10+t, '',font3)
        x=1
        z=0
        for row in self.db.c.execute("SELECT id, * FROM weekSchedule"):
            if row[3]!=' раз 12 месяцев' and row[3]!=' раз в 6 месяцев':
                sheet.write_merge(z+13, z+15, x,x,row[x+5]+'\n'+ row[x] +'\n'+row[x+6],font3)
                #print('in calc 4   x=',x,row[x])
                z+=3

        x=1
        z=0
        for row in self.db.c.execute("SELECT id, * FROM weekSchedule"):
            if row[3]!=' раз 12 месяцев' and row[3]!=' раз в 6 месяцев':
                sheet.write_merge(z+13, z+15, x+1,x+1,z/3+1,font3)
                #print('in calc 4   x=',x,row[x])
                z+=3        

        x=1
        z=0
        for row in self.db.c.execute("SELECT id, * FROM weekSchedule"):
            if row[3]!=' раз 12 месяцев' and row[3]!=' раз в 6 месяцев':
                sheet.row(z+15).height_mismatch = True
                sheet.row(z+15).height = self.WhatDistant(row[x+1])
                sheet.write_merge(z+13, z+15, x+2,x+2, row[x+1],font3)
                #print('in calc 4   x=',x,row[x])
                z+=3
        x=1
        z=0
        for row in self.db.c.execute("SELECT id, * FROM weekSchedule"):
            if row[3]!=' раз 12 месяцев' and row[3]!=' раз в 6 месяцев':
                sheet.write_merge(z+13, z+15, x+3,x+3, row[x+2],font3)
                #print('in calc 4   x=',x,row[x])
                z+=3
        x=1
        z=0
        for row in self.db.c.execute("SELECT id, * FROM weekSchedule"):
            if row[3]!=' раз 12 месяцев' and row[3]!=' раз в 6 месяцев':
                sheet.write_merge(z+13, z+15, x+4,x+4, row[x+8],font3)
                #print('in calc 4   x=',x,row[x])
                z+=3

        x=1
        z=0
        for row in self.db.c.execute("SELECT id, * FROM weekSchedule"):
            if row[3]!=' раз 12 месяцев' and row[3]!=' раз в 6 месяцев':
                sheet.write_merge(z+13, z+15, x+5,x+5,'',font3)
                #print('in calc 4   x=',x,row[x])
                z+=3

        x=1
        z=0
        for row in self.db.c.execute("SELECT id, * FROM weekSchedule"):
            if row[3]!=' раз 12 месяцев' and row[3]!=' раз в 6 месяцев':
                sheet.write_merge(z+13, z+15, x+6,x+6, row[x+7],font3)
                #print('in calc 4   x=',x,row[x])
                z+=3

        x=1
        z=0
        for row in self.db.c.execute("SELECT id, * FROM weekSchedule"):
            if row[3]!=' раз 12 месяцев' and row[3]!=' раз в 6 месяцев':
                sheet.write_merge(z+13, z+15, x+7,x+7,'',font3)
                #print('in calc 4   x=',x,row[x])
                z+=3

        x=1
        z=0
        for row in self.db.c.execute("SELECT id, * FROM weekSchedule"):
            if row[3]!=' раз 12 месяцев' and row[3]!=' раз в 6 месяцев':
                sheet.write_merge(z+13, z+15, x+8,x+8,'',font3)
                #print('in calc 4   x=',x,row[x])
                z+=3

       
        z=0
        for row in self.db.c.execute("SELECT id, * FROM weekSchedule"):

           if row[3]!=' раз 12 месяцев' and row[3]!=' раз в 6 месяцев':
            
                self.startday=forNow.weekday()
                e=0
                w=0
                for self.p in range(3):
                    #print(self.p)
                    for y in range (14):
                        sheet.write(z+13+self.p,10+y,'',font3)
                    while (10+w+self.startday) <= 23 and e in range(calendar.mdays[forNow.month]):
                        e+=1
                        forNowCor=datetime.datetime(forNow.year,forNow.month,e)
                        #print('in while',forNowCor,e,self.calculateOneDay(row,forNowCor))
                        #print(row[3])
                        if(self.calculateOneDay(row,forNowCor)):
                            sheet.write(z+13+self.p,10+self.startday+w,'*',font3)
                        else:
                            sheet.write(z+13+self.p,10+self.startday+w,' ',font3)
                    
                        w+=1
                    w=0
                
                    self.startday=0
                    #print(self.p)
                    self.p=0
                
                e=0
                z+=3

        sheet.write_merge(z+15, z+15, 1,5,'Составил: _____________ %s'%self.entry_set.get(),font2)
        # print (self.calculateOneDay(self.db.c.execute("SELECT id, * FROM weekSchedule"),forNow))
        
        sheet.portrait = False
        sheet.set_print_scaling(100)
        #print(self.desktop+'/Четырёхнедельный %s %i.xls'%(self.combobox1.get(),self.now1.year))
        book.save(self.desktop+'/Четырёхнедельный %s %i.xls'%(self.combobox1.get(),self.now1.year) ) 

    
    def WhatDistant(self,targetText):
        #print(targetText,len(targetText),len(targetText)//20)
        return (len(targetText)//20+1)*300
 

    def calculateOneDay (self, rowver, date):
        now= date
        now_day=(now.day)
        now_weekday=(now.weekday())
        now_month=(now.month)
        now_year=(now.year)
        now_week=(now.isocalendar()[1])
        association={' пн.':0,' вт.':1,' ср.':2,' чт.':3,' пт.':4}
        associationforMonth={' Январь':1,' Февраль':2,' Март':3,' Апрель':4,' Май':5,' Июнь':6,' Июль':7,' Август':8,
                                                        ' Сентябрь':9,' Октябрь':10,' Ноябрь':11,' Декабрь':12}
        #print('in one day',rowver[3])
        if now_weekday !=6 and now_weekday !=5 :
            if rowver[3] == ' ежедневно':
                return(True)
                
                        

            elif str(rowver[3]) == str(' раз в неделю'):
                #print(date,'in one day',rowver[4],now_weekday)
                if association[rowver[4]]==now_weekday:
                    #print('i work')
                    return(True)
                   
                            

            elif str(rowver[3]) == str(' раз в 2 недели'):
                if (now_week+rowver[10])%2==0:
                    if association[rowver[4]]==now_weekday:
                        return(True)
                       
                                
                                
            elif str(rowver[3]) == str(' раз в 4 недели'):
                if (now_week+rowver[10])%4==0:
                    if association[rowver[4]]==now_weekday:
                        return(True)
                       
                             

            elif str(rowver[3]) == str(' раз в 3 месяца'):
                if (rowver[10]+now_week+(4*(13-associationforMonth[rowver[5]])))%13==0:
                    if association[rowver[4]]==now_weekday:
                        #print('in 6 month', associationforMonth[rowver[5]],now_month)
                        return(True)

            
            elif str(rowver[3]) == str(' раз в 6 месяцев'):
                if (rowver[10]+now_week+(4*(13-associationforMonth[rowver[5]])))%26==0:
                    if association[rowver[4]]==now_weekday:
                        #print('in 6 month', associationforMonth[rowver[5]],now_month)
                        return(True)
                    
                                                          
            
            elif str(rowver[3]) == str(' раз 12 месяцев'):
                if (rowver[10]+now_week+(4*(13-associationforMonth[rowver[5]])))%52==0:
                     if (47+now_week+associationforMonth[rowver[5]]+rowver[10])%52==0:
                        #print('in 12 month', associationforMonth[rowver[5]],now_month)
                        if association[rowver[4]]==now_weekday:
                            return(True)
                           
        return(False)


    def on_entry_click(self,event):
        """function that gets called whenever entry is clicked"""
        if self.entry_utv.get() == 'ШЧУ Шинкаренко':
            self.entry_utv.delete(0, "end") # delete all the text in the entry
            self.entry_utv.insert(0, '') #Insert blank for user input
            self.entry_utv.configure(style="Black.TEntry")
    def on_entry_click1(self,event):
        if self.entry_set.get() == 'ШНС Шипин':
            self.entry_set.delete(0, "end") # delete all the text in the entry
            self.entry_set.insert(0, '') #Insert blank for user input
            self.entry_set.configure(style="Black.TEntry")#entry.config(fg = 'black')
    def on_entry_click2(self,event):
        #print(self.text2)
        if self.entry_do.get('1.0', END) ==self.text1:
            self.text1=self.entry_do.get('1.0', END) 
            #print('yes i work')
            self.entry_do.delete('1.0', END) # delete all the text in the entry
            self.entry_do.insert(INSERT, self.text2) #Insert blank for user input
            self.text2=self.entry_do.get('1.0', END)
            self.entry_do.config(fg = 'black')#entry.config(fg = 'black')
            

    def on_focusout(self,event):
        if self.entry_utv.get() == '':
            self.entry_utv.insert(0, 'ШЧУ Шинкаренко')
            self.entry_utv.configure(style="Red.TEntry")
    def on_focusout1(self,event):
        if self.entry_set.get() == '':
            self.entry_set.insert(0, 'ШНС Шипин')
            self.entry_set.configure(style="Red.TEntry")
    def on_focusout2(self,event):
        #print(self.text2)
        if self.entry_do.get('1.0', END) == self.text2:
            self.text2=self.entry_do.get('1.0', END)
            #print('yes i work to')
            self.entry_do.insert(INSERT, self.text1)
            self.entry_do.config(fg = 'gray')


    def init_choice(self):
        self.title("Вывести в Exel")
        self.geometry("500x220+550+250")
        #self.resizable(False,False)
        self.minsize(500,220)
        self.text1=''
        self.text2=''
        self.desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

        style = ttk.Style()
        style.configure("Red.TEntry", foreground="gray")
        style = ttk.Style()
        style.configure("Black.TEntry", foreground="black")

        self.textForUtv=StringVar()
        self.textForSet=StringVar()
        self.textForDo=StringVar()

        self.now1=datetime.datetime.now()
        association1={' Январь':1,' Февраль':2,' Март':3,' Апрель':4,' Май':5,' Июнь':6,' Июль':7,' Август':8,
                                                        ' Сентябрь':9,' Октябрь':10,' Ноябрь':11,' Декабрь':12}
        
        
        self.combobox1=ttk.Combobox(self,values=[u' Январь',u' Февраль',u' Март',u' Апрель',u' Май',u' Июнь',u' Июль',u' Август',
                                                        u' Сентябрь',u' Октябрь',u' Ноябрь',u' Декабрь'])
        self.combobox1.current(self.now1.month-1)
        self.combobox1.place(x=270,y=20)


        self.buttonOper=ttk.Button(self,text="Оперативный")
        self.buttonOper.place(x=20,y=170)
        self.buttonOper.bind('<Button-1>', lambda event: self.caclulateExel(datetime.datetime(self.now1.year,association1[self.combobox1.get()],1),self.now1))
     
        self.buttonFor=ttk.Button(self,text="Четырёхнедельный")
        self.buttonFor.place(x=140,y=170)
        self.buttonFor.bind('<Button-1>', lambda event: self.caclulateExelFor(datetime.datetime(self.now1.year,association1[self.combobox1.get()],1),self.now1))

        label_utv=tk.Label(self, text="Утвердил")
        label_utv.place(x=20,y=20)
        label_set=tk.Label(self, text="Составил")
        label_set.place(x=20,y=50)
        label_do=tk.Label(self, text="Исполнители")
        label_do.place(x=20,y=80)

        
        self.entry_utv=ttk.Entry(self)
        self.entry_utv.insert(0, 'ШЧУ Шинкаренко')
        self.entry_utv.bind('<FocusIn>', self.on_entry_click)
        self.entry_utv.bind('<FocusOut>', self.on_focusout)
        self.entry_utv.configure(style="Red.TEntry")
        self.entry_utv.place(x=100,y=20)
        
        self.entry_set=ttk.Entry(self)
        self.entry_set.insert(0, 'ШНС Шипин')
        self.entry_set.bind('<FocusIn>', self.on_entry_click1)
        self.entry_set.bind('<FocusOut>', self.on_focusout1)
        self.entry_set.configure(style="Red.TEntry")
        self.entry_set.place(x=100,y=50)

        self.entry_do=tk.Text(self,height=3,width=35,font='Times_New_Roman 10',wrap=WORD)
        
        self.entry_do.place(x=100,y=80)
        #self.text1=self.entry_do.get('1.0', END)

        self.grab_set()
        self.focus_set()


class ShowOneDay(tk.Toplevel):
    
    def __init__ (self):
        super().__init__ (root)
        self.main=app
        self.db=db
        self.show_onedaypunkt()
        
    

    def myWrap(self,string, lenght=8):
        return '\n'.join(textwrap.wrap(string, lenght))

    
    def show_onedaypunkt (self):
        self.title("Вывести в Exel")
        self.geometry("400x600")

        self.style=ttk.Style(self)
        self.style.configure('mystyle.Treeview',rowheight=110)
        
        self.sctribeTree=ttk.Treeview(self,columns=('id','description'),height=40,show='headings',style="mystyle.Treeview")
       
        self.sctribeTree.column('id',width=60,anchor=tk.N)
        self.sctribeTree.column('description',width=340,anchor=tk.N)
        self.sctribeTree.heading('id',text='пункт')
        self.sctribeTree.heading('description',text='описание')
        self.sctribeTree.pack(side=BOTTOM,fill=BOTH, expand=YES)

        self.scrollbar = ttk.Scrollbar(self,orient='vertical',command=self.sctribeTree.yview)
        self.scrollbar.pack( side = RIGHT, fill = Y )
         
        
        self.sctribeTree.configure(yscrollcommand=self.scrollbar.set)
        
        i=0
        print(self.main.todayPunkt())
        for x in self.main.todayPunkt():
            item = self.sctribeTree.insert("", "end", values=(x, '\n'.join(textwrap.wrap(str(db.read_data(str(x)))[3:-6], 45))))
            

            i+=1
        
        self.grab_set()
        self.focus_set()

        

class DB:
    def __init__(self):
        self.conn=sqlite3.connect('weekSchedule.db')
        self.c = self.conn.cursor()

        self.c.execute('''CREATE TABLE IF NOT EXISTS weekSchedule (id text primary key,
                        description text, whatweek text, whatday text, yearMonth text,
                        instruction text, comand text, Maker text, equipment text, shiftweek integer)''')
        self.c.execute('''select * from weekSchedule''')
        self.conn.commit()

               
    def insert_data(self, num, description, whenW, whenD,yearM,inst,coma,make,equip,number):
        
        #print (num, description, whenW, whenD,yearM)
        self.c.execute('''INSERT INTO weekSchedule (id, description, whatweek, whatday, yearMonth, instruction, comand, Maker, equipment, shiftweek) 
                          VALUES (?,?,?,?,?,?,?,?,?,?)''',(num, description, whenW, whenD,yearM,inst,coma,make,equip,number))
        self.conn.commit()

    def delet_data(self, n):
        self.c.execute('''DELETE FROM weekSchedule WHERE id =? ''',(n,))
        self.conn.commit()

    def update_data(self, description, whenW, whenD,yearM,inst,coma,make,equip,num,number):
        self.c.execute('''UPDATE weekSchedule SET description = ?, whatweek = ?, whatday = ?, yearMonth = ?, instruction = ?, comand = ?, Maker = ?, equipment = ?, shiftweek = ? WHERE id = ?''',(description, whenW, whenD, yearM, inst, coma, make, equip, number, num,))
        self.conn.commit()
        
    def read_data(self,num):
        self.c.execute('''SELECT description FROM weekSchedule WHERE id =?''',(num,))
        #print('in read',self.c.fetchall())
        return self.c.fetchall()
       
    def __del__(self):     
        self.conn.close()

   


if __name__ ==  "__main__":
    root=tk.Tk()
    db=DB()

    app = Main (root)
    app.pack()
    root.title("Техпроцесс")
    root.geometry("580x350+300+220")
    #root.resizable(False,False)
    
    root.minsize(580,350)
    root.mainloop()


