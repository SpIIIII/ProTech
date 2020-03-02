import tkinter as tk
import platform
import config
import os

from DB import DB, DB_linePunkts

from plots import Plot
from tkinter import ttk
from windows import Main
from punkts import Punkts
from updater import Updater
from version import Version
from datetime import timedelta
from create_output import Output
from linePunkts import LineProcessShedule

   

if __name__ ==  "__main__":

    config.IS_WINDOWS = True if platform.system() == 'Windows' else False
   
    root = tk.Tk()

    db = DB.DB()
    db_lp = DB_linePunkts.DB_linePunkts()
    db_c = DB_linePunkts.DB_certifications()
    
    Version = Version.Versions()
    Updater = Updater.Updater(Version)
    
    Punkts = Punkts.Punkts(db)
    LinePunkts = LineProcessShedule.LinePunkts(db_lp)
    CertPunkts = LineProcessShedule.CertPunkts(db_c)
    Plot = Plot.Plot(Punkts)
    Outputter = Output.Output(Punkts, LinePunkts, CertPunkts)


    app = Main.Main(root, Punkts, Version, Updater, Plot, Outputter, LinePunkts, CertPunkts)
    app.pack()
    root.title("Техпроцесс ")
    root.geometry("580x350+300+220")
    #root.resizable(False,False)
    
    root.minsize(580,350)
    root.mainloop()


