import tkinter as tk
import textwrap
from tkinter import ttk

class Show_punkt(tk.Toplevel):
    def __init__ (self, main, punkt):
        super().__init__(main)
        self.main = main
        self.title('Пункт')
        self.geometry("640x430")
        self.minsize(600,350)
        self.resizable(False, False)
        self.bind('<Escape>', lambda e: self.destroy())

        self.punkt = punkt
        self.change_punct = self.main.change_punkt
        

        self.init_show_punkt()

    def init_show_punkt(self):
        """ Draw main window of Show_punkt """

        ## add frames
        self.top_frame = ttk.Frame(self, height=50)
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

        self.bottom_frame = tk.Frame(self, bg = 'white')
        self.bottom_frame.pack(side=tk.BOTTOM,fill=tk.BOTH, expand=True)

        # add labels
        self.label_punkt_name = ttk.Label(self.top_frame, text = self.punkt.name,font=("TimesNewRoman", 18))
        self.label_punkt_name.place(x = 300, y = 15)

        self.label_punkt_deskription_intro = tk.Label(self.bottom_frame, text = 'Описание:', bg = 'white', justify = 'left')
        self.label_punkt_deskription_intro.place(x=10, y=150)

        self.label_punkt_deskription = tk.Label(self.bottom_frame, text = '\n'.join(textwrap.wrap(self.punkt.description,40)), bg = 'white', justify = 'left')
        self.label_punkt_deskription.place(x=20, y=170)

        self.label_day = tk.Label(self.bottom_frame, text = f'День выполнения - {self.punkt.day_of_week}', bg = 'white')
        self.label_day.place(x=10, y=10)
        
        if self.punkt.period == ' раз 12 месяцев' or self.punkt.period == ' раз в 6 месяцев':
            self.label_day = tk.Label(self.bottom_frame, text = f'Месяц - {self.punkt.month}', bg = 'white')
            self.label_day.place(x=170, y=10)

        self.label_period = tk.Label(self.bottom_frame, text = f'Периодичность - {self.punkt.period}', bg = 'white')
        self.label_period.place(x=10, y=30)

        self.label_instruction = tk.Label(self.bottom_frame, text = f'Инструкция - {self.punkt.instruction}', bg = 'white')
        self.label_instruction.place(x=10, y=50)

        self.label_order = tk.Label(self.bottom_frame, text = f'Приказ - {self.punkt.order}', bg = 'white')
        self.label_order.place(x=10, y=70)
        
        self.label_responsible = tk.Label(self.bottom_frame, text = f'Исполнитель - {self.punkt.responsible}', bg = 'white')
        self.label_responsible.place(x=10, y=90)

        self.label_responsible = tk.Label(self.bottom_frame, text = f'Оборудование - {self.punkt.equipment}', bg = 'white')
        self.label_responsible.place(x=10, y=110)

        #add buttons 
        self.button_change = ttk.Button(self.bottom_frame, text = 'Изменить', command = self.open_change_punkt)
        self.button_change.place(x = 10, y = 350)

        self.button_delete = ttk.Button(self.bottom_frame, text = 'Удалить', command = self.open_delete_punkt)
        self.button_delete.place(x = 535, y = 350)

        self.wait_visibility()
        self.grab_set()
        self.focus_set()

    def open_change_punkt(self):
        self.change_punct(self.main, self.punkt)

    def open_delete_punkt(self):
        self.punkt.GUI_delete()
        self.main.refresh_tree_view()

    

        

