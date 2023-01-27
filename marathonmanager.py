# Marathon Manager v4.0
# marathonmanager.py

# This is an attempt to create a cross-platform instance of previous versions of
# the Marathon Manager and MarathonLog.

# Design Doc:       https://docs.google.com/document/d/1VVr96XDRAQdNaRYn9vpivIfoGgfj0RA9UhD9_bLc_cM/edit#heading=h.ik9a8ixasni9
# Requirements Doc: https://docs.google.com/document/d/1BqDi_qj6UHPEp5H2pAipckIPRC01c_GxmwDunDiP-oE/edit#
#
# =============================================================================
# Imports
import random
import sqlite3
from pathlib import Path
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from tkinter import colorchooser
import re
from datetime import datetime
# from PIL import ImageTk, Image

from checkpoints import *
from constants import *
from courses import *
from database import *
from events import *
from sitings import *



# =============================================================================
# GUI Definitions
#
def quick_links(main_frame: tk.Frame) -> tk.Frame:
    qlf = tk.Frame(main_frame,highlightbackground="blue",highlightthickness=1)

    lblMcc1 = ttk.Label(qlf,text='Marathon')
    lblMcc2 = ttk.Label(qlf,text='Control')
    lblMcc3 = ttk.Label(qlf,text='Center')
    butEvent = ttk.Button(qlf,text="Event")
    butSitings = ttk.Button(qlf,text='Sitings')
    butMessages = ttk.Button(qlf,text='Messages')
    butVolunteers = ttk.Button(qlf,text='Volunteers')
    butReports = ttk.Button(qlf,text='Reports')
    # mmLogo
    
    lblMcc1.grid(row=0,column=0,sticky='W', padx=5, pady=8)

    return qlf



# =============================================================================
#  Report/Status Panel
# =============================================================================

def reports_status(main_frame: tk.Frame) -> tk.Frame:
    rsf = tk.Frame(main_frame,highlightbackground="blue",highlightthickness=1)
    rsf.highlightbackground="blue"
    rsf.highlightthickness=1

    lblTitle = ttk.Label(rsf,text='Reports/Status')

    lblTitle.grid(row=0,column=0,sticky='w', padx=5, pady=8)

    return rsf





# =============================================================================
#  Log Panel
# =============================================================================

def logs(main_frame: tk.Frame) -> tk.Frame:
    lf = tk.Frame(main_frame,highlightbackground="blue",highlightthickness=1)

    lblTitle = ttk.Label(lf,text='Log')

    lblTitle.grid(row=0,column=0,sticky='W', padx=5, pady=8)

    return lf





# =============================================================================
#  Volunteer Window
# =============================================================================

def volunteers(main_frame: tk.Frame) -> tk.Frame:
    vf = tk.Frame(main_frame,highlightbackground="blue",highlightthickness=1)

    lblTitle = ttk.Label(vf,text='Volunteers')

    lblTitle.grid(row=0,column=0,sticky='W', padx=5, pady=8)

    return vf





# =============================================================================
#  Messages Panel
# =============================================================================

def messages(main_frame: tk.Frame) -> tk.Frame:
    mf = tk.Frame(main_frame,highlightbackground="blue",highlightthickness=1)

    lblTitle = ttk.Label(mf,text='Messages')

    lblTitle.grid(row=0,column=0,sticky='W', padx=5, pady=8)

    return mf   




# =============================================================================
#  Main Menu Bar
# =============================================================================

