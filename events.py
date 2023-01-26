import random
import sqlite3
from pathlib import Path
# from tkinter import Tk
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from tkinter import colorchooser
import re
from datetime import datetime
from constants import *

# =============================================================================
#  Event Window
# =============================================================================

def event_window(main_frame: tk.Frame) -> tk.Frame:
    cn,cur = None,None

    cn = sqlite3.connect(DB_NAME)
    cur = cn.cursor()

    def event_save():
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
        main_frame.destroy()

    def event_cancel():
        main_frame.destroy()

    # img2 = ImageTk.PhotoImage(file='runner_blue.png')
    # imgLogo = ttk.Label(main_frame,image=img2)
    imgLogo = ttk.Label(main_frame,text="logo placeholder")
    imgLogo.grid(row=0,column=0,rowspan=5)

    lblEventName = ttk.Label(main_frame,text='Event Name:',width=12)
    lblEventName.grid(row=0,column=1,sticky='e', padx=5, pady=8)
    txtEventName = ttk.Entry(main_frame,width=25)
    txtEventName.grid(row=0,column=2, columnspan=2,sticky='w')
    
    lblDescription = ttk.Label(main_frame,text='Description:',width=12)
    lblDescription.grid(row=1,column=1,sticky='e',padx=5, pady=8)
    txtDescription = tk.Entry(main_frame,width=25)
    txtDescription.grid(row=1,column=2, columnspan=2,sticky='w',padx=5, pady=8)

    lblLocation = ttk.Label(main_frame,text='Location:',width=12)
    lblLocation.grid(row=2,column=1,sticky='e')
    txtLocation = tk.Entry(main_frame,width=10)
    txtLocation.grid(row=2,column=2,sticky='w')

    lblStartDate = ttk.Label(main_frame,text='Start Date:',width=12)
    lblStartDate.grid(row=3,column=1,sticky='e')
    txtStartDate = tk.Entry(main_frame,width=10)
    txtStartDate.grid(row=3,column=2,sticky='w')

    lblStartTime = ttk.Label(main_frame,text='Start Time:',width=12)
    lblStartTime.grid(row=4,column=1,sticky='e')
    txtStartTime = tk.Entry(main_frame,width=10)
    txtStartTime.grid(row=4,column=2,sticky='w')

    butSave = ttk.Button(main_frame,text='Save',command=event_save)
    butSave.grid(row=3,column=3)
    butCancel = ttk.Button(main_frame,text='Cancel',command=event_cancel)
    butCancel.grid(row=4,column=3)
    
    return main_frame
