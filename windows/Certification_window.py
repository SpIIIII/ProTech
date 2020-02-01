import tkinter as tk
from tkinter import ttk

class Certification(tk.Toplevel):
    def __init__ (self, main):
        super().__init__ (main)
        self.main=main
        self.certifications = self.main.Certifications
        self.Punkts = self.main.Punkts
        self.bind('<Escape>', lambda e: self.destroy())
        self.title("Паспортизация")
        self.geometry("600x350")
        self.minsize(600,350)
        self.resizable(False,False)
        self.Month_assoc = {'Январь':0, 'Февраль':1, 'Март':2, 'Апрель':3, 'Май':4, 'Июнь':5, 'Июль':6, 'Август':7,
                                                        'Сентябрь':8, 'Октябрь':9, 'Ноябрь':10, 'Декабрь':11}
        self.Month_assoc_back = {0:'Январь', 1:'Февраль', 2:'Март', 3:'Апрель', 4:'Май', 5:'Июнь', 6:'Июль', 7:'Август',
                                                        8:'Сентябрь', 9:'Октябрь', 10:'Ноябрь', 11:'Декабрь'}
        self.init_certification_window()
        
    def init_certification_window(self):
        # Draw Frames
        self.top_frame = ttk.Frame(self, height=68)
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.bottom_frame = ttk.Frame(self)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.fill_top_frame()
        self.fill_bottom_frame()
         # Draw MenuBar
        menubar = tk.Menu()
        filemenu = tk.Menu(menubar, tearoff=0)
        
        filemenu.add_command(label="Добавить", command=lambda: self.fill_top_frame(version=1))
        filemenu.add_separator()
        filemenu.add_command(label="Выход", command=self.destroy)
        
        menubar.add_cascade(label="Файл", menu=filemenu)
        self.config(menu=menubar)

        #fill top_frame

        self.grab_set()
        self.focus_set()

    def fill_bottom_frame(self):
        # create and fill tree view
        self.certs_tree = ttk.Treeview(self.bottom_frame, columns=('equipment', 'location', 'executer', 'month'), height=15, show='headings')

        self.certs_tree.column('equipment', width=60, anchor=tk.CENTER)
        self.certs_tree.column('location', width=60, anchor=tk.E)
        self.certs_tree.column('executer', width=200, anchor=tk.CENTER)
        self.certs_tree.column('month', width=100, anchor=tk.CENTER)

        self.certs_tree.heading('equipment', text='Оборудование')
        self.certs_tree.heading('location', text='Станция')
        self.certs_tree.heading('executer', text='Исполнитель')
        self.certs_tree.heading('month', text='Месяц')
        # self.certs_tree.bind('<Button-3>',self.drop_popup_menu)
        # self.certs_tree.bind("<Double-1>", self.show_punkt)
        self.certs_tree.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.YES)
        
        self.fill_certs_tree()

    def fill_certs_tree(self):
        for cert in self.certifications:
            self.certs_tree.insert('', 'end', values=(cert.equipment, cert.location, cert.executer, 
                                                        self.Month_assoc_back[cert.month]+', '+self.Month_assoc_back[cert.month+6]))

    def fill_top_frame(self, version=0):
        for child in self.top_frame.winfo_children():
            child.destroy()

        if version == 0:
            pass
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
            month_start_combo = ttk.Combobox(sub_top_frame, values=['Январь','Февраль','Март','Апрель','Май','Июнь'], justify='center')
            month_start_combo.current(start_pair[0])
            month_start_combo.place(x=330, y=23)
            month_start_combo.bind('<<ComboboxSelected>>', lambda x:  post_month_comboboxes(month_pair(one=self.Month_assoc[month_start_combo.get()])))

            month_finish_combo = ttk.Combobox(sub_top_frame, values=['Июль','Август', 'Сентябрь','Октябрь','Ноябрь','Декабрь'], justify='center')
            month_finish_combo.current(start_pair[1]-6)
            month_finish_combo.place(x=330, y=43)
            month_finish_combo.bind('<<ComboboxSelected>>', lambda x:  post_month_comboboxes(month_pair(two=self.Month_assoc[month_finish_combo.get()])))

            return month_start_combo, month_finish_combo
        # add month block
        month_start_combo, _ = post_month_comboboxes(month_pair())

        # add conform button
        add_button = ttk.Button(sub_top_frame, text="Добавить", command=lambda:self.certifications.add_cert(self.equipment_entry.get(),
                                                                                                self.location_entry.get(),
                                                                                                self.executer_entry.get(),
                                                                                self.Month_assoc[month_start_combo.get()]))
        add_button.place(x=470, y=20)

    def fill_top_frame_regular(self):
        pass

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
        

