import tkinter as tk
import platform
import textwrap
import datetime
import calendar
import sqlite3
import xlwt
import os

from tkinter import ttk
from punkts import Punkts
from updater import update
from version import Version
from datetime import timedelta
from tkinter import messagebox
from windows import Show_one_day, Change_punkt ,New_punkt




class Main(tk.Frame):

    def __init__ (self, root):
        super().__init__ (root)
        self.db = db
        self.version = Version.Versions()
        self.punkts = Punkts.Punkts(db)
        self.init_main()
        
        
    def init_main(self):

        self.now1 = datetime.datetime.now()
        
        self.updater = update.Update(self.version)
        '''
        association1={' Январь':1,' Февраль':2,' Март':3,' Апрель':4,' Май':5,' Июнь':6,' Июль':7,' Август':8,
                                                        ' Сентябрь':9,' Октябрь':10,' Ноябрь':11,' Декабрь':12}
        '''  
        # Draw Frames    
        main_frame = tk.Frame(bd = 2)
        main_frame.pack(side=tk.BOTTOM,fill=tk.BOTH, expand=True)

        # Draw MenuBar
        menubar = tk.Menu()
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Добавить пункт", command=self.add_new_punkt)
        filemenu.add_command(label="Обновить список", command=self.refresh_tree_view)
        filemenu.add_command(label="в Exel", command=self.open_To_Exel)
        # filemenu.add_command(label="test", command=self.db.db_to_class)
        filemenu.add_separator()
        filemenu.add_command(label="Выход", command=root.quit)

        programmenu = tk.Menu(menubar, tearoff=0)
        programmenu.add_command(label='Обновить программу', command=self.updater.start)
        
        menubar.add_cascade(label="Файл", menu=filemenu)
        menubar.add_cascade(label="Программа", menu=programmenu)
        root.config(menu=menubar)

        # Draw Labels
        label_on_root=tk.Label(main_frame, text=' Сегодня: '+''.join(self.punkts.today_punkts(name_only = True)),bd=1,relief=tk.SUNKEN,anchor=tk.W)
        label_on_root.pack(side=tk.BOTTOM,fill =tk.X)
        label_on_root.bind('<Button-1>', lambda e:self.open_Show())
        
        # Draw TreeView      
        self.tree=ttk.Treeview(main_frame, columns =('ID','description','day','month'),height=15,show='headings')
       
        self.tree.column('ID', width=80,anchor=tk.CENTER)
        self.tree.column('description', width=350,anchor=tk.CENTER)
        self.tree.column('day', width=100,anchor=tk.CENTER)
        self.tree.column('month', width=50,anchor=tk.CENTER)
        
        self.tree.heading('ID', text='номер')
        self.tree.heading('description', text='краткое описание')
        self.tree.heading('day', text='переодичность')
        self.tree.heading('month', text='день')
        self.tree.bind('<Button-3>',self.select)
        self.tree.pack(side=tk.BOTTOM,fill=tk.BOTH, expand=tk.YES)
        self.fill_tree_view()
        
        # Create a popup menu
        self.aMenu = tk.Menu(self, tearoff=0)
        self.aMenu.add_command(label='Изменить', command=self.change_selected_punkt)
        self.aMenu.add_command(label='Добавить', command=self.add_new_punkt)
        self.aMenu.add_separator()
        self.aMenu.add_command(label='Удалить', command=self.delete)

        self.tree_item = ''

    def select(self, event):
        """action in event of button 3 on tree view"""
        # select row under mouse
        iid = self.tree.identify_row(event.y)
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
        self.refresh_tree_view()

    def change_selected_punkt(self):
        item = self.tree.selection()[0]
        punkt_name = self.tree.item(item,'values')[0]
        Change_punkt.Change(self.punkts.get_punkts(punkt_name), self.punkts, self, root) 
       
    def fill_tree_view(self):
        for row in self.punkts.re_read():
            self.tree.insert('', 'end', values=(row.name,row.description,row.period,row.day_of_week))
        
    def refresh_tree_view(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.fill_tree_view()

    def add_new_punkt(self):
        New_punkt.New_Punkt(self.punkts, self, root)

    def open_To_Exel(self):
        To_Exel(root,self.punkts)

    def open_Show(self):
        Show_one_day.ShowOneDay(root, self.punkts)
             
        
class To_Exel(tk.Toplevel):
    def __init__ (self, root, punkts):
        super().__init__ (root)
        self.punkts = punkts
        self.db=db
        self.init_choice()

    def caclulateExel(self,whatday,real_now):
        now= whatday
        self.month_punkts = self.punkts.month_punkts(now,annual=False)
        self.annual_punkts = self.punkts.month_punkts(now,annual=True)
        self.CreateExel(self.month_punkts,self.annual_punkts)
   
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
            # Заполняем ячейку число (Строка, Колонка, Текст, Шрифт)
            sheet.write(self.x+13,1,str(dayPunkt[self.x-1][0]),font3)
            sheet.write(self.x+13,12,'%s'%self.entry_do.get('1.0', tk.END),font3)
            self.x+=1
        self.x=1
        
        for i in dayPunkt:
            # Заполняем ячейку номура пунктов (Строка, Колонка, Текст, Шрифт)
            sheet.write_merge(self.x+13,self.x+13,2,5,str((dayPunkt[self.x-1][1])),font3)
            self.x+=1  
        self.x=1

        for i in yearPunkt:
            # Заполняем ячейку годовой пункт (Строка, Колонка, Текст, Шрифт)
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
        print(self.punktNumber)


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
                z+=3

        x=1
        z=0
        for row in self.db.c.execute("SELECT id, * FROM weekSchedule"):
            if row[3]!=' раз 12 месяцев' and row[3]!=' раз в 6 месяцев':
                sheet.write_merge(z+13, z+15, x+8,x+8,'',font3)
                z+=3

       
        z=0
        for row in self.db.c.execute("SELECT id, * FROM weekSchedule"):

           if row[3]!=' раз 12 месяцев' and row[3]!=' раз в 6 месяцев':
            
                self.startday=forNow.weekday()
                e=0
                w=0
                for self.p in range(3):
                    for y in range (14):
                        sheet.write(z+13+self.p,10+y,'',font3)
                    while (10+w+self.startday) <= 23 and e in range(calendar.mdays[forNow.month]):
                        e+=1
                        forNowCor=datetime.datetime(forNow.year,forNow.month,e)
                        if(calculateOneDay(row,forNowCor)):
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
        
        sheet.portrait = False
        sheet.set_print_scaling(100)
        book.save(self.desktop+'/Четырёхнедельный %s %i.xls'%(self.combobox1.get(),self.now1.year) ) 

    
    def WhatDistant(self,targetText):
        return (len(targetText)//20+1)*300

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
            self.entry_set.insert(0, 'ШНС Шипин')
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
        association1={' Январь':1,' Февраль':2,' Март':3,' Апрель':4,' Май':5,' Июнь':6,' Июль':7,' Август':8,
                                                        ' Сентябрь':9,' Октябрь':10,' Ноябрь':11,' Декабрь':12}
        
        
        self.combobox1=ttk.Combobox(self,values=[u' Январь',u' Февраль',u' Март',u' Апрель',u' Май',u' Июнь',u' Июль',u' Август',
                                                        u' Сентябрь',u' Октябрь',u' Ноябрь',u' Декабрь'])
        self.combobox1.current(self.now1.month-1)
        self.combobox1.place(x=270,y=20)


        self.buttonOper=ttk.Button(self,text="Оперативный")
        self.buttonOper.place(x=20,y=170)
        self.buttonOper.bind('<Button-1>', lambda event: self.caclulateExel(datetime.datetime(self.now1.year,association1[self.combobox1.get()],1), self.now1))
     
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

        self.entry_do=tk.Text(self,height=3,width=35,font='Times_New_Roman 10',wrap=tk.WORD)
        
        self.entry_do.place(x=100,y=80)
        #self.text1=self.entry_do.get('1.0', tk.END)

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
        self.c.execute('''INSERT INTO weekSchedule (id, description, whatweek, whatday, yearMonth, instruction, comand, Maker, equipment, shiftweek) 
                          VALUES (?,?,?,?,?,?,?,?,?,?)''',(num, description, whenW, whenD,yearM,inst,coma,make,equip,number))
        self.conn.commit()

    def delet_data(self, n):
        self.c.execute('''DELETE FROM weekSchedule WHERE id =? ''',(n,))
        self.conn.commit()

    def update_data(self, description, whenW, whenD, yearM, inst, coma, make, equip, num, number):
        self.c.execute('''UPDATE weekSchedule SET description = ?, whatweek = ?, whatday = ?, yearMonth = ?, \
            instruction = ?, comand = ?, Maker = ?, equipment = ?, shiftweek = ? WHERE id = ?''',
        (description, whenW, whenD, yearM, inst, coma, make, equip, number, num,))
        self.conn.commit()
        
    def read_data(self,num):
        self.c.execute('''SELECT description FROM weekSchedule WHERE id =?''',(num,))
        return self.c.fetchall()

        
    def __del__(self):     
        self.conn.close()

   

def calculateOneDay (rowver, date):
        now = date        
        now_weekday=(now.weekday())       
        
        now_week=(now.isocalendar()[1])
        association={' пн.':0,' вт.':1,' ср.':2,' чт.':3,' пт.':4}
        associationforMonth={' Январь':1,' Февраль':2,' Март':3,' Апрель':4,' Май':5,' Июнь':6,' Июль':7,' Август':8,
                                                        ' Сентябрь':9,' Октябрь':10,' Ноябрь':11,' Декабрь':12}
        if now_weekday !=6 and now_weekday !=5 :
            if rowver[3] == ' ежедневно':
                return(True)

            elif str(rowver[3]) == str(' раз в неделю'):
                if association[rowver[4]]==now_weekday:
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
                        return(True)
            
            elif str(rowver[3]) == str(' раз в 6 месяцев'):
                if (rowver[10]+now_week+(4*(13-associationforMonth[rowver[5]])))%26==0:
                    if association[rowver[4]]==now_weekday:
                        return(True)                  
            
            elif str(rowver[3]) == str(' раз 12 месяцев'):
                if (rowver[10]+now_week+(4*(13-associationforMonth[rowver[5]])))%52==0:
                     if (47+now_week+associationforMonth[rowver[5]]+rowver[10])%52==0:
                        if association[rowver[4]]==now_weekday:
                            return(True)
                           
        return(False)


if __name__ ==  "__main__":
    IS_WINDOWS = True if platform.system() == 'Windows' else False
    root=tk.Tk()
    db=DB()
    app = Main(root)
    app.pack()
    root.title("Техпроцесс")
    root.geometry("580x350+300+220")
    #root.resizable(False,False)
    
    root.minsize(580,350)
    root.mainloop()


