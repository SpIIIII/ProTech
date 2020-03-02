
import sqlite3

class base_DB:
    def insert_data(self, equipment,  localtion , executer , month):
        self.c.execute('''INSERT INTO certification (equipment, localtion , executer , month) 
                          VALUES (?,?,?,?) ''', (equipment, localtion , executer , month))
        self.conn.commit()

    def delet_data(self, id):
        self.c.execute('''DELETE FROM certification WHERE id =? ''', (id,))
        self.conn.commit()

    def update_data(self, id, equipment, localtion , executer , month):
        self.c.execute('''UPDATE certification SET equipment=?,  localtion = ?, executer = ?, 
                            month = ?,  WHERE id = ?''',
        (equipment, localtion, executer, month, id))
        self.conn.commit()
        
    def read_data(self,num):
        self.c.execute('''SELECT * FROM certification WHERE id =?''',(num,))
        return self.c.fetchall()

    def __del__(self):     
        self.conn.close()


class DB_linePunkts(base_DB):
    def __init__(self):
        self.conn=sqlite3.connect('linePunkts.db')
        self.c = self.conn.cursor()

        self.c.execute('''CREATE TABLE IF NOT EXISTS certification (id INTEGER PRIMARY KEY, equipment text,
                            localtion text, executer text, month int)''')
        self.c.execute('''select * from certification''')
        self.conn.commit()
               

class DB_certifications(base_DB):
    def __init__(self):
        self.conn=sqlite3.connect('certifications.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS certification (id INTEGER PRIMARY KEY, equipment text,
                            localtion text, executer text, month int)''')
        self.c.execute('''select * from certification''')
        self.conn.commit()