import sqlite3

class DB:
    def __init__(self):
        self.conn=sqlite3.connect('weekSchedule.db')
        self.c = self.conn.cursor()

        self.c.execute('''CREATE TABLE IF NOT EXISTS weekSchedule (id text primary key,
                        description text, whatweek text, whatday text, yearMonth text,
                        instruction text, comand text, Maker text, equipment text, shiftweek integer, active integer)''')
        self.c.execute('''select * from weekSchedule''')
        self.conn.commit()
        self.update_table()

               
    def insert_data(self, num, description, whenW, whenD, yearM, inst, coma, make, equip, shift):
        self.c.execute('''INSERT INTO weekSchedule (id, description, whatweek, whatday, yearMonth, instruction, comand, Maker, equipment, shiftweek) 
                          VALUES (?,?,?,?,?,?,?,?,?,?)''',(num, description, whenW, whenD, yearM, inst, coma, make, equip, shift))
        self.conn.commit()

    def delet_data(self, n):
        self.c.execute('''DELETE FROM weekSchedule WHERE id =? ''',(n,))
        self.conn.commit()

    def update_data(self, new_name, description, whenW, whenD, yearM, inst, coma, make, equip, num, shift, active):
        self.c.execute('''UPDATE weekSchedule SET id = ?, description = ?, whatweek = ?, whatday = ?, yearMonth = ?, \
            instruction = ?, comand = ?, Maker = ?, equipment = ?, shiftweek = ?, active = ? WHERE id = ?''',
        (new_name, description, whenW, whenD, yearM, inst, coma, make, equip, shift, active, num,))
        self.conn.commit()
        
    def read_data(self,num):
        self.c.execute('''SELECT description FROM weekSchedule WHERE id =?''',(num,))
        return self.c.fetchall()

    def update_table(self)-> None:
        '''update table if needed'''
        self.c.execute('''PRAGMA table_info('weekSchedule')''')
        x = self.c.fetchall()
        if not 'active' in [i[1] for i in x]:
            self.c.execute('''ALTER TABLE weekSchedule ADD COLUMN active DEFAULT 1''')
            self.conn.commit()
        else:
            pass   


 