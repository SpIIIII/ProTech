class Punkts:
    def __init__(self):
        self.all_punkts = list()
        
    def is_on_date(self,date):
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

    def add_punkt(self, *args):
        self.all_punkts.append(Punkt(args))

class Punkt:
    def __init__ (self,*args):
        self.name,self.description,self.period,self.day_of_week,self.month,self.instruction,\
        self.order,self.responsible,self.equipment,self.shift_week = args[0][0][1:]

    def __repr__(self):
        return f"===============\nпункт: {self.name}\nописание: {self.description}\
            \nпериодичность: {self.period}\nдень: {self.day_of_week}\nМесяц: {self.month}\
            \nинструкция: {self.instruction}\nприказ: {self.order}\nответственный: {self.responsible}\
            \nоборудование: {self.equipment}\nсдвиг: {self.shift_week}\n==============="