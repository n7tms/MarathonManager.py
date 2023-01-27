# Marathon Manager
#
# Participant Functions
#


import sqlite3
from pathlib import Path
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from tkinter import colorchooser
from datetime import datetime
from constants import *

def participants_filldata(tv:ttk.Treeview) -> None:
    """Clear and then fill/refresh the Checkpoints table with data"""
    # clear the table
    for item in tv.get_children():
        tv.delete(item)

    # get the checkpoints from the database
    cn = sqlite3.connect(DB_NAME)
    cur = cn.cursor()

    # This SQL statement retrieves all of the participants regardless if a courseid has been assigned.
    cur.execute("select ParticipantID, Lastname || ', ' || Firstname as Name, c.CourseID, CourseName, Bib from Participants as p LEFT JOIN Courses as c ON p.CourseID=c.CourseID;")
    rows = cur.fetchall()
    for row in rows:
        tv.insert("",tk.END,values=row)


def participant_edit(pid=None,tv=None):
    cn = sqlite3.connect(DB_NAME)
    cur = cn.cursor()
    textable_var = tk.StringVar()
    gender_var = tk.StringVar()

    if pid:
        cur.execute("select Firstname, Lastname, Gender, Birthdate, Phone, Textable, Email, Street1, Street2, City, State, Zipcode, EContactName, EContactPhone, CourseID, Bib from Participants where ParticipantID=?",[pid])
        row = cur.fetchone()
        fname,lname,gender,bday,phone,textable,email,street1,street2,city,state,zipcode,ename,ephone,cid,bib = list(row)
    else:
        fname,lname,gender,bday,phone,textable,email,street1,street2,city,state,zipcode,ename,ephone,cid,bib = list([''] * 16)
        textable = 0
        cid = 0
        bib = 0

    
    def cancel():
        croot.destroy()

    def save():
        """Create/insert a new participant"""
        cn = sqlite3.connect(DB_NAME)
        cur = cn.cursor()

        fname = txtFName.get()
        lname = txtLName.get()
        gender = gender_var.get()
        bday = txtBday.get()
        phone = txtPhone.get()
        textable = int(textable_var.get())
        email = txtEmail.get()
        street1 = txtStreet1.get()
        street2 = txtStreet2.get()
        city = txtCity.get()
        state = txtState.get()
        zipcode = txtZip.get()
        ename = txtEname.get()
        ephone = txtEphone.get()
        cid = txtCID.get()
        bib = txtBib.get()

        cur.execute("""insert into Participants (Firstname, Lastname, Gender, Birthdate, Phone, 
        Textable, Email, Street1, Street2, City, State, Zipcode, EContactName, EContactPhone, 
        CourseID, Bib) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);""",[fname,lname,gender,bday,phone,textable,email,street1,street2,city,state,zipcode,ename,ephone,cid,bib])
        cn.commit()

        participants_filldata(tv)
        croot.destroy()

    def update():
        """Update an existing Checkpoint"""
        cn = sqlite3.connect(DB_NAME)
        cur = cn.cursor()

        fname = txtFName.get()
        lname = txtLName.get()
        gender = gender_var.get()
        bday = txtBday.get()
        phone = txtPhone.get()
        textable = int(textable_var.get())
        email = txtEmail.get()
        street1 = txtStreet1.get()
        street2 = txtStreet2.get()
        city = txtCity.get()
        state = txtState.get()
        zipcode = txtZip.get()
        ename = txtEname.get()
        ephone = txtEphone.get()
        cid = txtCID.get()
        bib = txtBib.get()

        cur.execute("""update Participants set Firstname=?, Lastname=?, Gender=?, Birthdate=?, 
        Phone=?, Textable=?, Email=?, Street1=?, Street2=?, City=?, State=?, Zipcode=?, 
        EContactName=?, EContactPhone=?, CourseID=?, Bib=? where ParticipantID=?""",
        [fname,lname,gender,bday,phone,textable,email,street1,street2,city,state,zipcode,ename,ephone,cid,bib,pid])
        cn.commit()

        participants_filldata(tv)
        croot.destroy()

    croot = tk.Tk()
    croot.title("MM: Edit Checkpoint")
    croot.geometry('750x550')

    lblPID = ttk.Label(croot,text="Participant ID:")
    lblPID.grid(row=0,column=0,sticky='e')
    txtPID = ttk.Entry(croot)
    txtPID.grid(row=0,column=1,columnspan=2,sticky='w')
    if pid:
        txtPID.insert(0,pid)
    txtPID.config(state="disabled")

    lblFName = ttk.Label(croot,text="Firstname:")
    lblFName.grid(row=1,column=0,sticky='e')
    txtFName = ttk.Entry(croot)
    txtFName.grid(row=1,column=1,columnspan=2,sticky='w')
    txtFName.insert(0,fname)

    lblLName = ttk.Label(croot,text="Lastname:")
    lblLName.grid(row=1,column=3,sticky='e')
    txtLName = ttk.Entry(croot)
    txtLName.grid(row=1,column=4,columnspan=2,sticky='w')
    txtLName.insert(0,lname)

    def gender_selected():
        tk.messagebox.showinfo(title="Gender",message=gender_var.get())
    
    gender_f = tk.Radiobutton(croot, text='Female',variable=gender_var, value='F')
    gender_m = tk.Radiobutton(croot, text='Male',variable=gender_var, value='M')
    gender_o = tk.Radiobutton(croot, text='Other',variable=gender_var, value='O')
    gender_f.grid(row=2,column=0,sticky='w')
    gender_m.grid(row=2,column=1,sticky='w')
    gender_o.grid(row=2,column=2,sticky='w')
    # gender_var.set(gender)
    gender_f.invoke()

    lblBday = ttk.Label(croot,text="Birthdate:")
    lblBday.grid(row=3,column=0,sticky='e')
    txtBday = ttk.Entry(croot)
    txtBday.grid(row=3,column=1,columnspan=2,sticky='w')
    if bday:
        txtBday.insert(0,bday)

    lblPhone = ttk.Label(croot,text="Phone:")
    lblPhone.grid(row=4,column=0,sticky='e')
    txtPhone = ttk.Entry(croot)
    txtPhone.grid(row=4,column=1,columnspan=2,sticky='w')
    if phone:
        txtPhone.insert(0,phone)

    chkTextable = tk.Checkbutton(croot,text="Texable",variable=textable_var,onvalue="1",offvalue="0")
    chkTextable.grid(row=4,column=3,sticky='w')
    if textable:
        textable_var.set(str(textable))
    else:
        textable_var.set("0")

    lblEmail = ttk.Label(croot,text="Email:")
    lblEmail.grid(row=5,column=0,sticky='e')
    txtEmail = ttk.Entry(croot)
    txtEmail.grid(row=5,column=1,columnspan=2,sticky='w')
    if email:
        txtEmail.insert(0,email)

    lblStreet1 = ttk.Label(croot,text="Street:")
    lblStreet1.grid(row=6,column=0,sticky='e')
    txtStreet1 = ttk.Entry(croot)
    txtStreet1.grid(row=6,column=1,columnspan=2,sticky='w')
    if street1:
        txtStreet1.insert(0,street1)

    lblStreet2 = ttk.Label(croot,text="Street:")
    lblStreet2.grid(row=7,column=0,sticky='e')
    txtStreet2 = ttk.Entry(croot)
    txtStreet2.grid(row=7,column=1,columnspan=2,sticky='w')
    if street2:
        txtStreet2.insert(0,street2)

    lblCity = ttk.Label(croot,text="City/State/Zip:")
    lblCity.grid(row=8,column=0,sticky='e')
    txtCity = ttk.Entry(croot)
    txtCity.grid(row=8,column=1,columnspan=1,sticky='w')
    if city:
        txtCity.insert(0,city)

    txtState = ttk.Entry(croot)
    txtState.grid(row=8,column=2,columnspan=1,sticky='w')
    if state:
        txtState.insert(0,state)

    txtZip = ttk.Entry(croot)
    txtZip.grid(row=8,column=3,columnspan=1,sticky='w')
    if zipcode:
        txtZip.insert(0,zipcode)

    lblEname = ttk.Label(croot,text="Emergency Contact Name/Phone:")
    lblEname.grid(row=9,column=0,sticky='e')
    txtEname = ttk.Entry(croot)
    txtEname.grid(row=9,column=1,columnspan=2,sticky='w')
    if ename:
        txtEname.insert(0,ename)

    txtEphone = ttk.Entry(croot)
    txtEphone.grid(row=9,column=3,columnspan=2,sticky='w')
    if ephone:
        txtEphone.insert(0,ephone)

    lblCID = ttk.Label(croot,text="Course ID:")
    lblCID.grid(row=10,column=0,sticky='e')
    txtCID = ttk.Entry(croot)
    txtCID.grid(row=10,column=1,columnspan=2,sticky='w')
    if cid:
        txtCID.insert(0,cid)

    lblBib = ttk.Label(croot,text="Bib #:")
    lblBib.grid(row=11,column=0,sticky='e')
    txtBib = ttk.Entry(croot)
    txtBib.grid(row=11,column=1,columnspan=2,sticky='w')
    if bib:
        txtBib.insert(0,bib)


    if pid:
        butSave = ttk.Button(croot,text="Update",command=update)
    else:
        butSave = ttk.Button(croot,text="Save",command=save)
    butSave.grid(row=12,column=1,sticky='e')

    butCancel = ttk.Button(croot,text="Cancel",command=cancel)
    butCancel.grid(row=12,column=2,sticky='w')





