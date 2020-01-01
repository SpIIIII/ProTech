import tkinter as tk
import datetime
import sqlite3
from tkinter import ttk
from punkts import Punkts
from updater import update
from version import Version
from datetime import timedelta
from tkinter import messagebox
from windows import Show_one_day, Change_punkt, New_punkt, To_exel



class Main(tk.Frame):

    def __init__ (self, root):
        super().__init__ (root)
        self.db = db
        self.version = Version.Versions()
        self.punkts = Punkts.Punkts(db)
        self.init_main()
        
        
    def init_main(self):

        self.now1 = datetime.datetime.now()
        
        self.updater = update.Update(self.version)
        '''
        association1={' Январь':1,' Февраль':2,' Март':3,' Апрель':4,' Май':5,' Июнь':6,' Июль':7,' Август':8,
                                                        ' Сентябрь':9,' Октябрь':10,' Ноябрь':11,' Декабрь':12}
        '''  
        # Draw Frames    
        main_frame = tk.Frame(bd = 2)
        main_frame.pack(side=tk.BOTTOM,fill=tk.BOTH, expand=True)

        # Draw MenuBar
        menubar = tk.Menu()
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Добавить пункт", command=self.add_new_punkt)
        filemenu.add_command(label="Обновить список", command=self.refresh_tree_view)
        filemenu.add_command(label="в Exel", command=self.open_To_Exel)
        # filemenu.add_command(label="test", command=self.db.db_to_class)
        filemenu.add_separator()
        filemenu.add_command(label="Выход", command=root.quit)

        programmenu = tk.Menu(menubar, tearoff=0)
        programmenu.add_command(label='Обновить программу', command=self.updater.start)
        
        menubar.add_cascade(label="Файл", menu=filemenu)
        menubar.add_cascade(label="Программа", menu=programmenu)
        root.config(menu=menubar)

        # Draw Labels
        label_on_root=tk.Label(main_frame, text=' Сегодня: '+''.join(self.punkts.today_punkts(name_only = True)),bd=1,relief=tk.SUNKEN,anchor=tk.W)
        label_on_root.pack(side=tk.BOTTOM,fill =tk.X)
        label_on_root.bind('<Button-1>', lambda e:self.open_Show())
        
        # Draw TreeView      
        self.tree=ttk.Treeview(main_frame, columns =('ID','description','day','month'),height=15,show='headings')
       
        self.tree.column('ID', width=80,anchor=tk.CENTER)
        self.tree.column('description', width=350,anchor=tk.CENTER)
        self.tree.column('day', width=100,anchor=tk.CENTER)
        self.tree.column('month', width=50,anchor=tk.CENTER)
        
        self.tree.heading('ID', text='номер')
        self.tree.heading('description', text='краткое описание')
        self.tree.heading('day', text='переодичность')
        self.tree.heading('month', text='день')
        self.tree.bind('<Button-3>',self.select)
        self.tree.pack(side=tk.BOTTOM,fill=tk.BOTH, expand=tk.YES)
        self.fill_tree_view()
        
        # Create a popup menu
        self.aMenu = tk.Menu(self, tearoff=0)
        self.aMenu.add_command(label='Изменить', command=self.change_selected_punkt)
        self.aMenu.add_command(label='Добавить', command=self.add_new_punkt)
        self.aMenu.add_separator()
        self.aMenu.add_command(label='Удалить', command=self.delete)

        self.tree_item = ''

    def select(self, event):
        """action in event of button 3 on tree view"""
        # select row under mouse
        iid = self.tree.identify_row(event.y)
        if iid:
            # mouse pointer over item
            self.tree.selection_set(iid)
            self.aMenu.post(event.x_root, event.y_root)
        else:
           pass

    def delete(self):
        item = self.tree.selection()[0]
        #print(self.tree.item(item,'values')[0])
        self.db.delet_data(self.tree.item(item,'values')[0])
        self.refresh_tree_view()

    def change_selected_punkt(self):
        item = self.tree.selection()[0]
        punkt_name = self.tree.item(item,'values')[0]
        Change_punkt.Change(self.punkts.get_punkts(punkt_name), self.punkts, self, root) 
       
    def fill_tree_view(self):
        for row in self.punkts.re_read():
            self.tree.insert('', 'end', values=(row.name,row.description,row.period,row.day_of_week))
        
    def refresh_tree_view(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.fill_tree_view()

    def add_new_punkt(self):
        New_punkt.New_Punkt(self.punkts, self, root)

    def open_To_Exel(self):
        To_exel.To_Exel(root,self.punkts)

    def open_Show(self):
        Show_one_day.ShowOneDay(root, self.punkts)

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

   

def calculateOneDay (rowver, date):
        now = date        
        now_weekday=(now.weekday())       
        
        now_week=(now.isocalendar()[1])
        association={' пн.':0,' вт.':1,' ср.':2,' чт.':3,' пт.':4}
        associationforMonth={' Январь':1,' Февраль':2,' Март':3,' Апрель':4,' Май':5,' Июнь':6,' Июль':7,' Август':8,
                                                        ' Сентябрь':9,' Октябрь':10,' Ноябрь':11,' Декабрь':12}
        if now_weekday !=6 and now_weekday !=5 :
            if rowver[3] == ' ежедневно':
                return(True)

            elif str(rowver[3]) == str(' раз в неделю'):
                if association[rowver[4]]==now_weekday:
                    return(True)

            elif str(rowver[3]) == str(' раз в 2 недели'):
                if (now_week+rowver[10])%2==0:
                    if association[rowver[4]]==now_weekday:
                        return(True)
                                
            elif str(rowver[3]) == str(' раз в 4 недели'):
                if (now_week+rowver[10])%4==0:
                    if association[rowver[4]]==now_weekday:
                        return(True)

            elif str(rowver[3]) == str(' раз в 3 месяца'):
                if (rowver[10]+now_week+(4*(13-associationforMonth[rowver[5]])))%13==0:
                    if association[rowver[4]]==now_weekday:
                        return(True)
            
            elif str(rowver[3]) == str(' раз в 6 месяцев'):
                if (rowver[10]+now_week+(4*(13-associationforMonth[rowver[5]])))%26==0:
                    if association[rowver[4]]==now_weekday:
                        return(True)                  
            
            elif str(rowver[3]) == str(' раз 12 месяцев'):
                if (rowver[10]+now_week+(4*(13-associationforMonth[rowver[5]])))%52==0:
                     if (47+now_week+associationforMonth[rowver[5]]+rowver[10])%52==0:
                        if association[rowver[4]]==now_weekday:
                            return(True)
                           
        return(False)


if __name__ ==  "__main__":
    
    root=tk.Tk()
    db=DB()
    app = Main(root)
    app.pack()
    root.title("Техпроцесс")
    root.geometry("580x350+300+220")
    #root.resizable(False,False)
    
    root.minsize(580,350)
    root.mainloop()


