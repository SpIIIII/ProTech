import datetime

class PunktsIterator:
    def __init__(self,punkts):
        self._punkts = punkts
        self.index = 0
    def __next__(self):
        if self.index < len(self._punkts.all_punkts):
            res = self._punkts.all_punkts[self.index]
            self.index+=1
            return res
        raise StopIteration

class Punkts:
    class __Punkts():
        """ class for manages all punkts
        """
        def __init__(self,db):
            self.db=db
            self.fill_punkts()
            
        def __iter__(self):
            return(PunktsIterator(self))

        def fill_punkts(self):
            self.all_punkts = list()
            for punkt in self.db.c.execute("SELECT id, * FROM weekSchedule"):
                self.all_punkts.append(Punkt(punkt))

        def get_punkts(self,*name)->list:
            return [punkt for punkt in self.all_punkts if punkt.name in name]

        def re_read(self):
            self.fill_punkts()
            return self

        def today_punkts (self, date:datetime=datetime.datetime.now(), name_only = False)->list:
            if name_only:
                return [punkt.name for punkt in self.all_punkts if punkt.is_today(date)]
            else:
                return [punkt for punkt in self.all_punkts if punkt.is_today(date)]  
                
        def update_punct(self, description, period, week_day, month, instruction, order, responsible, equipment, name, shift):
            self.db.update_data(description, period, week_day, month,
                                instruction, order, responsible,
                                equipment, name, shift)  


    instance = None
    def __new__(cls,db):
        if not Punkts.instance:
            Punkts.instance = Punkts.__Punkts(db)
        return Punkts.instance


class Punkt:
    def __init__ (self,*args):
        self.name,self.description,self.period,self.day_of_week,self.month,self.instruction,\
        self.order,self.responsible,self.equipment,self.shift_week = args[0][1:]

    def is_today (self,date):
        now = date        
        now_weekday=(now.weekday())       
        
        now_week=(now.isocalendar()[1])
        association={' пн.':0,' вт.':1,' ср.':2,' чт.':3,' пт.':4}
        associationforMonth={' Январь':1,' Февраль':2,' Март':3,' Апрель':4,' Май':5,' Июнь':6,' Июль':7,' Август':8,
                                                        ' Сентябрь':9,' Октябрь':10,' Ноябрь':11,' Декабрь':12}
        if now_weekday !=6 and now_weekday !=5 :
            if self.period == ' ежедневно':
                return(True)

            elif str(self.period) == str(' раз в неделю'):
                if association[self.day_of_week]==now_weekday:
                    return(True)

            elif str(self.period) == str(' раз в 2 недели'):
                if (now_week+self.shift_week)%2==0:
                    if association[self.day_of_week]==now_weekday:
                        return(True)
                                
            elif str(self.period) == str(' раз в 4 недели'):
                if (now_week+self.shift_week)%4==0:
                    if association[self.day_of_week]==now_weekday:
                        return(True)

            elif str(self.period) == str(' раз в 3 месяца'):
                if (self.shift_week+now_week+(4*(13-associationforMonth[self.month])))%13==0:
                    if association[self.day_of_week]==now_weekday:
                        return(True)
            
            elif str(self.period) == str(' раз в 6 месяцев'):
                if (self.shift_week+now_week+(4*(13-associationforMonth[self.month])))%26==0:
                    if association[self.day_of_week]==now_weekday:
                        return(True)                  
            
            elif str(self.period) == str(' раз 12 месяцев'):
                if (self.shift_week+now_week+(4*(13-associationforMonth[self.month])))%52==0:
                     if (47+now_week+associationforMonth[self.month]+self.shift_week)%52==0:
                        if association[self.day_of_week]==now_weekday:
                            return(True)
        return(False) 

    def __repr__(self):
        return f"===============\nпункт: {self.name}\nописание: {self.description}\
            \nпериодичность: {self.period}\nдень: {self.day_of_week}\nМесяц: {self.month}\
            \nинструкция: {self.instruction}\nприказ: {self.order}\nответственный: {self.responsible}\
            \nоборудование: {self.equipment}\nсдвиг: {self.shift_week}\n==============="