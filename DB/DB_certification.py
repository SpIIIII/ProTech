
import sqlite3

class DB_certification:
    def __init__(self):
        self.conn=sqlite3.connect('certification.db')
        self.c = self.conn.cursor()

        self.c.execute('''CREATE TABLE IF NOT EXISTS certification (id ROWID, localtion text, executer text, month int)''')
        self.c.execute('''select * from certification''')
        self.conn.commit()

               
    def insert_data(self, id, localtion , executer , month):
        self.c.execute('''INSERT INTO certification (localtion , executer , month) 
                          VALUES (?,?,?) ''', (localtion , executer , month))
        self.conn.commit()

    def delet_data(self, id):
        self.c.execute('''DELETE FROM certification WHERE id =? ''', (id,))
        self.conn.commit()

    def update_data(self, id, localtion , executer , month):
        self.c.execute('''UPDATE certification SET  localtion = ?, executer = ?, month = ?,  WHERE id = ?''',
        (localtion, executer, month, id))
        self.conn.commit()
        
    def read_data(self,num):
        self.c.execute('''SELECT * FROM certification WHERE id =?''',(num,))
        return self.c.fetchall()

    def __del__(self):     
        self.conn.close()