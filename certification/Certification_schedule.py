

class Cert:
    def __init__(self, *args, db=None):
        self.id, self.equipment, self.location, self.executer, self.month = args[0]
        self.db=db

    def __str__(self):
        return f'Оборудование: {self.equipment},\nСтанция: {self.location}\nИсполнитель: {self.executer}\nМесяц: {self.month}'

    def __repr__(self):
        return f'Cert({self.id}, {self.equipment}, {self. location}, {self.executer}, {self.month}, {self.db})'


class CertificationsIterator:
    def __init__(self, Certifications)-> None:
        self._Certs = Certifications
        self.index = 0

    def __next__(self)-> Cert:
        if self.index < len(self._Certs.all_certs):
            res = self._Certs.all_certs[self.index]
            self.index += 1
            return res
        raise StopIteration

class Certifications:
    def __init__(self, db_c)-> None:
        self.db_c = db_c
        self.fill_certs()

    def __iter__(self)-> CertificationsIterator:
        return CertificationsIterator(self)

    def __len__ (self):
        return len(self.__all_certs)


    def fill_certs(self)-> None:
        self.__all_certs = list()
        for cert in self.db_c.c.execute("Select * from certification"):
            self.__all_certs.append(Cert(cert, db=self.db_c))
    
    @property
    def all_certs(self)-> list:
        return self.__all_certs

    def refresh(self):
        self.fill_certs()
    
    def add_cert(self, *args):
        self.db_c.insert_data(*args)

    

