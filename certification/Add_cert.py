import tkinter as tk
from tkinter import ttk

class Add_cert(tk.Toplevel):
    def __init__ (self, main):
        super().__init__ (main)
        self.main=main
        self.certifications = self.main.Certifications
        self.Punkts = self.main.Punkts
        self.bind('<Escape>', lambda e: self.destroy())
        self.title("Добавить пункт")
        self.geometry("600x350")
        self.minsize(600,350)
        self.resizable(False,False)
        self.init_certification_window()

    def init_add_cert_window(self):


        self.grab_set()
        self.focus_set()