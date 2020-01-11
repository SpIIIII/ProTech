import tkinter as tk
import datetime
import platform
import calendar
import xlwt
import os
from tkinter import ttk


IS_WINDOWS = True if platform.system() == 'Windows' else False

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
              
    def caclulateExelFor(self,dayPunkt,yearPunkt):

        self.punktNumber=[i.name for i in self.Punkts]
        self.textPunktNumber=''
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
        
        sheet.write_merge(5, 5, 1, 23, 'Четырехнедельный план-график технического обслуживания устройств связи на %s %s года бригады цифровой'%(self.combox_month.get(),nowWithMonth.year),font2)
        sheet.write_merge(6, 6, 2, 20, 'связи участка магистральной связи Донецькой дистанции  связи Донецкой железной дороги',font2)
        
        sheet.write_merge(8, 8, 1,9, 'Месяц/день недели',font3)
        sheet.write_merge(9, 11, 1,9, '%s'%self.combox_month.get(),font3)

        sheet.write(12,1, 'Наименовние инструкций',font4)
        sheet.write(12,2, '№ работ из Перечня работ',font4)
        sheet.write(12,3, 'Наименование устройств и наборов работ в комплексах ТО 1С и ТО 2С',font4)
        sheet.write(12,4, 'Периодичность работ',font4)
        sheet.write(12,5, 'Измеритель',font4)
        sheet.write(12,6, 'Норма времени на измерение',font4)
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
        for row in self.Punkts:
            if not row.is_annual():
                sheet.write_merge(z+13, z+15, x,x,row.instruction+'\n'+ row.name +'\n'+row.order,font3)     # fill "Наименование инструкций" column

                sheet.write_merge(z+13, z+15, x+1,x+1,z/3+1,font3)                                          # fill "Номер работ" column

                sheet.row(z+15).height_mismatch = True
                sheet.row(z+15).height = self.WhatDistant(row.description)                                          
                sheet.write_merge(z+13, z+15, x+2,x+2, row.description,font3)                               # fill "Наименование устройств и наборов работ" column

                sheet.write_merge(z+13, z+15, x+3,x+3, row.period,font3)                                    # fill "Периодичность работ" column

                sheet.write_merge(z+13, z+15, x+4,x+4, row.equipment,font3)                                 # fill "Измеритель" column

                sheet.write_merge(z+13, z+15, x+5,x+5,'',font3)                                             # fill "Норма времени" column (curently blank)

                sheet.write_merge(z+13, z+15, x+6,x+6, row.responsible ,font3)                              # fill "Исполнитель" column

                sheet.write_merge(z+13, z+15, x+7,x+7,'',font3)                                             # fill "Колличество обьектов" column (curently blank)

                sheet.write_merge(z+13, z+15, x+8,x+8,'',font3)                                             # fill "Общие затраты труда" column (curently blank)

                self.startday=forNow.weekday()
                e=0
                w=0
                for self.p in range(3):
                    for y in range (14):
                        sheet.write(z+13+self.p,10+y,'',font3)
                    while (10+w+self.startday) <= 23 and e in range(calendar.mdays[forNow.month]):
                        e+=1
                        forNowCor=datetime.datetime(forNow.year,forNow.month,e)
                        if row.is_today(date = forNowCor, annual = False):
                            sheet.write(z+13+self.p,10+self.startday+w,'*',font3)
                        else:
                            sheet.write(z+13+self.p,10+self.startday+w,' ',font3)
                    
                        w+=1
                    w=0
                
                    self.startday=0
                    #print(self.p)
                    self.p=0
                z+=3

        sheet.write_merge(z+15, z+15, 1,5,'Составил: _____________ %s'%self.entry_set.get(),font2)
        
        sheet.portrait = False
        sheet.set_print_scaling(100)
        book.save(self.desktop+'/Четырёхнедельный %s %i.xls'%(self.combox_month.get(),self.now1.year) ) 

    def WhatDistant(self,targetText):
        return (len(targetText)//20+1)*300

    def on_entry_click(self,event):
        """function that gets called whenever entry is clicked"""
        if self.entry_utv.get() == 'ШЧУ Шинкаренко':
            self.entry_utv.delete(0, "end") # delete all the text in the entry
            self.entry_utv.insert(0, '') #Insert blank for user input
            self.entry_utv.configure(style="Black.TEntry")

    def on_entry_click1(self,event):
        if self.entry_set.get() == 'ШЧИ Маленда':
            self.entry_set.delete(0, "end")                 # delete all the text in the entry
            self.entry_set.insert(0, '')                    #Insert blank for user input
            self.entry_set.configure(style="Black.TEntry")  #entry.config(fg = 'black')

    def on_entry_click2(self,event):
        #print(self.text2)
        if self.entry_do.get('1.0', tk.END) ==self.text1:
            self.text1=self.entry_do.get('1.0', tk.END) 
            #print('yes i work')
            self.entry_do.delete('1.0', tk.END) # delete all the text in the entry
            self.entry_do.insert(tk.INSERT, self.text2) #Insert blank for user input
            self.text2=self.entry_do.get('1.0', tk.END)
            self.entry_do.config(fg = 'black')#entry.config(fg = 'black')
            
    def on_focusout(self,event):
        if self.entry_utv.get() == '':
            self.entry_utv.insert(0, 'ШЧУ Шинкаренко')
            self.entry_utv.configure(style="Red.TEntry")

    def on_focusout1(self,event):
        if self.entry_set.get() == '':
            self.entry_set.insert(0, 'ШЧИ Маленда')
            self.entry_set.configure(style="Red.TEntry")

    def on_focusout2(self,event):
        #print(self.text2)
        if self.entry_do.get('1.0', tk.END) == self.text2:
            self.text2=self.entry_do.get('1.0', tk.END)
            #print('yes i work to')
            self.entry_do.insert(tk.INSERT, self.text1)
            self.entry_do.config(fg = 'gray')

    def init_choice(self):
        self.title("Вывести в Exel")
        self.geometry("500x220+550+250")
        #self.resizable(False,False)
        self.minsize(500,220)
        self.text1=''
        self.text2=''
        if IS_WINDOWS:
            self.desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        else:
            self.desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')

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
                                                                                                1), self.entry_utv.get(), self.entry_set.get(), self.entry_do.get('1.0', tk.END) ))
     
        self.buttonFor=ttk.Button(self,text="Четырёхнедельный")
        self.buttonFor.place(x=140, y=170)
        self.buttonFor.bind('<Button-1>', lambda event: self.caclulateExelFor(datetime.datetime(int(self.combox_year.get()), 
                                                                                                self.month_association[self.combox_month.get()],
                                                                                                1),self.now1))

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
        #self.text1=self.entry_do.get('1.0', tk.END)

        self.grab_set()
        self.focus_set()

   