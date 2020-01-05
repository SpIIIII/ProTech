import tkinter as tk
from tkinter import ttk
import textwrap


class ShowOneDay(tk.Toplevel):
    
    def __init__ (self,root, punkts):
        super().__init__ (root)
        self.punkts = punkts
        self.bind('<Escape>', lambda e: self.destroy())
        self.show_onedaypunkt()

    def myWrap(self,string, lenght=8):
        return '\n'.join(textwrap.wrap(string, lenght))

    def show_onedaypunkt (self):
        self.title("Вывести в Exel")
        self.geometry("500x600")

        self.style=ttk.Style(self)
        self.style.configure('mystyle.Treeview',rowheight=110)
        
        self.sctribeTree=ttk.Treeview(self,columns=('id','description'),height=40,show='headings',style="mystyle.Treeview")
       
        self.sctribeTree.column('id',width=20,anchor=tk.N)
        self.sctribeTree.column('description',width=380,anchor=tk.N)
        self.sctribeTree.heading('id',text='пункт')
        self.sctribeTree.heading('description',text='описание')
        self.sctribeTree.pack(side=tk.BOTTOM,fill=tk.BOTH, expand=tk.YES)

        self.scrollbar = ttk.Scrollbar(self,orient='vertical',command=self.sctribeTree.yview)
        self.scrollbar.pack( side = tk.RIGHT, fill = tk.Y )
         
        
        self.sctribeTree.configure(yscrollcommand=self.scrollbar.set)
   
        for x in self.punkts.today_punkts(name_only = False):
            self.sctribeTree.insert("", "end", values=(x.name, '\n'.join(textwrap.wrap(x.description,35))))
            
        self.wait_visibility()
        self.grab_set()
        self.focus_set()

    