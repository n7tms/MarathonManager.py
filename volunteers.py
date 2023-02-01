# Marathon Manager
#
# Volunteer Screen
#

import sqlite3
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from constants import *
import csv


class VolunteersWindow():

    def __init__(self,master):

        self.master = master

        self.root = tk.Frame(master)
        self.root.pack()

        master.title("MM: Volunteers")
        master.geometry('550x400')

        self.cn = sqlite3.connect(DB_NAME)
        self.cur = self.cn.cursor()

        self.title = ttk.Label(self.root,text='Volunteers',font=('Arial',18))
        self.title.grid(row=0,column=0,columnspan=2,sticky='nw')

        self.lblLogo = ttk.Label(self.root,text="Logo Placeholder")
        self.lblLogo.grid(row=0,column=2,rowspan=2,sticky='news')

        self.btnNew = ttk.Button(self.root,text="New Volunteer",command=self.new_volunteer)
        self.btnNew.grid(row=2,column=0,padx=5,pady=5,sticky='w')

        self.btnImport = ttk.Button(self.root,text="Import Volunteers",command=self.volunteers_import)
        self.btnImport.grid(row=2,column=1,padx=5,pady=5,sticky='w')


        self.tvVolunteer = ttk.Treeview(self.root,column=("1","2","3","4"),show='headings',selectmode='browse')
        
        self.tvVolunteer.column("1",anchor='center',minwidth=0,width=50)
        self.tvVolunteer.heading("1",text="ID")
        self.tvVolunteer.column("2",anchor='w',minwidth=0,width=200)
        self.tvVolunteer.heading("2",text="Name",anchor='w')
        self.tvVolunteer.column("3",anchor='w',minwidth=0,width=100)
        self.tvVolunteer.heading("3",text="Call Sign",anchor='w')
        self.tvVolunteer.column("4",anchor='w',minwidth=0,width=100)
        self.tvVolunteer.heading("4",text="Assignment",anchor='w')
        self.tvVolunteer.grid(row=4,column=0,columnspan=3,padx=5,pady=5)
        self.tvVolunteer.bind("<Double-1>",self.volunteer_edit_row)

        self.yscrollbar = ttk.Scrollbar(self.root,orient='vertical',command=self.tvVolunteer.yview)
        self.yscrollbar.grid(row=4, column=3,pady=15,sticky='nse')
        self.yscrollbar.configure(command=self.tvVolunteer.yview)    
        self.tvVolunteer.configure(yscrollcommand=self.yscrollbar.set)

        self.btnCancel = ttk.Button(self.root,text="Cancel",command=self.volunteer_cancel)
        self.btnCancel.grid(row=6,column=2,padx=5,pady=5,sticky='e')

    def new_volunteer(self):
        pass


    def volunteer_edit_row(self):
        pass


    def volunteer_cancel(self):
        """Cancel everything and close this window"""
        self.master.destroy()

    def volunteers_import(self):
        pass





