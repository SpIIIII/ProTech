
import tkinter as tk


class Analysis(tk.Toplevel):
    def __init__(self,root,punkts,plot):
        super().__init__(root)
        self.plot = plot
        self.punkts = punkts
        self.title("Анализ")
        self.geometry("600x500")
        self.minsize(600,350)
        self.bind('<Escape>', lambda e: self.destroy())
        self.init_analysis()

    

    def init_analysis(self):
        # add frames
        top_frame = tk.Frame(self)
        top_frame.pack(side=tk.TOP,fill=tk.BOTH, expand=True)

        bottom_frame = tk.Frame(self)
        bottom_frame.pack(side=tk.BOTTOM,fill=tk.BOTH, expand=True)

        # Draw MenuBar
        menubar = tk.Menu()
        filemenu = tk.Menu(menubar, tearoff=0)
          
        filemenu.add_separator()
        filemenu.add_command(label="Выход", command=self.destroy)
        
        menubar.add_cascade(label="Файл", menu=filemenu)
        self.config(menu=menubar)

        self.plot.draw_plot(bottom_frame)
        self.grab_set()
        self.focus_set()
