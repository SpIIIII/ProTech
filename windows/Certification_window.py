import tkinter as tk
from tkinter import ttk


class basePunktsWindow(tk.Toplevel):      
    def init_certification_window(self):
        # Draw Frames
        self.top_frame = ttk.Frame(self, height=68)
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.bottom_frame = ttk.Frame(self)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.fill_top_frame(version=0)
        self.fill_bottom_frame()

         # Draw MenuBar
        menubar = tk.Menu()
        filemenu = tk.Menu(menubar, tearoff=0)
        
        filemenu.add_command(label="Добавить", command=lambda: self.fill_top_frame(version=1))
        filemenu.add_separator()
        filemenu.add_command(label="Выход", command=self.destroy)
        
        menubar.add_cascade(label="Файл", menu=filemenu)
        self.config(menu=menubar)

        # Create a popup menu
        self.popup_menu = tk.Menu(self, tearoff=0)
        self.popup_menu.add_command(label='Изменить', command=lambda:1)
        self.popup_menu.add_command(label='Добавить', command=lambda:1)
        self.popup_menu.add_separator()
        self.popup_menu.add_command(label='Удалить', command=self.delete_cert)

        self.grab_set()
        self.focus_set()

    def fill_bottom_frame(self):
        # create and fill tree view
        self.line_punkt_tree = ttk.Treeview(self.bottom_frame, columns=( 'equipment', 'location', 'executer', 'month'), height=15, show='headings')

        self.line_punkt_tree.column('equipment', width=60, anchor=tk.CENTER)
        self.line_punkt_tree.column('location', width=60, anchor=tk.E)
        self.line_punkt_tree.column('executer', width=200, anchor=tk.CENTER)
        self.line_punkt_tree.column('month', width=100, anchor=tk.CENTER)

        self.line_punkt_tree.heading('equipment', text='Оборудование')
        self.line_punkt_tree.heading('location', text='Станция')
        self.line_punkt_tree.heading('executer', text='Исполнитель')
        self.line_punkt_tree.heading('month', text='Месяц')
        self.line_punkt_tree.bind('<Button-3>',self.drop_popup_menu)
        # self.line_punkt_tree.bind("<Double-1>", self.show_punkt)
        self.line_punkt_tree.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.YES)
        
        self.fill_certs_tree()

    def fill_certs_tree(self, equ='Все', loc='Все', exc='Все', mth='Все'):
        equ, loc, exc, mth = [False if i == 'Все' else i for i in (equ, loc, exc, mth)]
        for punkt in self.LinePunkts:
            if (punkt.equipment==equ or not equ ) and (punkt.location==loc or not loc) and (punkt.executer==exc or not exc) and (self.Month_assoc_back[punkt.month]==mth or not mth):
                self.line_punkt_tree.insert('', 'end', values=(punkt.equipment, punkt.location, punkt.executer, 
                                                        self.Month_assoc_back[punkt.month]+', '+self.Month_assoc_back[punkt.month+6]), 
                                                        tags=(punkt.id,))
    
    def refresh_tree_view(self, equ='Все', loc='Все', exc='Все', mth='Все'):
        for i in self.line_punkt_tree.get_children():
            self.line_punkt_tree.delete(i)
        self.fill_certs_tree(equ, loc, exc, mth)

    def fill_top_frame(self, version=0):
        for child in self.top_frame.winfo_children():
            child.destroy()

        if version == 0:
            self.fill_top_frame_regular(self.top_frame)
        elif version == 1:
            self.fill_top_frame_add(self.top_frame)
            
    def fill_top_frame_add(self, sub_top_frame):
        # configure styles to set tamplate text in entries
        style = ttk.Style()
        style.configure("Red.TEntry", foreground="gray")
        style.configure("Black.TEntry", foreground="black")

        # add equipment block
        self.equipment_label = ttk.Label(sub_top_frame, text="Оборудование") 
        self.equipment_label.place(x=10, y=5)
        
        self.equipment_entry = ttk.Entry(sub_top_frame)
        self.equipment_entry.insert(0,'OMS 1664  ')
        self.equipment_entry.configure(style="Red.TEntry")
        self.equipment_entry.bind('<FocusIn>', self.equipment_entry_FocusIn)
        self.equipment_entry.bind('<FocusOut>', self.equipment_entry_FocusOut)
        self.equipment_entry.place(x=10, y=23)

        # add station block
        self.location_label = ttk.Label(sub_top_frame, text="Станция") 
        self.location_label.place(x=110, y=5)
        
        self.location_entry = ttk.Entry(sub_top_frame)
        self.location_entry.insert(0, 'Иловайск  ')
        self.location_entry.config(style='Red.TEntry')
        self.location_entry.bind('<FocusIn>', self.location_entry_FocusIn)
        self.location_entry.bind('<FocusOut>', self.location_entry_FocusOut)
        self.location_entry.place(x=110, y=23)

        # add executer block
        executer_label = ttk.Label(sub_top_frame, text="Исполнитель") 
        executer_label.place(x=210, y=5)
        
        self.executer_entry = ttk.Entry(sub_top_frame)
        self.executer_entry.insert(0, 'Теряев Е.А.  ')
        self.executer_entry.config(style='Red.TEntry')
        self.executer_entry.bind('<FocusIn>', self.executer_entry_FocusIn)
        self.executer_entry.bind('<FocusOut>', self.executer_entry_FocusOut)
        self.executer_entry.place(x=210, y=23)

        # sub function to calculation for month block
        def month_pair(one=None, two=None):
            if not two:
                two = 6
            if one:
                return (one, one+6)
            return (two-6, two)

        # function to add month block
        def post_month_comboboxes(start_pair):
            month_start_label = ttk.Label(sub_top_frame, text="Месяц") 
            month_start_label.place(x=330, y=5)
            self.month_start_combo = ttk.Combobox(sub_top_frame, values=['Январь','Февраль','Март','Апрель','Май','Июнь'], justify='center')
            self.month_start_combo.current(start_pair[0])
            self.month_start_combo.place(x=330, y=23)
            self.month_start_combo.bind('<<ComboboxSelected>>', lambda x:  post_month_comboboxes(month_pair(one=self.Month_assoc[self.month_start_combo.get()])))

            month_finish_combo = ttk.Combobox(sub_top_frame, values=['Июль','Август', 'Сентябрь','Октябрь','Ноябрь','Декабрь'], justify='center')
            month_finish_combo.current(start_pair[1]-6)
            month_finish_combo.place(x=330, y=43)
            month_finish_combo.bind('<<ComboboxSelected>>', lambda x:  post_month_comboboxes(month_pair(two=self.Month_assoc[month_finish_combo.get()])))

            # return month_start_combo, month_finish_combo
        # add month block
        post_month_comboboxes(month_pair())

        # add conform button
        add_button = ttk.Button(sub_top_frame, text="Добавить", command=lambda:(self.LinePunkts.add_cert(self.equipment_entry.get(),
                                                                                                self.location_entry.get(),
                                                                                                self.executer_entry.get(),
                                                                                                self.Month_assoc[self.month_start_combo.get()]),
                                                                                self.LinePunkts.refresh(),
                                                                                self.refresh_tree_view()))
        add_button.place(x=470, y=20)

        # add back button
        back_button = ttk.Button(sub_top_frame, text="Назад", command=lambda: self.fill_top_frame(version=0))
        back_button.place(x=470, y=43)

    def fill_top_frame_regular(self, frame:tk.Frame)-> None:

        def call_refresh_tree_vie(event):
            self.refresh_tree_view(equipment_s_combo.get(), location_s_combo.get(), executer_s_combo.get(), month_s_combo.get())

        # block of equipment selection
        equipment_s_label = tk.Label(frame, text="Оборудование")
        equipment_s_label.place(x=10, y=5)
        equipments = [i for i in set(c.equipment for c in self.LinePunkts)]
        equipments.append("Все")
        equipment_s_combo = ttk.Combobox(frame, values=equipments)
        equipment_s_combo.current(len(equipments)-1)
        equipment_s_combo.bind('<<ComboboxSelected>>', call_refresh_tree_vie)
        equipment_s_combo.place(x=10, y=25)

        # block of location selection
        location_s_label = ttk.Label(frame, text="Станция")
        location_s_label.place(x=150, y=5)
        locations = [i for i in set(c.location for c in self.LinePunkts)]
        locations.append("Все")
        location_s_combo = ttk.Combobox(frame, values=locations)
        location_s_combo.current(len(locations)-1)
        location_s_combo.bind('<<ComboboxSelected>>', call_refresh_tree_vie)
        location_s_combo.place(x=150, y=25)
        
        # block of executer selection
        executer_s_label = ttk.Label(frame, text="Исполнитель")
        executer_s_label.place(x=290, y=5)
        executers = [i for i in set(c.executer for c in self.LinePunkts)]
        executers.append('Все')
        executer_s_combo = ttk.Combobox(frame, values=executers)
        executer_s_combo.current(len(executers)-1)
        executer_s_combo.bind('<<ComboboxSelected>>', call_refresh_tree_vie)
        executer_s_combo.place(x=290, y=25)

        # block of month selection
        month_s_label = ttk.Label(frame, text="Месяц")
        month_s_label.place(x=430, y=5)
        months = [i for i in set(self.Month_assoc_back[c.month] for c in self.LinePunkts)]
        months.append('Все')
        month_s_combo = ttk.Combobox(frame, values=months)
        month_s_combo.current(len(months)-1)
        month_s_combo.bind('<<ComboboxSelected>>', call_refresh_tree_vie)
        month_s_combo.place(x=430, y=25)

    def drop_popup_menu(self, event):
        """action in event of button 3 on tree view"""
        # select row under mouse 
        iid = self.line_punkt_tree.identify_row(event.y)
        if iid:
            # mouse pointer over item
            self.line_punkt_tree.selection_set(iid)
            self.popup_menu.post(event.x_root, event.y_root)
        else:
           pass

    def delete_cert(self):
        item = self.line_punkt_tree.selection()[0]
        self.LinePunkts.get_cert_by_id(self.line_punkt_tree.item(item,'tags')[0]).GUI_delete()
        self.LinePunkts.refresh()
        self.refresh_tree_view()

    # function to set template for equipment entry
    def equipment_entry_FocusIn(self,event):
        """function that gets called whenever entry is clicked"""
        if self.equipment_entry.get() == 'OMS 1664  ':
            self.equipment_entry.delete(0, "end")               # delete all the text in the entry
            self.equipment_entry.insert(0, '')                  #Insert blank for user input
            self.equipment_entry.configure(style="Black.TEntry")
    def equipment_entry_FocusOut(self,event):
        if self.equipment_entry.get() == '':
            self.equipment_entry.insert(0, 'OMS 1664  ')
            self.equipment_entry.configure(style="Red.TEntry")

    # function to set template for location entry
    def location_entry_FocusIn(self,event):
        """function that gets called whenever entry is clicked"""
        if self.location_entry.get() == 'Иловайск  ':
            self.location_entry.delete(0, "end")                # delete all the text in the entry
            self.location_entry.insert(0, '')                   #Insert blank for user input
            self.location_entry.configure(style="Black.TEntry")
    def location_entry_FocusOut(self,event):
        if self.location_entry.get() == '':
            self.location_entry.insert(0, 'Иловайск  ')
            self.location_entry.configure(style="Red.TEntry")

    # function to set template for executor entry
    def executer_entry_FocusIn(self, event):
        """function that gets called whenever entry is clicked"""
        if self.executer_entry.get() == 'Теряев Е.А.  ':
            self.executer_entry.delete(0, "end")            # delete all the text in the entry
            self.executer_entry.insert(0, '')               #Insert blank for user input
            self.executer_entry.configure(style="Black.TEntry")
    def executer_entry_FocusOut(self, event):
        if self.executer_entry.get() == '':
            self.executer_entry.insert(0, 'Теряев Е.А.  ')
            self.executer_entry.configure(style="Red.TEntry")
        




