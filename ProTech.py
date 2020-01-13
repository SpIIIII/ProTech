import tkinter as tk
import platform
import config
import os
from DB import DB
from plots import Plot
from tkinter import ttk
from windows import Main
from punkts import Punkts
from updater import Updater
from version import Version
from datetime import timedelta
from create_output import Output

   

if __name__ ==  "__main__":

    config.IS_WINDOWS = True if platform.system() == 'Windows' else False
   
    root=tk.Tk()

    db=DB.DB()
    
    Version = Version.Versions()
    Updater = Updater.Updater(Version)
    
    Punkts = Punkts.Punkts(db)
    Plot = Plot.Plot(Punkts)
    Outputter = Output.Output(Punkts)

    app = Main.Main(root, Punkts, Version, Updater, Plot, Outputter)
    app.pack()
    root.title("Техпроцесс ")
    root.geometry("580x350+300+220")
    #root.resizable(False,False)
    
    root.minsize(580,350)
    root.mainloop()


