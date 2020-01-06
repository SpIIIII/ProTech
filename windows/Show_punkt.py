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

        self.label_punkt_deskription = tk.Label(self.bottom_frame, text = '\n'.join(textwrap.wrap(self.punkt.description,40)), bg = 'white', justify = 'left')
        self.label_punkt_deskription.place(x = 10, y = 150)

        #add buttons 
        self.button_change = ttk.Button(self.bottom_frame, text = 'Изменить', command = self.open_change_punkt)
        self.button_change.place(x = 10, y = 350)

        self.button_delete = ttk.Button(self.bottom_frame, text = 'Удалить', command = self.open_delete_punkt)
        self.button_delete.place(x = 535, y = 350)

    def open_change_punkt(self):
        self.change_punct(self.main, self.punkt)

    def open_delete_punkt(self):
        self.punkt.GUI_delete()
        self.main.refresh_tree_view()

        