def mainmenubar(main_frame: tk.Frame) -> tk.Frame:
    mmb = tk.Menu(main_frame)

    def donothing():
        pass

    def new_database():
        pass

    
    def event_click():
        e_root = tk.Tk()
        e_root.title("MM: Event")
        e_root.geometry('350x150')
        ew = event_window(e_root)

    def checkpoints_click():
        root = tk.Tk()
        root.title("MM: Checkpoints")
        root.geometry('700x340')
        ew = checkpoint_window(root)

    def courses_click():
        root = tk.Tk()
        root.title("MM: Courses")
        root.geometry('735x380')
        ew = courses_window(root)


    filemenu = tk.Menu(mmb, tearoff=0)
    filemenu.add_command(label="New", command=donothing)
    filemenu.add_separator()
    filemenu.add_command(label="Open", command=donothing)
    filemenu.add_command(label="Close", command=donothing)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=main_frame.quit)
    mmb.add_cascade(label="File", menu=filemenu) 

    eventmenu = tk.Menu(mmb, tearoff=0)
    eventmenu.add_command(label="Edit Event", command=event_click)
    eventmenu.add_separator()
    eventmenu.add_command(label="Checkpoints", command=checkpoints_click)
    eventmenu.add_command(label="Courses", command=courses_click)
    eventmenu.add_separator()
    eventmenu.add_command(label="Participants", command=donothing)
    mmb.add_cascade(label="Event", menu=eventmenu)

    helpmenu = tk.Menu(mmb, tearoff=0)
    helpmenu.add_command(label="Help Index", command=donothing)
    helpmenu.add_command(label="About...", command=donothing)
    mmb.add_cascade(label="Help", menu=helpmenu)

    return mmb
        





def initialize():
    global CONN 
    global CUR
    
    # open the database
    # # TODO: this needs to be modified to check for valid fields (a db version?)
    # if not database_exists(DB_NAME_SETTINGS):
    #     CONN = sqlite3.connect(DB_NAME_SETTINGS)
    #     CUR = CONN.cursor()
    #     create_settings_database()
    #     CONN.close()

    if not database_exists(DB_NAME):
        CONN = sqlite3.connect(DB_NAME)
        CUR = CONN.cursor()
        create_database()
        CONN.close()

    CONN = sqlite3.connect(DB_NAME)
    CUR = CONN.cursor()

    res = CUR.execute("""SELECT SettingValue from Settings WHERE SettingName = 'DBVersion'""")
    # reslst = list(res)
    db_version = int(list(res)[0][0])
    # db_version = 1
    if db_version < 1:
        print("Database is an older (incompatible) version. Update.")
        exit()
    # print("Using DB Version",db_version)



# =============================================================================
# Main
# 
def main():

    initialize()

    root = tk.Tk()
    main_frame = ttk.Frame(root)
    main_frame.pack(fill='both',expand=True)

    # Main Menu bar
    menubar = mainmenubar(main_frame)
    root.config(menu=menubar)

    def open_sitings():
        sitings = tk.Tk()
        sitings.title("MM: Sitings")
        sitings.geometry('600x320')
        sw = siting_window(sitings)
        # sitings.grid(row=0,column=1,sticky='n')

    def open_reports():
        root = tk.Tk()
        root.title("MM: Checkpoints")
        root.geometry('825x340')
        ew = checkpoint_window(root)

    def open_log():
        pass

    def open_volunteers():
        pass

    def open_messages():
        pass
    

    btnSitings = ttk.Button(main_frame,text="Sitings",command=open_sitings)
    btnSitings.grid(row=1,column=0,padx=10,pady=10,sticky='news')

    
    # # Reports/Status
    # reports = guis.reports_status(main_frame)
    # # reports.pack(side='left')
    # reports.grid(row=1,column=1)
    
    # # Log
    # logs = guis.logs(main_frame)
    # # logs.pack(side='left', fill='x')
    # logs.grid(row=0,column=2,sticky='n',rowspan=2)
    
    # # Volunteers
    # volunteers = guis.volunteers(main_frame)
    # # volunteers.pack(side='right', fill='x')
    # volunteers.grid(row=0,column=3,sticky='ne',rowspan=2)
    
    # # Messages
    # messages = guis.messages(main_frame)
    # # messages.pack(side='bottom',fill='y')
    # messages.grid(row=2,column=1,sticky='s')

    root.title("Marathon Manager")
    root.geometry('450x200')
    root.minsize(400,100)
    root.mainloop()





if __name__ == "__main__":
    initialize()

    main()



