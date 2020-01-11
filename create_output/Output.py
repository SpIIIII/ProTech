import config
import xlwt
import os
from typing import List
from datetime import datetime


class Output:
    def __init__(self, punkts):
        self.Punkts = punkts

        if config.IS_WINDOWS:
            self.desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        else:
            self.desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        self.month_association_back = {1:' Январь', 2:' Февраль', 3:' Март', 4:' Апрель', 5:' Май', 6:' Июнь', 7:' Июль', 8:' Август',
                                                        9:' Сентябрь', 10:' Октябрь', 11:' Ноябрь', 12:' Декабрь',}

    def operational_to_exel(self, date:datetime, *names:str)-> None:
        self.calculate_operational(date, *names)

    def fourday_to_exel (self, date:datetime, *names:str)-> None:
        pass
                
    def calculate_operational (self, whatday:datetime, *names:str)-> None:
        now = whatday
        self.month_punkts: List(int,str) = self.Punkts.month_punkts(now, annual=False)
        self.annual_punkts: List(int,str) = self.Punkts.month_punkts(now, annual=True)
        self.create_Exel(self.month_punkts,self.annual_punkts, now, *names)
   
    def create_Exel(self, dayPunkt: List(int,str), yearPunkt: List(int,str), date: datetime, *names)-> None:
        self.x=1
        self.y=1
        self.z=0
        date_for_which = date
        self.names = names

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

        sheet.write_merge(self.l+15,self.l+15, 1, 8, 'Составил: _____________ %s'%self.names[1],font2_1)
       
        for i in dayPunkt:
            # Заполняем ячейку число (Строка, Колонка, Текст, Шрифт)
            sheet.write(self.x+13,1,str(dayPunkt[self.x-1][0]),font3)
            sheet.write(self.x+13,12,'%s'%self.names[2],font3)

            # Заполняем ячейку номура пунктов (Строка, Колонка, Текст, Шрифт)
            sheet.write_merge(self.x+13,self.x+13,2,5,str((dayPunkt[self.x-1][1])),font3)

            # Заполняем ячейку годовой пункт (Строка, Колонка, Текст, Шрифт)
            sheet.write_merge(self.x+13, self.x+13, 6, 6, str(yearPunkt[self.x-1][1]),font3)
            self.x+=1
                    
        #sheet.row(12).height = 20000
        sheet.write_merge(1, 1, 1, 7, 'Утверждаю: ________________%s'%self.names[0], font1)
        sheet.write_merge(2, 2, 1, 5, '«__»_____________ %i г.'%date_for_which.year ,font1)
        sheet.write_merge(5, 5, 6, 8, 'Оперативный план',font2)
        sheet.write_merge(6, 6, 4, 10, 'работы на %s месяц %i года'%(self.month_association_back[date_for_which.month], date_for_which.year), font2)
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
        #print(self.desktop+'/Оперативный %s %i.xls'%(self.combox_month.get(),self.now1.year))
        book.save(self.desktop+'/Оперативный %s %i.xls'%(self.month_association_back[date_for_which.month], date_for_which.year))
