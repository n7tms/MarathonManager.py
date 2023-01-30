# Marathon Manager - Events Window

import sqlite3
from pathlib import Path
# from tkinter import Tk
from tkinter import ttk
# from tkinter import
import tkinter as tk
from tkinter import messagebox
from tkinter import colorchooser
from datetime import datetime
from constants import *

class EventsWindow:
    
    def __init__(self):

        self.root = tk.Tk()
        self.root.title("MM: Events")
        self.root.geometry('450x200')
        self.root.minsize(400,100)

        self.cn = sqlite3.connect(DB_NAME)
        self.cur = self.cn.cursor()


        # img2 = ImageTk.PhotoImage(file='runner_blue.png')
        # imgLogo = ttk.Label(main_frame,image=img2)
        imgLogo = ttk.Label(self,text="logo placeholder")
        imgLogo.grid(row=0,column=0,rowspan=5)

        lblEventName = ttk.Label(self,text='Event Name:',width=12)
        lblEventName.grid(row=0,column=1,sticky='e', padx=5, pady=8)
        txtEventName = ttk.Entry(self,width=25)
        txtEventName.grid(row=0,column=2, columnspan=2,sticky='w')

        lblDescription = ttk.Label(self,text='Description:',width=12)
        lblDescription.grid(row=1,column=1,sticky='e',padx=5, pady=8)
        txtDescription = tk.Entry(self,width=25)
        txtDescription.grid(row=1,column=2, columnspan=2,sticky='w',padx=5, pady=8)

        lblLocation = ttk.Label(self,text='Location:',width=12)
        lblLocation.grid(row=2,column=1,sticky='e')
        txtLocation = tk.Entry(self,width=10)
        txtLocation.grid(row=2,column=2,sticky='w')

        lblStartDate = ttk.Label(self,text='Start Date:',width=12)
        lblStartDate.grid(row=3,column=1,sticky='e')
        txtStartDate = tk.Entry(self,width=10)
        txtStartDate.grid(row=3,column=2,sticky='w')

        lblStartTime = ttk.Label(self,text='Start Time:',width=12)
        lblStartTime.grid(row=4,column=1,sticky='e')
        txtStartTime = tk.Entry(self,width=10)
        txtStartTime.grid(row=4,column=2,sticky='w')

        butSave = ttk.Button(self,text='Save',command=self.event_save)
        butSave.grid(row=3,column=3)
        butCancel = ttk.Button(self,text='Cancel',command=self.event_cancel)
        butCancel.grid(row=4,column=3)



    def event_save(self):
        # get the field values
        eName = txtEventName.get()
        eDescription = txtDescription.get()
        eLocation = txtLocation.get()
        eDate = txtStartDate.get()
        eTime = txtStartTime.get()
        eStart = eDate + ' ' + eTime

        # TODO: Error checking; Do the fields contain valid information

        stmt = "insert into Events (EventName, Description, Location, Starttime) values ('" + eName + "','" + eDescription + "','" + eLocation + "','" + eStart + "');"
        res =  cur.execute(stmt)
        cn.commit()
        self.e_root.destroy()

    def event_cancel(self):
        self.e_root.destroy()



