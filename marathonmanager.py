# Marathon Manager v4.0
# marathonmanager.py

# This is an attempt to create a cross-platform instance of previous versions of
# the Marathon Manager and MarathonLog.

# Design Doc:       https://docs.google.com/document/d/1VVr96XDRAQdNaRYn9vpivIfoGgfj0RA9UhD9_bLc_cM/edit#heading=h.ik9a8ixasni9
# Requirements Doc: https://docs.google.com/document/d/1BqDi_qj6UHPEp5H2pAipckIPRC01c_GxmwDunDiP-oE/edit#
#
# =============================================================================
# Imports
import sqlite3
from pathlib import Path
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from tkinter import colorchooser
from datetime import datetime
# from PIL import ImageTk, Image

from main import *
from constants import *



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
    # initialize settings
    initialize()

    # Open Main Window
    m = MainWindow()





if __name__ == "__main__":
    main()



