# Marathon Manager
#
# Checkpoint Functions
#


import sqlite3
from pathlib import Path
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from tkinter import colorchooser
from datetime import datetime
from constants import *

def checkpoint_filldata(tv:ttk.Treeview) -> None:
    """Clear and then fill/refresh the Checkpoints table with data"""
    # clear the table
    for item in tv.get_children():
        tv.delete(item)

    # get the checkpoints from the database
    cn = sqlite3.connect(DB_NAME)
    cur = cn.cursor()
    cur.execute("select CheckpointID, CPName, Description, Longitude, Latitude from Checkpoints;")
    rows = cur.fetchall()
    for row in rows:
        tv.insert("",tk.END,values=row)

def checkpoint_edit(checkpoint,tv):
    if checkpoint:
        cpid,cname,cdescription,clong,clat = checkpoint
    else:
        cpid,cname,cdescription,clong,clat = '','','','',''

    def cancel():
        croot.destroy()

    def save():
        """Create/insert a new Checkpoint"""
        cn = sqlite3.connect(DB_NAME)
        cur = cn.cursor()

        cpid = txtCPID.get()
        cname=txtName.get()
        cdescription = txtDescr.get()
        clong = txtLong.get()
        clat = txtLat.get()
        cur.execute("insert into Checkpoints (CPName, Description, Longitude, Latitude) values(?,?,?,?);",[cname,cdescription,clong,clat])
        cn.commit()

        checkpoint_filldata(tv)
        croot.destroy()

    def update():
        """Update an existing Checkpoint"""
        cn = sqlite3.connect(DB_NAME)
        cur = cn.cursor()

        cpid = txtCPID.get()
        cname=txtName.get()
        cdescription = txtDescr.get()
        clong = txtLong.get()
        clat = txtLat.get()
        cur.execute("update Checkpoints set CPName=?, Description=?, Longitude=?, Latitude=? where CheckpointID=?",[cname,cdescription,clong,clat,cpid])
        cn.commit()

        checkpoint_filldata(tv)
        croot.destroy()

    croot = tk.Tk()
    croot.title("MM: Edit Checkpoint")
    croot.geometry('250x150')

    lblCPID = ttk.Label(croot,text="Checkpoint ID:")
    lblCPID.grid(row=0,column=0,sticky='e')
    txtCPID = ttk.Entry(croot)
    txtCPID.grid(row=0,column=1,columnspan=2,sticky='w')
    txtCPID.insert(0,cpid)
    txtCPID.config(state="disabled")

    lblName = ttk.Label(croot,text="Name:")
    lblName.grid(row=1,column=0,sticky='e')
    txtName = ttk.Entry(croot)
    txtName.grid(row=1,column=1,columnspan=2,sticky='w')
    txtName.insert(0,cname)

    lblDescr = ttk.Label(croot,text="Description:")
    lblDescr.grid(row=2,column=0,sticky='e')
    txtDescr = ttk.Entry(croot)
    txtDescr.grid(row=2,column=1,columnspan=2,sticky='w')
    txtDescr.insert(0,cdescription)

    lblLong = ttk.Label(croot,text="Longitude:")
    lblLong.grid(row=3,column=0,sticky='e')
    txtLong = ttk.Entry(croot)
    txtLong.grid(row=3,column=1,columnspan=2,sticky='w')
    txtLong.insert(0,clong)

    lblLat = ttk.Label(croot,text="Latitude:")
    lblLat.grid(row=4,column=0,sticky='e')
    txtLat = ttk.Entry(croot)
    txtLat.grid(row=4,column=1,columnspan=2,sticky='w')
    txtLat.insert(0,clat)


    if checkpoint:
        butSave = ttk.Button(croot,text="Update",command=update)
    else:
        butSave = ttk.Button(croot,text="Save",command=save)
    butSave.grid(row=5,column=1,sticky='e')

    butCancel = ttk.Button(croot,text="Cancel",command=cancel)
    butCancel.grid(row=5,column=2,sticky='w')



def checkpoint_window(main_frame:tk.Frame) -> tk.Frame:
    cn,cur = None,None

    cn = sqlite3.connect(DB_NAME)
    cur = cn.cursor()


    def checkpoint_close():
        main_frame.destroy()

    def checkpoint_new():
        checkpoint_edit(None,tvCheckpoints)

    def checkpoint_map():
        print("Map Checkpoint")

    def checkpoint_edit_row(event):
        item = tvCheckpoints.item(tvCheckpoints.focus(),"values")
        checkpoint_edit(item,tvCheckpoints)

    title = ttk.Label(main_frame,text='Checkpoints',font=('Arial',18))
    title.grid(row=0,column=0,columnspan=2,sticky='nw')

    lblLogo = ttk.Label(main_frame,text="Logo Placeholder")
    lblLogo.grid(row=0,column=2,rowspan=2,sticky='news')

    btnNew = ttk.Button(main_frame,text="New Checkpoint",command=checkpoint_new)
    btnNew.grid(row=1,column=0,padx=5,pady=5,sticky='e')

    btnMap = ttk.Button(main_frame,text="Map Checkpoints",command=checkpoint_map)
    btnMap.grid(row=1,column=1,padx=5,pady=5,sticky='w')

    tvCheckpoints = ttk.Treeview(main_frame,column=("c1","c2","c3","c4","c5"),show='headings',selectmode='browse')
    tvCheckpoints.column("#1",anchor='center',minwidth=0,width=0)   # hidden
    tvCheckpoints.heading("#1",text="CP ID")
    tvCheckpoints.column("#2",anchor='w',minwidth=0,width=100)
    tvCheckpoints.heading("#2",text="Checkpoint",anchor='w')
    tvCheckpoints.column("#3",anchor='w',minwidth=0,width=200)
    tvCheckpoints.heading("#3",text="Description",anchor='w')
    tvCheckpoints.column("#4",anchor='w',minwidth=0,width=150)
    tvCheckpoints.heading("#4",text="Longitude",anchor='w')
    tvCheckpoints.column("#5",anchor='w',minwidth=0,width=150)
    tvCheckpoints.heading("#5",text="Latitude",anchor='w')
    tvCheckpoints.grid(row=2,column=0,columnspan=3,padx=5,pady=5)
    tvCheckpoints.bind("<Double-1>",checkpoint_edit_row)

    yscrollbar = ttk.Scrollbar(main_frame,orient='vertical',command=tvCheckpoints.yview)
    yscrollbar.grid(row=2, column=3,pady=15,sticky='nse')
    yscrollbar.configure(command=tvCheckpoints.yview)    
    tvCheckpoints.configure(yscrollcommand=yscrollbar.set)


    checkpoint_filldata(tvCheckpoints)

    btnClose = ttk.Button(main_frame,text="Close",command=checkpoint_close)
    btnClose.grid(row=3,column=2,padx=5,pady=5,sticky='w')
