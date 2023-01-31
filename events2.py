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
    
    def __init__(self,master):

        # self.root = tk.Tk()
        # self.root = master

        root = tk.Frame(master)
        root.pack()

        master.title("MM: Events")
        master.geometry('450x200')
        master.minsize(400,100)

        self.cn = sqlite3.connect(DB_NAME)
        self.cur = self.cn.cursor()


        # img2 = ImageTk.PhotoImage(file='runner_blue.png')
        # imgLogo = ttk.Label(main_frame,image=img2)
        self.imgLogo = ttk.Label(root,text="logo placeholder")
        self.imgLogo.grid(row=0,column=0,rowspan=5)

        self.lblEventName = ttk.Label(root,text='Event Name:',width=12)
        self.lblEventName.grid(row=0,column=1,sticky='e', padx=5, pady=8)
        self.txtEventName = ttk.Entry(root,width=25)
        self.txtEventName.grid(row=0,column=2, columnspan=2,sticky='w')

        # self.lblDescription = ttk.Label(self,text='Description:',width=12)
        # self.lblDescription.grid(row=1,column=1,sticky='e',padx=5, pady=8)
        # self.txtDescription = tk.Entry(self,width=25)
        # self.txtDescription.grid(row=1,column=2, columnspan=2,sticky='w',padx=5, pady=8)

        # self.lblLocation = ttk.Label(self,text='Location:',width=12)
        # self.lblLocation.grid(row=2,column=1,sticky='e')
        # self.txtLocation = tk.Entry(self,width=10)
        # self.txtLocation.grid(row=2,column=2,sticky='w')

        # self.lblStartDate = ttk.Label(self,text='Start Date:',width=12)
        # self.lblStartDate.grid(row=3,column=1,sticky='e')
        # self.txtStartDate = tk.Entry(self,width=10)
        # self.txtStartDate.grid(row=3,column=2,sticky='w')

        # self.lblStartTime = ttk.Label(self,text='Start Time:',width=12)
        # self.lblStartTime.grid(row=4,column=1,sticky='e')
        # self.txtStartTime = tk.Entry(self,width=10)
        # self.txtStartTime.grid(row=4,column=2,sticky='w')

        # self.butSave = ttk.Button(self,text='Save',command=self.event_save)
        # self.butSave.grid(row=3,column=3)
        self.butCancel = ttk.Button(root,text='Cancel',command=self.event_cancel)
        self.butCancel.grid(row=4,column=3)



    def event_save(self):
        # get the field values
        eName = self.txtEventName.get()
        eDescription = self.txtDescription.get()
        eLocation = self.txtLocation.get()
        eDate = self.txtStartDate.get()
        eTime = self.txtStartTime.get()
        eStart = eDate + ' ' + eTime

        # TODO: Error checking; Do the fields contain valid information

        stmt = "insert into Events (EventName, Description, Location, Starttime) values ('" + eName + "','" + eDescription + "','" + eLocation + "','" + eStart + "');"
        res =  self.cur.execute(stmt)
        self.cn.commit()
        self.root.destroy()

    def event_cancel(self):
        self.root.destroy()



