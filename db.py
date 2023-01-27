import sqlite3


class DB:
    def __init__(self):
        self.dbname = 'test.db'




 
import tkinter as tk
import tkinter.ttk as ttk
 
root = tk.Tk()
vstring = tk.IntVar()
values = [
    ("Rome 1"),
    ("Paris 2"),
    ("London 3"),
    ("New York 4")
]
 
 
style = ttk.Style()
style.configure("BW.TRadiobutton", foreground="red", background="yellow")
 
def selection():
    print(vstring.get())

for v in values:
	# Here is the ttk style widget
    rb = ttk.Radiobutton(root,text=v[:-1],value= v[-1],variable = vstring,style = "BW.TRadiobutton",command=selection)
    rb.pack(anchor=tk.W)
 
root. mainloop()