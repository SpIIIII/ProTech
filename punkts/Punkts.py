import datetime
import calendar
import tkinter as tk
from typing import List


class Punkt:
    def __init__(self,*args,db=None)-> None:
        self.db = db
        self.name,self.description,self.period,self.day_of_week,self.month,self.instruction,\
        self.order,self.responsible,self.equipment,self.shift_week = args[0][1:]

    def is_annual (self)-> bool:
        if self.period == ' раз 12 месяцев' or self.period == ' раз в 6 месяцев' or self.period == ' раз в 3 месяца':
            return True
        return False
        
    def is_today(self, date, annual=None)-> bool:
        date_to_check = date        
        weekday=(date_to_check.weekday())
        month = date.month       
        
        week=(date_to_check.isocalendar()[1])
        week_in_month = (date_to_check.day-1)//7+1
        association={' пн.':0,' вт.':1,' ср.':2,' чт.':3,' пт.':4}
        associationforMonth={' Январь':1,' Февраль':2,' Март':3,' Апрель':4,' Май':5,' Июнь':6,' Июль':7,' Август':8,
                                                        ' Сентябрь':9,' Октябрь':10,' Ноябрь':11,' Декабрь':12}
        def check_cycle()-> bool:
            if weekday !=6 and weekday !=5 :
                if self.period == ' ежедневно':
                    return True

                elif str(self.period) == str(' раз в неделю'):
                    if association[self.day_of_week]==weekday:
                        return True

                elif str(self.period) == str(' раз в 2 недели'):
                    if (week+self.shift_week)%2==0:
                        if association[self.day_of_week]==weekday:
                            return True
                                    
                elif str(self.period) == str(' раз в 4 недели'):
                    if (week+self.shift_week)%4==0:
                        if association[self.day_of_week]==weekday:
                            return True

                elif str(self.period) == str(' раз в 3 месяца'):
                    if (self.shift_week+week+(4*(13-associationforMonth[self.month])))%13==0:
                        if association[self.day_of_week]==weekday:
                            return True
                
                elif str(self.period) == str(' раз в 6 месяцев'):
                    if (self.shift_week+week+(4*(13-associationforMonth[self.month])))%26==0:
                        if association[self.day_of_week]==weekday:
                            return True                  
                
                elif str(self.period) == str(' раз 12 месяцев'):
                    if associationforMonth[self.month] == month and association[self.day_of_week]==weekday and self.shift_week+week_in_month == 2:
                        return True
        
            return False

        if annual is None:
            return check_cycle()

        if annual == self.is_annual():
            return check_cycle()

        return False 

    def delete(self)-> None:
        self.db.delet_data(self.name)

    def GUI_delete(self)-> None:
        question = tk.messagebox.askquestion('Удаление',f'Вы собираетесь удалить пункт {self.name}.\nУдалить пункт?')
        if question == 'yes':
            self.delete()
            tk.messagebox.showinfo('Готово',f'Пункт {self.name} удален')

    def update(self, *args)-> None:
        self.db.update_data(*args)

    def __str__(self)-> None:
        return f"===============\nпункт: {self.name}\nописание: {self.description}\
            \nпериодичность: {self.period}\nдень: {self.day_of_week}\nМесяц: {self.month}\
            \nинструкция: {self.instruction}\nприказ: {self.order}\nответственный: {self.responsible}\
            \nоборудование: {self.equipment}\nсдвиг: {self.shift_week}\n==============="


class PunktsIterator:
    def __init__(self, Punkts)->None:
        self._Punkts = Punkts
        self.index = 0

    def __next__(self)-> Punkt:
        if self.index < len(self._Punkts.all_punkts):
            res = self._Punkts.all_punkts[self.index]
            self.index+=1
            return res
        raise StopIteration


class Punkts:
    class __Punkts():
        """ class for manages all punkts
        """
        def __init__(self,db)-> None:
            self.db=db
            self.fill_punkts()
            
        def __iter__(self)-> PunktsIterator:
            return PunktsIterator(self)

        def __len__(self)-> int:
            return len(self.__all_punkts)

        def insert_punkt (self, name, description, period, day_of_week, month, instruction, order, responsible, equipment, shift)-> None:
            self.db.insert_data(name, description, period, day_of_week,
                                month, instruction, order, responsible,
                                equipment, shift)

        def fill_punkts(self)-> None:
            self.__all_punkts = list()
            for punkt in self.db.c.execute("SELECT id, * FROM weekSchedule"):
                self.__all_punkts.append(Punkt(punkt,db=self.db))

        @property
        def all_punkts(self)-> list:
            return self.__all_punkts

        def get_punkts(self,*name)->list:
            return [punkt for punkt in self.__all_punkts if punkt.name in name]

        def get_punkt(self,name:str)->Punkt:
            return [punkt for punkt in self.__all_punkts if punkt.name == name][0]

        def re_read(self):
            self.fill_punkts()
            return self

        def month_punkts(self,date:datetime, name_only=True, without_holidays=True, annual=None)->list:
            month = date.month
            day_for_calc = date.replace(day = 1)
            month_punkts=list()
            for i in range(calendar.mdays[month]):
                if without_holidays:
                    if day_for_calc.weekday() !=6 and day_for_calc.weekday() !=5:
                        month_punkts.append([day_for_calc.day,'; '.join(self.today_punkts(day_for_calc,name_only,annual))])
                else:
                    month_punkts.append([day_for_calc.day,'; '.join(self.today_punkts(day_for_calc,name_only,annual))])

                day_for_calc+=datetime.timedelta(1)
            return month_punkts

        def today_punkts (self, date:datetime=datetime.datetime.now(), name_only:bool=True, annual=None)->list:
            if name_only:
                return [punkt.name for punkt in self.__all_punkts if punkt.is_today(date, annual)]
            else:
                return [punkt for punkt in self.__all_punkts if punkt.is_today(date, annual)]

        def delete_punkts_by_name(self,punkts:list)-> None:
            [self.delete_punkt_by_name(name) for name in punkts]

        def delete_punkt_by_name(self, punkt_to_del)-> None:
            [punkt.GUI_delete() for punkt in self.__all_punkts if punkt.name == punkt_to_del]

        
                                
    instance = None
    def __new__(cls, db)-> __Punkts:
        if not Punkts.instance:
            Punkts.instance = Punkts.__Punkts(db)
        return Punkts.instance



