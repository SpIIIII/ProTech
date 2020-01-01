import tkinter as tk
from DB import DB
from tkinter import ttk
from windows import Main
from punkts import Punkts
from updater import update
from version import Version
from datetime import timedelta
from tkinter import messagebox
   

if __name__ ==  "__main__":
    
    root=tk.Tk()
    db=DB.DB()
    punkts = Punkts.Punkts(db)

    version = Version.Versions()
    updater = update.Update(version)
    app = Main.Main(root, punkts, version, updater)
    app.pack()
    root.title("Техпроцесс")
    root.geometry("580x350+300+220")
    #root.resizable(False,False)
    
    root.minsize(580,350)
    root.mainloop()


