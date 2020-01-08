import sqlite3

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

 