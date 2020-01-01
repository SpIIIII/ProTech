import tkinter as tk
import datetime
from tkinter import ttk
from . import Show_one_day, Change_punkt, New_punkt, To_exel 


class Main(tk.Frame):

    def __init__ (self, root, punkts, veison, updater):
        super().__init__ (root)
        self.root = root
        self.updater = updater
        self.version = veison
        self.punkts = punkts
        self.init_main()
        
        
    def init_main(self):

        self.now1 = datetime.datetime.now()
        
        
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
        filemenu.add_command(label="Выход", command=self.root.quit)

        programmenu = tk.Menu(menubar, tearoff=0)
        programmenu.add_command(label='Обновить программу', command=self.updater.start)
        
        menubar.add_cascade(label="Файл", menu=filemenu)
        menubar.add_cascade(label="Программа", menu=programmenu)
        self.root.config(menu=menubar)

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

    def delete (self):
        item = self.tree.selection()[0]
        self.punkts.get_punkt(self.tree.item(item,'values')[0]).delete()
        self.refresh_tree_view()

    def change_selected_punkt (self):
        item = self.tree.selection()[0]
        punkt_name = self.tree.item(item,'values')[0]
        Change_punkt.Change(self.punkts.get_punkts(punkt_name), self.punkts, self, self.root) 
       
    def fill_tree_view(self):
        for row in self.punkts.re_read():
            self.tree.insert('', 'end', values=(row.name,row.description,row.period,row.day_of_week))
        
    def refresh_tree_view(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.fill_tree_view()

    def add_new_punkt(self):
        New_punkt.New_Punkt(self.punkts, self, self.root)

    def open_To_Exel(self):
        To_exel.To_Exel(self.root,self.punkts)

    def open_Show(self):
        Show_one_day.ShowOneDay(self.root, self.punkts)
