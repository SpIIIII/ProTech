import tkinter as tk
from datetime import datetime

class Punkt:
    def __init__(self, *args, db=None):
        self.id, self.equipment, self.location, self.executer, self.month = args[0]
        self.db=db

    def __str__(self):
        return f'№ {self.id}\nОборудование: {self.equipment},\nСтанция: {self.location}\nИсполнитель: {self.executer}\nМесяц: {self.month}'

    def __repr__(self):
        return f'Punkt({self.id}, {self.equipment}, {self. location}, {self.executer}, {self.month}, {self.db})'

    def change(self, *args):
        self.db.update_data(self.id, *args)

    def delete(self):
        self.db.delet_data(self.id)

    def GUI_delete(self):
        question = tk.messagebox.askquestion('Удаление',f'Вы собираетесь удалить запись.\nУдалить?')
        if question == 'yes':
            self.delete()
            tk.messagebox.showinfo('Готово',f'Запись удаленa')

    def is_in_month(self, month:int)-> bool:
        if self.month == month:
            return True
        else:
            return False


class LinePunktsIterator:
    def __init__(self, LinePunkts)-> None:
        self._Punkts = LinePunkts
        self.index = 0

    def __next__(self)-> Punkt:
        if self.index < len(self._Punkts.all_punkts):
            res = self._Punkts.all_punkts[self.index]
            self.index += 1
            return res
        raise StopIteration

class basePunkts:
    def __iter__(self)-> LinePunktsIterator:
        return LinePunktsIterator(self)

    def __len__ (self):
        return len(self.__all_punkts)

    def fill_punkts(self)-> None:
        self.__all_punkts = list()
        for cert in self.db_lp.c.execute("Select * from certification"):
            self.__all_punkts.append(Punkt(cert, db=self.db_lp))
    
    @property
    def all_punkts(self)-> list:
        return self.__all_punkts

    def get_cert_by_id(self, id:int)-> Punkt:
        id = int(id)
        return  [cert for cert in self.all_punkts if cert.id == id][0]

    def refresh(self):
        self.fill_punkts()
    
    def add_cert(self, *args):
        self.db_lp.insert_data(*args)

    def month_punkts(self, target_date:datetime):
        month = target_date.month-1
        months = [punkt for punkt in self.all_punkts if punkt.is_in_month(month)]
        return months

class LinePunkts(basePunkts):
    def __init__(self, db_lp)-> None:
        self.db_lp = db_lp
        self.fill_punkts()


class CertPunkts(basePunkts):
    def __init__(self, db_c):
        self.db_lp = db_c
        self.fill_punkts()
        


