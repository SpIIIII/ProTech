import calendar
import config
import xlwt
import os
from typing import List
from datetime import datetime
from collections import Counter

class Output:
    def __init__(self, punkts, linePunkts, certPunkts):
        self.Punkts = punkts
        self.LinePunkts = linePunkts
        self.CertPunkts = certPunkts

        if config.IS_WINDOWS:
            self.desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        else:
            self.desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        self.month_association_back = {1:' Январь', 2:' Февраль', 3:' Март', 4:' Апрель', 5:' Май', 6:' Июнь', 7:' Июль', 8:' Август',
                                                        9:' Сентябрь', 10:' Октябрь', 11:' Ноябрь', 12:' Декабрь',}

    def operational_to_exel(self, date:datetime, *names:str)-> None:
        self.calculate_operational(date, *names)

    def forday_to_exel(self, date:datetime, *names:str)-> None:
        self.calculate_forday(date, *names)
                
    def calculate_operational(self, target_date:datetime, *names:str)-> None:
        target_date
        month_punkts: list = self.Punkts.month_punkts(target_date, annual=False)
        annual_punkts: list = self.Punkts.month_punkts(target_date, annual=True)
        line_punkts: list = self.LinePunkts.month_punkts(target_date)
        cert_punkts: list = self.CertPunkts.month_punkts(target_date)
        self.create_operational_Exel(month_punkts, line_punkts, cert_punkts, annual_punkts, 
                                    target_date, *names)
   
    def calculate_forday(self, whatday:datetime, *names:str)-> None:
        self.create_forday_Exel(whatday, *names)
    
    def create_operational_Exel(self, dayPunkt:list, lineDayPunkt:list, certDayPunkt:list, 
                                yearPunkt:list, date:datetime, *names)-> None:

        def stack_punkts_by_location(line_punkts:list, text:str)-> list:
            locations={}
            executers=[]
            for i in line_punkts:
                if i.location in locations:
                    locations[i.location].append(i.equipment)
                else:
                    locations[i.location] = [i.equipment]
                    executers.append(i.executer)
            
            result = list(zip( [text.format(', '.join(j),i) for i,j in locations.items()], executers))
            return result

        x=1
        z=0
        date_for_which = date
        line_punkt_text = 'Выполнение технологического процесса на оборудовании {}, на сайте {}'
        stacked_line_punkts = stack_punkts_by_location(lineDayPunkt, line_punkt_text)
        cert_punkt_text = 'Выполнение паспортизации оборудования {} на сайте {}'
        stacked_cert_punkts = stack_punkts_by_location(certDayPunkt, cert_punkt_text)

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
        l=0

        # устанавливаем размеры клеток, и рамку
        for i in dayPunkt:
            sheet.row(z+14).height_mismatch = True
            sheet.row(z+14).height = 1000
            sheet.write_merge(z+14,z+14, 7, 8, '',font3)
            sheet.write_merge(z+14,z+14, 9, 10, '',font3)
            sheet.write_merge(z+14,z+14, 11, 11, '',font3)
            sheet.write_merge(z+14,z+14, 12, 13, '',font3)
            sheet.write_merge(z+14,z+14, 14, 14, '',font3)
            z+=1
            l+=1
        for i in stacked_line_punkts:
            sheet.row(z+14).height_mismatch = True
            sheet.row(z+14).height = 1000
            sheet.write_merge(z+14,z+14, 1, 1, '',font3)
            sheet.write_merge(z+14,z+14, 6, 6, '',font3)
            sheet.write_merge(z+14,z+14, 7, 8, '',font3)
            sheet.write_merge(z+14,z+14, 9, 10, '',font3)
            sheet.write_merge(z+14,z+14, 11, 11, '',font3)
            sheet.write_merge(z+14,z+14, 12, 13, '',font3)
            sheet.write_merge(z+14,z+14, 14, 14, '',font3)
            z+=1
            l+=1
        for i in stacked_cert_punkts:
            sheet.row(z+14).height_mismatch = True
            sheet.row(z+14).height = 1000
            sheet.write_merge(z+14,z+14, 1, 1, '',font3)
            sheet.write_merge(z+14,z+14, 6, 6, '',font3)
            sheet.write_merge(z+14,z+14, 7, 8, '',font3)
            sheet.write_merge(z+14,z+14, 9, 10, '',font3)
            sheet.write_merge(z+14,z+14, 11, 11, '',font3)
            sheet.write_merge(z+14,z+14, 12, 13, '',font3)
            sheet.write_merge(z+14,z+14, 14, 14, '',font3)
            z+=1
            l+=1

        sheet.write_merge(l+15,l+15, 1, 8, 'Составил: _____________ %s'%names[1],font2_1)
       
        # Заполняем сами пункты
        for i in dayPunkt:
            # Заполняем ячейку число (Строка, Колонка, Текст, Шрифт)
            sheet.write(x+13,1,str(dayPunkt[x-1][0]),font3)
            sheet.write(x+13,12,'%s'%names[2],font3)

            # Заполняем ячейку номера пунктов (Строка, Колонка, Текст, Шрифт)
            sheet.write_merge(x+13,x+13,2,5,str((dayPunkt[x-1][1])),font3)

            # Заполняем ячейку годовой пункт (Строка, Колонка, Текст, Шрифт)
            sheet.write_merge(x+13, x+13, 6, 6, str(yearPunkt[x-1][1]),font3)
            x+=1

        # Заполняем пункты техпроцесса на линии
        for punkt in stacked_line_punkts:
            # Заполняем столбей Работ по графику
            sheet.write_merge(x+13, x+13, 2, 5, punkt[0], font3)
            # Заполняем столбец "Исполнитель"
            sheet.write(x+13, 12, punkt[1], font3)
            x+=1
        
        # Заполняем пункты паспортизации
        for punkt in stacked_cert_punkts:
            # Заполняем столбей Работ по графику
            sheet.write_merge(x+13, x+13, 2, 5, punkt[0], font3)
            # Заполняем столбец "Исполнитель"
            sheet.write(x+13, 12, punkt[1], font3)
            x+=1


                    
        # Заполняем шапку
        sheet.write_merge(1, 1, 1, 7, 'Утверждаю: ________________%s'%names[0], font1)
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



    def create_forday_Exel(self,nowWithMonth, *names):
        day_for_which = nowWithMonth
        who_approved, who_made, who_execute = names 
        
        book = xlwt.Workbook('utf8')
        sheet = book.add_sheet('sheetname',cell_overwrite_ok=True)

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

            
        self.startday=day_for_which.weekday()
        e=0
        w=0
        dayvar=1
        for i in range(3):
            for y in range (14):
                sheet.write(9+i,10+y,'',font3)
            while (10+w+self.startday) <= 23 and e in range(calendar.mdays[day_for_which.month]):
                sheet.write(9+i,10+self.startday+w,dayvar,font4)
                dayvar+=1
                e+=1
                w+=1
            w=0
            self.startday=0

        
        sheet.write_merge(1, 1, 1, 4, 'Согласовано_______________',font1)
        sheet.write_merge(2, 2, 1, 4, '%s'%who_approved,font1)
        sheet.write_merge(3, 3, 1, 4, '«____» _____________%s г.'%day_for_which.year,font1)
        
        sheet.write_merge(1, 1, 13, 20, 'Утверждено_________________ ',font1)
        sheet.write_merge(2, 2, 13, 20, 'Аношкин В.И.',font1)
        sheet.write_merge(3, 3, 13, 20, '«____» ____________%s г.'%day_for_which.year,font1)
        
        sheet.write_merge(5, 5, 1, 23, 'Четырехнедельный план-график технического обслуживания устройств связи на %s %s года бригады цифровой'%(self.month_association_back[day_for_which.month], day_for_which.year),font2)
        sheet.write_merge(6, 6, 2, 20, 'связи участка магистральной связи Донецькой дистанции  связи Донецкой железной дороги',font2)
        
        sheet.write_merge(8, 8, 1,9, 'Месяц/день недели',font3)
        sheet.write_merge(9, 11, 1,9, '%s'%who_execute,font3)

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

                self.startday=day_for_which.weekday()
                e=0
                w=0
                for p in range(3):
                    for y in range (14):
                        sheet.write(z+13+p, 10+y, '', font3)
                    while (10+w+self.startday) <= 23 and e in range(calendar.mdays[day_for_which.month]):
                        e+=1
                        forNowCor = datetime(day_for_which.year, day_for_which.month, e)
                        if row.is_today(date = forNowCor, annual = False):
                            sheet.write(z+13+p,10+self.startday+w,'*',font3)
                        else:
                            sheet.write(z+13+p,10+self.startday+w,' ',font3)
                    
                        w+=1
                    w=0
                    self.startday=0
                    p=0
                z+=3

        sheet.write_merge(z+15, z+15, 1,5,'Составил: _____________ %s'%who_made,font2)
        
        sheet.portrait = False
        sheet.set_print_scaling(100)
        book.save(self.desktop+'/Четырёхнедельный %s %i.xls'%(self.month_association_back[day_for_which.month] , day_for_which.year) )

    def WhatDistant(self,targetText):
        return (len(targetText)//20+1)*300

