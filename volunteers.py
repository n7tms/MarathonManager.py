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

        self.btnClose = ttk.Button(self.root,text="Close",command=self.volunteer_close)
        self.btnClose.grid(row=6,column=2,padx=5,pady=5,sticky='e')

        self.volunteers_filldata(self.tvVolunteer)


    def volunteers_filldata(self,tv:ttk.Treeview) -> None:
        """Clear and then fill/refresh the Checkpoints table with data"""
        # clear the table
        for item in tv.get_children():
            tv.delete(item)

        # get the checkpoints from the database
        rows = DB.query("select VolunteerID, Lastname || ', ' || Firstname as Name, Callsign, 0 from Volunteers order by Lastname;")
        for row in rows:
            tv.insert("",tk.END,values=list(row.values()))



    def new_volunteer(self):
        self.volunteer_edit(None,self.tvVolunteer)


    def volunteer_edit_row(self,event):
        item = int(self.tvVolunteer.item(self.tvVolunteer.focus(),"values")[0])
        self.volunteer_edit(item,self.tvVolunteer)


    def volunteer_close(self):
        """Cancel everything and close this window"""
        self.master.destroy()

    def volunteers_import(self):
        pass

    
    def volunteer_edit(self,vid=None,tv=None):
        pass
        textable_var = tk.StringVar()
        gender_var = tk.StringVar()

        if vid:
            row = DB.query("select Firstname, Lastname, Gender, Birthdate, Phone, Textable, Email, Street1, Street2, City, State, Zipcode, EContactName, EContactPhone, Callsign, Username, Password, Permission from Volunteers where VolunteerID=?",[vid])
            fname,lname,gender,bday,phone,textable,email,street1,street2,city,state,zipcode,ename,ephone,callsign,username,password,permission = list(row[0].values())
        else:
            fname,lname,gender,bday,phone,textable,email,street1,street2,city,state,zipcode,ename,ephone,callsign,username,password,permission = list([''] * 18)
            textable = 0
            vid = 0

        def cancel():
            vroot.destroy()

        def save():
            """Create/insert a new participant"""

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
            callsign = txtCallsign.get()
            username = txtUsername.get()
            password = txtPassword.get()
            permission = txtPermission.get()

            DB.nonQuery("""insert into Volunteers (Firstname, Lastname, Gender, Birthdate, Phone, 
            Textable, Email, Street1, Street2, City, State, Zipcode, EContactName, EContactPhone, 
            Callsign, Username, Password, Permission) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);""",[fname,lname,gender,bday,phone,textable,email,street1,street2,city,state,zipcode,ename,ephone,callsign,username,password,permission])

            self.volunteers_filldata(tv)
            vroot.destroy()

        def update():
            """Update an existing Participant"""

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
            callsign = txtCallsign.get()
            username = txtUsername.get()
            password = txtPassword.get()
            permission = txtPermission.get()


            DB.nonQuery("""update Volunteers set Firstname=?, Lastname=?, Gender=?, Birthdate=?, 
            Phone=?, Textable=?, Email=?, Street1=?, Street2=?, City=?, State=?, Zipcode=?, 
            EContactName=?, EContactPhone=?, Callsign=?, Username=?, Password=?, Permission=? where VolunteerID=?""",
            [fname,lname,gender,bday,phone,textable,email,street1,street2,city,state,zipcode,ename,ephone,callsign,username,password,permission,vid])

            self.volunteers_filldata(tv)
            vroot.destroy()

        vroot = tk.Tk()
        vroot.title("MM: Edit Volunteer")
        vroot.geometry('750x600')

        lblVID = ttk.Label(vroot,text="Volunteer ID:")
        lblVID.grid(row=0,column=0,sticky='e')
        txtVID = ttk.Entry(vroot)
        txtVID.grid(row=0,column=1,columnspan=2,sticky='w')
        if vid:
            txtVID.insert(0,vid)
        txtVID.config(state="disabled")

        lblFName = ttk.Label(vroot,text="Firstname:")
        lblFName.grid(row=1,column=0,sticky='e')
        txtFName = ttk.Entry(vroot)
        txtFName.grid(row=1,column=1,columnspan=2,sticky='w')
        txtFName.insert(0,fname)

        lblLName = ttk.Label(vroot,text="Lastname:")
        lblLName.grid(row=1,column=3,sticky='e')
        txtLName = ttk.Entry(vroot)
        txtLName.grid(row=1,column=4,columnspan=2,sticky='w')
        txtLName.insert(0,lname)

        def gender_selected():
            tk.messagebox.showinfo(title="Gender",message=gender_var.get())
        
        gender_f = tk.Radiobutton(vroot, text='Female',variable=gender_var, value='F')
        gender_m = tk.Radiobutton(vroot, text='Male',variable=gender_var, value='M')
        gender_o = tk.Radiobutton(vroot, text='Other',variable=gender_var, value='O')
        gender_f.grid(row=2,column=0,sticky='w')
        gender_m.grid(row=2,column=1,sticky='w')
        gender_o.grid(row=2,column=2,sticky='w')
        # gender_var.set(gender)
        gender_f.invoke()

        lblBday = ttk.Label(vroot,text="Birthdate:")
        lblBday.grid(row=3,column=0,sticky='e')
        txtBday = ttk.Entry(vroot)
        txtBday.grid(row=3,column=1,columnspan=2,sticky='w')
        if bday:
            txtBday.insert(0,bday)

        lblPhone = ttk.Label(vroot,text="Phone:")
        lblPhone.grid(row=4,column=0,sticky='e')
        txtPhone = ttk.Entry(vroot)
        txtPhone.grid(row=4,column=1,columnspan=2,sticky='w')
        if phone:
            txtPhone.insert(0,phone)

        chkTextable = tk.Checkbutton(vroot,text="Texable",variable=textable_var,onvalue="1",offvalue="0")
        chkTextable.grid(row=4,column=3,sticky='w')
        if textable:
            textable_var.set(str(textable))
        else:
            textable_var.set("0")

        lblEmail = ttk.Label(vroot,text="Email:")
        lblEmail.grid(row=5,column=0,sticky='e')
        txtEmail = ttk.Entry(vroot)
        txtEmail.grid(row=5,column=1,columnspan=2,sticky='w')
        if email:
            txtEmail.insert(0,email)

        lblStreet1 = ttk.Label(vroot,text="Street:")
        lblStreet1.grid(row=6,column=0,sticky='e')
        txtStreet1 = ttk.Entry(vroot)
        txtStreet1.grid(row=6,column=1,columnspan=2,sticky='w')
        if street1:
            txtStreet1.insert(0,street1)

        lblStreet2 = ttk.Label(vroot,text="Street:")
        lblStreet2.grid(row=7,column=0,sticky='e')
        txtStreet2 = ttk.Entry(vroot)
        txtStreet2.grid(row=7,column=1,columnspan=2,sticky='w')
        if street2:
            txtStreet2.insert(0,street2)

        lblCity = ttk.Label(vroot,text="City/State/Zip:")
        lblCity.grid(row=8,column=0,sticky='e')
        txtCity = ttk.Entry(vroot)
        txtCity.grid(row=8,column=1,columnspan=1,sticky='w')
        if city:
            txtCity.insert(0,city)

        txtState = ttk.Entry(vroot)
        txtState.grid(row=8,column=2,columnspan=1,sticky='w')
        if state:
            txtState.insert(0,state)

        txtZip = ttk.Entry(vroot)
        txtZip.grid(row=8,column=3,columnspan=1,sticky='w')
        if zipcode:
            txtZip.insert(0,zipcode)

        lblEname = ttk.Label(vroot,text="Emergency Contact Name/Phone:")
        lblEname.grid(row=9,column=0,sticky='e')
        txtEname = ttk.Entry(vroot)
        txtEname.grid(row=9,column=1,columnspan=2,sticky='w')
        if ename:
            txtEname.insert(0,ename)

        txtEphone = ttk.Entry(vroot)
        txtEphone.grid(row=9,column=3,columnspan=2,sticky='w')
        if ephone:
            txtEphone.insert(0,ephone)

        lblCallsign = ttk.Label(vroot,text="Callsign:")
        lblCallsign.grid(row=11,column=0,sticky='e')
        txtCallsign = ttk.Entry(vroot)
        txtCallsign.grid(row=11,column=1,columnspan=2,sticky='w')
        if callsign:
            txtCallsign.insert(0,callsign)

        lblUsername = ttk.Label(vroot,text="Username:")
        lblUsername.grid(row=10,column=0,sticky='e')
        txtUsername = ttk.Entry(vroot)
        txtUsername.grid(row=10,column=1,columnspan=2,sticky='w')
        if username:
            txtUsername.insert(0,username)

        lblPassword = ttk.Label(vroot,text="Password:")
        lblPassword.grid(row=10,column=0,sticky='e')
        txtPassword = ttk.Entry(vroot)
        txtPassword.grid(row=10,column=1,columnspan=2,sticky='w')
        if vid:
            txtPassword.insert(0,password)

        lblPermission = ttk.Label(vroot,text="Permissions:")
        lblPermission.grid(row=10,column=0,sticky='e')
        txtPermission = ttk.Entry(vroot)
        txtPermission.grid(row=10,column=1,columnspan=2,sticky='w')
        if vid:
            txtPermission.insert(0,permission)


        if vid:
            butSave = ttk.Button(vroot,text="Update",command=update)
        else:
            butSave = ttk.Button(vroot,text="Save",command=save)
        butSave.grid(row=12,column=1,sticky='e')

        butCancel = ttk.Button(vroot,text="Cancel",command=cancel)
        butCancel.grid(row=12,column=2,sticky='w')