class LinePunkts(basePunktsWindow):
    def __init__ (self, main):
        super().__init__ (main)
        self.main=main
        self.LinePunkts = self.main.LinePunkts
        self.bind('<Escape>', lambda e: self.destroy())
        self.title("Техпроцесс на линии")
        self.geometry("600x350")
        self.minsize(600,350)
        self.resizable(False,False)
        self.Month_assoc = {'Январь':0, 'Февраль':1, 'Март':2, 'Апрель':3, 'Май':4, 'Июнь':5, 'Июль':6, 'Август':7,
                                                        'Сентябрь':8, 'Октябрь':9, 'Ноябрь':10, 'Декабрь':11}
        self.Month_assoc_back = {0:'Январь', 1:'Февраль', 2:'Март', 3:'Апрель', 4:'Май', 5:'Июнь', 6:'Июль', 7:'Август',
                                                        8:'Сентябрь', 9:'Октябрь', 10:'Ноябрь', 11:'Декабрь'}
        self.init_certification_window()
class Certifications(basePunktsWindow):
    def __init__(self, main):
        super().__init__ (main)
        self.main=main
        self.LinePunkts = self.main.Certifications
        self.bind('<Escape>', lambda e: self.destroy())
        self.title("Паспортизация")
        self.geometry("400x350")
        self.minsize(600,350)
        self.resizable(False,False)
        self.Month_assoc = {'Январь':0, 'Февраль':1, 'Март':2, 'Апрель':3, 'Май':4, 'Июнь':5, 'Июль':6, 'Август':7,
                                                        'Сентябрь':8, 'Октябрь':9, 'Ноябрь':10, 'Декабрь':11}
        self.Month_assoc_back = {0:'Январь', 1:'Февраль', 2:'Март', 3:'Апрель', 4:'Май', 5:'Июнь', 6:'Июль', 7:'Август',
                                                        8:'Сентябрь', 9:'Октябрь', 10:'Ноябрь', 11:'Декабрь'}
        self.init_certification_window()
        
    def fill_certs_tree(self, equ='Все', loc='Все', exc='Все', mth='Все'):
        equ, loc, exc, mth = [False if i == 'Все' else i for i in (equ, loc, exc, mth)]
        for punkt in self.LinePunkts:
            if (punkt.equipment==equ or not equ ) and (punkt.location==loc or not loc) and (punkt.executer==exc or not exc) and (self.Month_assoc_back[punkt.month]==mth or not mth):
                self.line_punkt_tree.insert('', 'end', values=(punkt.equipment, punkt.location, punkt.executer, 
                                                        self.Month_assoc_back[punkt.month]), 
                                                        tags=(punkt.id,))

    def fill_top_frame_add(self, sub_top_frame):
        # configure styles to set tamplate text in entries
        style = ttk.Style()
        style.configure("Red.TEntry", foreground="gray")
        style.configure("Black.TEntry", foreground="black")

        # add equipment block
        self.equipment_label = ttk.Label(sub_top_frame, text="Оборудование") 
        self.equipment_label.place(x=10, y=5)
        
        self.equipment_entry = ttk.Entry(sub_top_frame)
        self.equipment_entry.insert(0,'OMS 1664  ')
        self.equipment_entry.configure(style="Red.TEntry")
        self.equipment_entry.bind('<FocusIn>', self.equipment_entry_FocusIn)
        self.equipment_entry.bind('<FocusOut>', self.equipment_entry_FocusOut)
        self.equipment_entry.place(x=10, y=23)

        # add station block
        self.location_label = ttk.Label(sub_top_frame, text="Станция") 
        self.location_label.place(x=110, y=5)
        
        self.location_entry = ttk.Entry(sub_top_frame)
        self.location_entry.insert(0, 'Иловайск  ')
        self.location_entry.config(style='Red.TEntry')
        self.location_entry.bind('<FocusIn>', self.location_entry_FocusIn)
        self.location_entry.bind('<FocusOut>', self.location_entry_FocusOut)
        self.location_entry.place(x=110, y=23)

        # add executer block
        executer_label = ttk.Label(sub_top_frame, text="Исполнитель") 
        executer_label.place(x=210, y=5)
        
        self.executer_entry = ttk.Entry(sub_top_frame)
        self.executer_entry.insert(0, 'Теряев Е.А.  ')
        self.executer_entry.config(style='Red.TEntry')
        self.executer_entry.bind('<FocusIn>', self.executer_entry_FocusIn)
        self.executer_entry.bind('<FocusOut>', self.executer_entry_FocusOut)
        self.executer_entry.place(x=210, y=23)

        # sub function to calculation for month block
        def month_pair(one=None, two=None):
            if not two:
                two = 6
            if one:
                return (one, one+6)
            return (two-6, two)

        # function to add month block
        month_start_label = ttk.Label(sub_top_frame, text="Месяц") 
        month_start_label.place(x=330, y=5)
        month_start_combo = ttk.Combobox(sub_top_frame, values=['Январь','Февраль','Март','Апрель','Май',
                                                                'Июнь','Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь'], justify='center')
        month_start_combo.current(0)
        month_start_combo.place(x=330, y=23)

        # add conform button
        add_button = ttk.Button(sub_top_frame, text="Добавить", command=lambda:(self.LinePunkts.add_cert(self.equipment_entry.get(),
                                                                                                self.location_entry.get(),
                                                                                                self.executer_entry.get(),
                                                                                                self.Month_assoc[self.month_start_combo.get()]),
                                                                                self.LinePunkts.refresh(),
                                                                                self.refresh_tree_view()))
        add_button.place(x=470, y=20)

        # add back button
        back_button = ttk.Button(sub_top_frame, text="Назад", command=lambda: self.fill_top_frame(version=0))
        back_button.place(x=470, y=43)
