# =============================================================================
#  Courses Window
# =============================================================================

import sqlite3
from pathlib import Path
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from tkinter import colorchooser
from datetime import datetime
from constants import *

def courses_filldata(tv:ttk.Treeview) -> None:
    """Clear and then fill/refresh the Courses table with data"""
    # clear the table
    for item in tv.get_children():
        tv.delete(item)

    # get the courses from the database
    cn = sqlite3.connect(DB_NAME)
    cur = cn.cursor()
    cur.execute("select CourseID, CourseName, Distance, Color, Path from Courses;")
    rows = cur.fetchall()
    
    # populate the treeview with the data
    for row in rows:
        tv.tag_configure(str(row[0]),background=row[3])
        tv.insert("",tk.END,values=row,tags=str(row[0]))


def course_edit(item,tv):
    if item:
        cid,cname,cdistance,ccolor,cpath = item
    else:
        cid,cname,cdistance,ccolor,cpath = '','','','',''

    def cancel():
        """Cancel any operations in this window and close it"""
        c_root.destroy()
    
    def save():
        """Create a new Course"""
        cn = sqlite3.connect(DB_NAME)
        cur = cn.cursor()

        cname = txtName.get()
        cdistance = txtDistance.get()
        ccolor = txtColor.get()
        cpath = txtPath.get()
        cur.execute("insert into Courses (CourseName, Distance, Color, Path) values (?,?,?,?);",[cname,cdistance,ccolor,cpath])
        cn.commit()

        courses_filldata(tv)
        c_root.destroy()

    def update():
        """Update an existing Course"""
        cn = sqlite3.connect(DB_NAME)
        cur = cn.cursor()

        cname = txtName.get()
        cdistance = txtDistance.get()
        ccolor = txtColor.get()
        cpath = txtPath.get()
        cur.execute("update Courses set CourseName=?, Distance=?, Color=?, Path=? where CourseID=?",[cname,cdistance,ccolor,cpath,cid])
        cn.commit()

        courses_filldata(tv)
        c_root.destroy()

    def choose_color():
        current_color = txtColor.get()
        color_code = colorchooser.askcolor(title="Choose Color",color=current_color)
        txtColor.delete(0,'end')
        txtColor.insert(0,color_code[1])

    c_root = tk.Tk()
    c_root.title("MM: Edit Course")
    c_root.geometry('325x150')
    c_root.resizable(False,False)

    lblCID = ttk.Label(c_root,text="Course ID:")
    lblCID.grid(row=0,column=0,sticky='e')
    txtCID = ttk.Entry(c_root,width=25)
    txtCID.grid(row=0,column=1,columnspan=2,sticky='w')
    txtCID.insert(0,cid)
    txtCID.config(state="disabled")

    lblName = ttk.Label(c_root,text="Name:")
    lblName.grid(row=1,column=0,sticky='e')
    txtName = ttk.Entry(c_root,width=25)
    txtName.grid(row=1,column=1,columnspan=2,sticky='w')
    txtName.insert(0,cname)

    lblDistance = ttk.Label(c_root,text="Distance:")
    lblDistance.grid(row=2,column=0,sticky='e')
    txtDistance = ttk.Entry(c_root,width=25)
    txtDistance.grid(row=2,column=1,columnspan=2,sticky='w')
    txtDistance.insert(0,cdistance)

    lblColor = ttk.Label(c_root,text="Color:")
    lblColor.grid(row=3,column=0,sticky='e')
    txtColor = ttk.Entry(c_root,width=25)
    txtColor.grid(row=3,column=1,columnspan=2,sticky='w')
    txtColor.insert(0,ccolor)
    butColor = ttk.Button(c_root,text="...",width=5,command=choose_color)
    butColor.grid(row=3,column=3,sticky='w')

    lblPath = ttk.Label(c_root,text="Path:")
    lblPath.grid(row=4,column=0,sticky='e')
    txtPath = ttk.Entry(c_root,width=25)
    txtPath.grid(row=4,column=1,columnspan=2,sticky='w')
    txtPath.insert(0,cpath)
    lblPathInstr = ttk.Label(c_root,text="(comma-separated CP names)",font=("Arial",6))
    lblPathInstr.grid(row=4,column=3,sticky='w')


    if item:
        butSave = ttk.Button(c_root,text="Update",command=update)
        butSave.grid(row=5,column=1,sticky='e')
    else:
        butSave = ttk.Button(c_root,text="Save",command=save)
        butSave.grid(row=5,column=1,sticky='e')


    butCancel = ttk.Button(c_root,text="Cancel",command=cancel)
    butCancel.grid(row=5,column=2,sticky='w')


def courses_window(main_frame:tk.Frame) -> tk.Frame:
    cn,cur = None,None

    cn = sqlite3.connect(DB_NAME)
    cur = cn.cursor()


    def courses_close():
        """Close the courses window"""
        main_frame.destroy()

    def courses_new():
        """Create a new course"""
        course_edit(None,tvCourses)

    def courses_edit_row(event):
        item = tvCourses.item(tvCourses.focus(),"values")
        course_edit(item,tvCourses)

    title = ttk.Label(main_frame,text='Courses',font=('Arial',18))
    title.grid(row=0,column=0,sticky='nw')

    lblLogo = ttk.Label(main_frame,text="Logo Placeholder")
    lblLogo.grid(row=0,column=2,rowspan=2,sticky='news')

    btnNew = ttk.Button(main_frame,text="New Course",command=courses_new)
    btnNew.grid(row=1,column=0,padx=5,pady=5,sticky='w')

    tvCourses = ttk.Treeview(main_frame,column=("c1","c2","c3","c4","c5"),show='headings',selectmode='browse')
    tvCourses.column("#1",anchor='w',minwidth=30,width=60,stretch='no')
    tvCourses.heading("#1",text="CourseID")
    tvCourses.column("#2",anchor='w',minwidth=30,width=80,stretch='no')
    tvCourses.heading("#2",text="Course")
    tvCourses.column("#3",anchor='w',minwidth=25,width=75,stretch='no')
    tvCourses.heading("#3",text="Distance")
    tvCourses.column("#4",anchor='w',minwidth=30,width=75,stretch='no')
    tvCourses.heading("#4",text="Color")
    tvCourses.column("#5",anchor='w',minwidth=50,width=400,stretch='no')
    tvCourses.heading("#5",text="Path")
    tvCourses.grid(row=2,column=0,columnspan=3,padx=5,pady=5)
    tvCourses.bind("<Double-1>",courses_edit_row)

    yscrollbar = ttk.Scrollbar(main_frame,orient='vertical',command=tvCourses.yview)
    yscrollbar.grid(row=2, column=3,pady=15,sticky='nse')
    yscrollbar.configure(command=tvCourses.yview)    
    tvCourses.configure(yscrollcommand=yscrollbar.set)

    xscrollbar = ttk.Scrollbar(main_frame,orient='horizontal',command=tvCourses.xview)
    xscrollbar.grid(row=3, column=0,columnspan=3,pady=5,padx=5,sticky='ew')
    xscrollbar.configure(command=tvCourses.xview)    
    tvCourses.configure(xscrollcommand=xscrollbar.set)

    courses_filldata(tvCourses)

    btnClose = ttk.Button(main_frame,text="Close",command=courses_close)
    btnClose.grid(row=4,column=2,padx=5,pady=5,sticky='w')
