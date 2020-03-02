import tkinter as tk
import config
import datetime
from tkinter import ttk
from . import Show_one_day, Show_punkt, Change_punkt, New_punkt, To_exel, Analysis, Certification_window


class Main(tk.Frame):
    def __init__ (self, root, Punkts, Veison, Updater, Plot, Outputter, LinePunkts, Certifications):
        super().__init__(root)
        self.root = root
        self.Punkts = Punkts
        self.Version = Veison
        self.Updater = Updater
        self.Plot = Plot
        self.Outputter = Outputter
        self.LinePunkts = LinePunkts
        self.Certifications = Certifications

        # sub windows        
        self.change_punkt = Change_punkt.Change
        self.Show_punkt = Show_punkt.Show_punkt
        self.To_exel = To_exel.To_Exel

        root.protocol("WM_DELETE_WINDOW", root.quit)
        self.init_main()
        
        
    def init_main(self):
        self.now1 = datetime.datetime.now()

        # Draw Frames    
        main_frame = tk.Frame(bd=2)
        main_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Draw MenuBars
        menubar = tk.Menu()
        fileMenu = tk.Menu(menubar, tearoff=0)
        fileMenu.add_command(label="Добавить пункт", command=self.open_add_new_punkt)
        fileMenu.add_command(label="Обновить список", command=self.refresh_tree_view)
        fileMenu.add_command(label="Анализ", command=self.open_Analysis)
        fileMenu.add_command(label="в Exel", command=self.open_To_Exel)
        fileMenu.add_separator()
        fileMenu.add_command(label="Выход", command=self.root.quit)
        
        otherPunktsMenu = tk.Menu(menubar, tearoff=0)
        otherPunktsMenu.add_command(label="Техпроцесс на линии", command=self.open_linepunkts)
        otherPunktsMenu.add_command(label='Паспортизация', command=self.open_certifications)

        programmenu = tk.Menu(menubar, tearoff=0)
        programmenu.add_command(label='Обновить программу', command=self.update)
        
        menubar.add_cascade(label="Файл", menu=fileMenu)
        menubar.add_cascade(label="Подпункты", menu=otherPunktsMenu)
        menubar.add_cascade(label="Программа", menu=programmenu)
        self.root.config(menu=menubar)
        
        # Draw Labels
        label_on_root=tk.Label(main_frame, text=' Сегодня: '+''.join(self.Punkts.today_punkts(name_only=True)), bd=1, relief=tk.SUNKEN, anchor=tk.W)
        label_on_root.pack(side=tk.BOTTOM, fill =tk.X)
        label_on_root.bind('<Button-1>', lambda e:self.open_Show())
        
        # Draw TreeView      
        self.tree=ttk.Treeview(main_frame, columns =('ID', 'description', 'day', 'month'), height=15, show='headings')
       
        self.tree.column('ID', width=80, anchor=tk.CENTER)
        self.tree.column('description', width=350, anchor=tk.E)
        self.tree.column('day', width=100, anchor=tk.CENTER)
        self.tree.column('month', width=50, anchor=tk.CENTER)
        
        self.tree.heading('ID', text='номер')
        self.tree.heading('description', text='краткое описание')
        self.tree.heading('day', text='переодичность')
        self.tree.heading('month', text='день')
        self.tree.bind('<Button-3>',self.drop_popup_menu)
        self.tree.bind("<Double-1>", self.show_punkt)
        self.tree.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.YES)
        self.fill_tree_view()
        
        # Create a popup menu
        self.popup_menu = tk.Menu(self, tearoff=0)
        self.popup_menu.add_command(label='Изменить', command=self.open_change_selected_punkt)
        self.popup_menu.add_command(label='Добавить', command=self.open_add_new_punkt)
        self.popup_menu.add_separator()
        self.popup_menu.add_command(label='Удалить', command=self.delete)

        self.tree_item = ''

        try:
            self.init_update_check()
        except:
            pass

    def show_punkt(self, event):
        """ action when doubleclick the treeview"""
        iid = self.tree.identify_row(event.y)
        self.tree.selection_set(iid)
        item = self.tree.selection()[0]
        name = self.tree.item(item,'values')[0]
        punkt = self.Punkts.get_punkt(name)
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
        self.Punkts.get_punkt(self.tree.item(item,'values')[0]).GUI_delete()
        self.refresh_tree_view()
       
    def fill_tree_view(self):
        for row in self.Punkts.re_read():
            self.tree.insert('', 'end', values=(row.name, row.description, row.period, row.day_of_week))
        
    def refresh_tree_view(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.fill_tree_view()

    def update(self):
        if self.Updater.need_update():
            if self.confirm_update():
                self.Updater.start()
        else:
            tk.messagebox.showinfo('Up to date',f'Текущая версия ({self.Version.local_version_txt}) обновлена')

    def init_update_check(self):
        if self.Updater.need_update():
            ask = tk.messagebox.askquestion('Доступно обновление', f'Текущая версия - {self.Version.local_version_txt}.\
                                            \nДоступно обновление до версии {self.Version.remote_version_txt}\nОбновить?')
            if ask == 'yes':
                self.update()
    
    def confirm_update(self):
            MsgBox = tk.messagebox.askquestion ('Обновить?',f'Текущая версия - {self.Version.local_version_txt} \
                                                \nверсия для обновления - {self.Version.remote_version_txt}.\nОбновить?')
            if MsgBox == 'yes':
                tk.messagebox.showinfo('Обновление','Дождитесь скачивания новой версии.\n После скачивания программа будет закрыта, \
                                        и начнется процес установки')
                return True
            else:
                return False

    def open_change_selected_punkt (self):
        item = self.tree.selection()[0]
        punkt_name = self.tree.item(item,'values')[0]
        self.change_punkt(self, self.Punkts.get_punkt(punkt_name)) 

    def open_add_new_punkt(self):
        New_punkt.New_Punkt(self)

    def open_show_punkt(self,punkt):
        self.Show_punkt(self, punkt)

    def open_To_Exel(self):
        self.To_exel(self)

    def open_Show(self):
        Show_one_day.ShowOneDay(self)

    def open_linepunkts(self):
        Certification_window.LinePunkts(self)

    def open_certifications(self):
        Certification_window.Certifications(self)

    def open_Analysis(self):
        Analysis.Analysis(self)
