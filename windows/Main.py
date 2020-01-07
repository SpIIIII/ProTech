import tkinter as tk
import datetime
from tkinter import ttk
from . import Show_one_day, Change_punkt, New_punkt, To_exel, Analysis, Show_punkt


class Main(tk.Frame):

    def __init__ (self, root, punkts, veison, updater, plot):
        super().__init__(root)
        self.root = root
        self.plot = plot
        self.updater = updater
        self.version = veison
        self.punkts = punkts
        self.change_punkt = Change_punkt.Change
        root.protocol("WM_DELETE_WINDOW", root.quit)
        self.Show_punkt = Show_punkt.Show_punkt
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
        filemenu.add_command(label="Добавить пункт", command=self.open_add_new_punkt)
        filemenu.add_command(label="Обновить список", command=self.refresh_tree_view)
        filemenu.add_command(label="Анализ", command=self.open_Analysis)
        filemenu.add_command(label="в Exel", command=self.open_To_Exel)
        
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
        self.tree.column('description', width=350,anchor=tk.E)
        self.tree.column('day', width=100,anchor=tk.CENTER)
        self.tree.column('month', width=50,anchor=tk.CENTER)
        
        self.tree.heading('ID', text='номер')
        self.tree.heading('description', text='краткое описание')
        self.tree.heading('day', text='переодичность')
        self.tree.heading('month', text='день')
        self.tree.bind('<Button-3>',self.drop_popup_menu)
        self.tree.bind("<Double-1>", self.show_punkt)
        self.tree.pack(side=tk.BOTTOM,fill=tk.BOTH, expand=tk.YES)
        self.fill_tree_view()
        
        # Create a popup menu
        self.popup_menu = tk.Menu(self, tearoff=0)
        self.popup_menu.add_command(label='Изменить', command=self.open_change_selected_punkt)
        self.popup_menu.add_command(label='Добавить', command=self.open_add_new_punkt)
        self.popup_menu.add_separator()
        self.popup_menu.add_command(label='Удалить', command=self.delete)

        self.tree_item = ''

    def show_punkt(self, event):
        """ action when doubleclick the treeview"""
        iid = self.tree.identify_row(event.y)
        self.tree.selection_set(iid)
        item = self.tree.selection()[0]
        name = self.tree.item(item,'values')[0]
        punkt = self.punkts.get_punkt(name)
        self.open_show_punkt(punkt)

    def drop_popup_menu(self, event):
        """action in event of button 3 on tree view"""
        # select row under mouse
        iid = self.tree.identify_row(event.y)
        if iid:
            # mouse pointer over item
            self.tree.selection_set(iid)
            self.popup_menu.post(event.x_root, event.y_root)
        else:
           pass

    def delete (self):
        item = self.tree.selection()[0]
        self.punkts.get_punkt(self.tree.item(item,'values')[0]).GUI_delete()
        self.refresh_tree_view()
       
    def fill_tree_view(self):
        for row in self.punkts.re_read():
            self.tree.insert('', 'end', values=(row.name,row.description,row.period,row.day_of_week))
        
    def refresh_tree_view(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.fill_tree_view()

    def open_change_selected_punkt (self):
        item = self.tree.selection()[0]
        punkt_name = self.tree.item(item,'values')[0]
        self.change_punkt(self, self.punkts.get_punkt(punkt_name)) 

    def open_add_new_punkt(self):
        New_punkt.New_Punkt(self)

    def open_show_punkt(self,punkt):
        self.Show_punkt(self, punkt)

    def open_To_Exel(self):
        To_exel.To_Exel(self)

    def open_Show(self):
        Show_one_day.ShowOneDay(self)

    def open_Analysis(self):
        Analysis.Analysis(self)