def participant_window(main_frame:tk.Frame) -> tk.Frame:
    cn,cur = None,None

    cn = sqlite3.connect(DB_NAME)
    cur = cn.cursor()


    def participants_close():
        main_frame.destroy()

    def participant_new():
        participant_edit(None,tvParticipants)


    def participant_edit_row(event):
        item = int(tvParticipants.item(tvParticipants.focus(),"values")[0])
        participant_edit(item,tvParticipants)

    title = ttk.Label(main_frame,text='Participants',font=('Arial',18))
    title.grid(row=0,column=0,columnspan=2,sticky='nw')

    lblLogo = ttk.Label(main_frame,text="Logo Placeholder")
    lblLogo.grid(row=0,column=2,rowspan=2,sticky='news')

    btnNew = ttk.Button(main_frame,text="New Participant",command=participant_new)
    btnNew.grid(row=1,column=0,padx=5,pady=5,sticky='w')

    tvParticipants = ttk.Treeview(main_frame,column=("c1","c2","c3","c4","c5"),show='headings',selectmode='browse')
    tvParticipants.column("#1",anchor='center',minwidth=0,width=0)  # hidden
    tvParticipants.heading("#1",text="PID")
    tvParticipants.column("#2",anchor='w',minwidth=0,width=200)
    tvParticipants.heading("#2",text="Name",anchor='w')
    tvParticipants.column("#3",anchor='w',minwidth=0,width=0)       # hidden
    tvParticipants.heading("#3",text="CID",anchor='w')
    tvParticipants.column("#4",anchor='w',minwidth=0,width=100)
    tvParticipants.heading("#4",text="Course",anchor='w')
    tvParticipants.column("#5",anchor='w',minwidth=0,width=75)
    tvParticipants.heading("#5",text="Bib",anchor='w')
    tvParticipants.grid(row=2,column=0,columnspan=3,padx=5,pady=5)
    tvParticipants.bind("<Double-1>",participant_edit_row)

    yscrollbar = ttk.Scrollbar(main_frame,orient='vertical',command=tvParticipants.yview)
    yscrollbar.grid(row=2, column=3,pady=15,sticky='nse')
    yscrollbar.configure(command=tvParticipants.yview)    
    tvParticipants.configure(yscrollcommand=yscrollbar.set)

    participants_filldata(tvParticipants)

    btnClose = ttk.Button(main_frame,text="Close",command=participants_close)
    btnClose.grid(row=3,column=2,padx=5,pady=5,sticky='w')


