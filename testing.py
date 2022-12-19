from tkinter import *

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.title = "Temp Converter"

        menu = Menu(self.master)
        self.master.config(menu=menu)

        fileMenu = Menu(menu)
        fileMenu.add_command(label="Item")
        fileMenu.add_command(label="Exit", command=self.exitProgram)
        menu.add_cascade(label="File", menu=fileMenu)

        editMenu = Menu(menu)
        editMenu.add_command(label="Undo")
        editMenu.add_command(label="Redo")
        menu.add_cascade(label="Edit", menu=editMenu)

    def exitProgram(self):
        exit()


root = Tk()
app = Window(root)
root.mainloop()

# def f_to_c():
#     fahreneit = ent_temp.get()
#     celsius = (5 / 9) * (float(fahreneit) - 32)
#     lbl_result["text"] = f"{round(celsius,2)} \N{DEGREE CELSIUS}"





# frm_entry = tk.Frame(master=window)
# ent_temp = tk.Entry(master=frm_entry,width=10)
# lbl_temp = tk.Label(master=frm_entry, text="\N{DEGREE FAHRENHEIT}")

# ent_temp.grid(row=0,column=0,sticky="e")
# lbl_temp.grid(row=0,column=1,sticky="w")

# btn_Convert = tk.Button(master=window, text="\N{RIGHTWARDS BLACK ARROW}", command=f_to_c)
# lbl_result = tk.Label(master=window, text="\N{DEGREE CELSIUS}")

# frm_entry.grid(row=0,column=0,padx=10)
# btn_Convert.grid(row=0,column=1,pady=10)
# lbl_result.grid(row=0,column=2,padx=10)

# window.mainloop()