# Marathon Manager - Participants Window

import sqlite3
from tkinter import ttk
import tkinter as tk
from constants import *
from participant_import import *
from functools import partial

class ParticipantsWindow:
    
    def __init__(self,master):

        self.master = master

        self.root = tk.Frame(master)
        self.root.pack()

        master.title("MM: Participants")
        master.geometry('800x600')
        master.minsize(400,100)


        self.title = ttk.Label(self.root,text='Participants',font=('Arial',18))
        self.title.grid(row=0,column=0,columnspan=2,sticky='nw')

        self.lblLogo = ttk.Label(self.root,text="Logo Placeholder")
        self.lblLogo.grid(row=0,column=2,rowspan=2,sticky='news')

        self.btnNew = ttk.Button(self.root,text="New Participant",command=self.participant_new)
        self.btnNew.grid(row=1,column=0,padx=5,pady=5,sticky='w')

        self.btnImport = ttk.Button(self.root,text="Import Participants",command=self.participant_import)
        self.btnImport.grid(row=1,column=1,padx=5,pady=5,sticky='w')

        self.tvParticipants = ttk.Treeview(self.root,column=("c1","c2","c3","c4","c5"),show='headings',selectmode='browse')
        self.tvParticipants.column("#1",anchor='center',minwidth=0,width=0)  # hidden
        self.tvParticipants.heading("#1",text="PID")
        self.tvParticipants.column("#2",anchor='w',minwidth=0,width=200)
        self.tvParticipants.heading("#2",text="Name",anchor='w')
        self.tvParticipants.column("#3",anchor='w',minwidth=0,width=0)       # hidden
        self.tvParticipants.heading("#3",text="CID",anchor='w')
        self.tvParticipants.column("#4",anchor='w',minwidth=0,width=100)
        self.tvParticipants.heading("#4",text="Course",anchor='w')
        self.tvParticipants.column("#5",anchor='w',minwidth=0,width=75)
        self.tvParticipants.heading("#5",text="Bib",anchor='w')
        self.tvParticipants.grid(row=2,column=0,columnspan=3,padx=5,pady=5)
        self.tvParticipants.bind("<Double-1>",self.participant_edit_row)
        self.tvParticipants.bind("<Button-3>",self.showContextMenu)

        self.yscrollbar = ttk.Scrollbar(self.root,orient='vertical',command=self.tvParticipants.yview)
        self.yscrollbar.grid(row=2, column=3,pady=15,sticky='nse')
        self.yscrollbar.configure(command=self.tvParticipants.yview)    
        self.tvParticipants.configure(yscrollcommand=self.yscrollbar.set)

        self.participants_filldata(self.tvParticipants)

        self.btnClose = ttk.Button(self.root,text="Close",command=self.participants_close)
        self.btnClose.grid(row=3,column=2,padx=5,pady=5,sticky='w')

        self.part_gender = ""
        self.part_textable = 0

    def participants_close(self):
        self.master.destroy()


    def participant_new(self):
        self.participant_edit(None,self.tvParticipants)


    def participant_edit_row(self,event):
        item = int(self.tvParticipants.item(self.tvParticipants.focus(),"values")[0])
        self.participant_edit(item,self.tvParticipants)


    def showContextMenu(self,event):
        iid = self.tvParticipants.identify('item',event.x,event.y)

        def p_e_r():
            item = int(self.tvParticipants.item(self.tvParticipants.focus(),"values")[0])
            self.participant_edit(item,self.tvParticipants)

        def participant_delete():
            print("Participant delete not yet implemented.")
        

        if iid:
            self.tvParticipants.selection_set(iid)
            self.tvParticipants.focus_set()
            self.tvParticipants.focus(iid)

            # Treeview right-click popup menu definition
            context_menu = tk.Menu(self.master,tearoff=0)
            context_menu.add_command(label="Edit",command=p_e_r)
            context_menu.add_separator()
            context_menu.add_command(label="Delete",command=participant_delete)
            context_menu.post(event.x_root,event.y_root)
        else:
            pass


    def participant_import(self):
        adds,colisions = 0,0
        # part_imp = tk.Tk()
        # part_imp.title("MM: Participants Import")
        # part_imp.geometry('1000x600')
        # paim = self.import_window(part_imp)
        pi_root = tk.Toplevel()
        paim = ImportParticipantsWindow(pi_root)


    def participants_filldata(self,tv:ttk.Treeview) -> None:
        """Clear and then fill/refresh the Checkpoints table with data"""
        # clear the table
        for item in tv.get_children():
            tv.delete(item)

        # get the checkpoints from the database

        # This SQL statement retrieves all of the participants regardless if a courseid has been assigned.
        rows = DB.query("select ParticipantID, Lastname || ', ' || Firstname as Name, c.CourseID, CourseName, Bib from Participants as p LEFT JOIN Courses as c ON p.CourseID=c.CourseID;")
        for row in rows:
            tv.insert("",tk.END,values=[row['ParticipantID'],row['Name'],row['CourseID'],row['CourseName'],row['Bib']])


    def participant_edit(self,pid=None,tv=None):
        self.textable_var = tk.IntVar()
        self.gender_var = tk.StringVar()

        if pid:
            row = DB.query("select Firstname, Lastname, Gender, Birthdate, Phone, Textable, Email, Street1, Street2, City, State, Zipcode, EContactName, EContactPhone, CourseID, Bib from Participants where ParticipantID=?",[pid])
            fname,lname,gender,bday,phone,textable,email,street1,street2,city,state,zipcode,ename,ephone,cid,bib = row[0].values()
            # print(fname)
        else:
            fname,lname,gender,bday,phone,textable,email,street1,street2,city,state,zipcode,ename,ephone,cid,bib = list([''] * 16)
            textable = 0
            cid = 0
            bib = 0

        
        def cancel():
            croot.destroy()

        def save():
            """Create/insert a new participant"""

            fname = txtFName.get()
            lname = txtLName.get()
            gender = self.part_gender
            bday = txtBday.get()
            phone = txtPhone.get()
            if 'selected' in chkTextable.state():
                textable = 1
            else:
                textable = 0
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

            DB.nonQuery("""insert into Participants (Firstname, Lastname, Gender, Birthdate, Phone, 
            Textable, Email, Street1, Street2, City, State, Zipcode, EContactName, EContactPhone, 
            CourseID, Bib) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);""",[fname,lname,gender,bday,phone,textable,email,street1,street2,city,state,zipcode,ename,ephone,cid,bib])

            self.participants_filldata(tv)
            croot.destroy()

        def update():
            """Update an existing Participant"""

            fname = txtFName.get()
            lname = txtLName.get()
            gender = self.part_gender
            bday = txtBday.get()
            phone = txtPhone.get()
            if 'selected' in chkTextable.state():
                textable = 1
            else:
                textable = 0
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

            DB.nonQuery("""update Participants set Firstname=?, Lastname=?, Gender=?, Birthdate=?, 
            Phone=?, Textable=?, Email=?, Street1=?, Street2=?, City=?, State=?, Zipcode=?, 
            EContactName=?, EContactPhone=?, CourseID=?, Bib=? where ParticipantID=?""",
            [fname,lname,gender,bday,phone,textable,email,street1,street2,city,state,zipcode,ename,ephone,cid,bib,pid])

            self.participants_filldata(tv)
            croot.destroy()

        croot = tk.Tk()
        croot.title("MM: Edit Participant")
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

        def gender_selected(arg):
            self.part_gender = arg

        gender_f = tk.Radiobutton(croot, text='Female',variable=self.gender_var, value='F',command=partial(gender_selected,'F'))
        gender_m = tk.Radiobutton(croot, text='Male',variable=self.gender_var, value='M',command=partial(gender_selected,'M'))
        gender_o = tk.Radiobutton(croot, text='Other',variable=self.gender_var, value='O',command=partial(gender_selected,'O'))
        gender_f.grid(row=2,column=0,sticky='w')
        gender_m.grid(row=2,column=1,sticky='w')
        gender_o.grid(row=2,column=2,sticky='w')
        if gender == 'F':
            gender_f.invoke()
        elif gender == 'M':
            gender_m.invoke()
        else:
            gender_o.invoke()
            

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

        chkTextable = ttk.Checkbutton(croot,text="Textable")
        chkTextable.grid(row=4,column=3,sticky='w')
        if textable:
            chkTextable.state(['!alternate'])
            chkTextable.state(['selected'])
        else:
            chkTextable.state(['!alternate'])
            chkTextable.state(['!selected'])

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


