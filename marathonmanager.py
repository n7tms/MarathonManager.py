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
# from tkinter import Tk
from tkinter import ttk
import tkinter as tk
from tkinter import colorchooser
import re
from datetime import datetime
# from PIL import ImageTk, Image


# =============================================================================
# Constants
DB_NAME = 'mm_test2.db'
DB_NAME_SETTINGS = 'mmsettings.db'
CONN = None
CUR = None

# =============================================================================
# Function Definitions
#
def database_exists(db_name: str) -> bool:
    """Test if the specified database file exists."""
    path = Path(db_name)
    if path.is_file():
        return True
    else:
        return False

def create_database(db_name: str = None) -> bool:
    """Create the initial Marathon Manager database and populate it with some
    global data."""
    global CONN
    global CUR

    # # Users Table
    # sStmt = """CREATE TABLE Users (UserID INTEGER, PersonID INTEGER, Username TEXT, Password TEXT, Permission INTEGER)"""
    # CUR.execute(sStmt)

    # Volunteers Table
    sStmt = """CREATE TABLE IF NOT EXISTS Volunteers (
            VolunteerID INTEGER UNIQUE, 
            Firstname TEXT, 
            Lastname TEXT, 
            Gender TEXT, 
            Birthdate TEXT, 
            Phone TEXT, 
            Textable INTEGER, 
            Email TEXT, 
            Street1 TEXT, 
            Street2 TEXT, 
            City TEXT, 
            State TEXT, 
            Zipcode TEXT, 
            EContactName TEXT, 
            EContactPhone TEXT, 
            Callsign TEXT, 
            Username TEXT,
            Password TEXT,
            Permission INTEGER,
            PRIMARY KEY(VolunteerID AUTOINCREMENT)
            );"""
    CUR.execute(sStmt)

    # Volunteer Log Table (history of assignments, check-ins and -outs)
    sStmt = """CREATE TABLE VolLog (
            LogID	INTEGER UNIQUE,
            VolunteerID INTEGER,
            EventID	INTEGER,
            Assignment	TEXT,
            Checkin	TEXT,
            Checkout	TEXT,
            PRIMARY KEY(LogID AUTOINCREMENT)
        )"""
    CUR.execute(sStmt)

    # Participants Table
    sStmt = """CREATE TABLE Participants (
            ParticipantID	INTEGER UNIQUE,
            Firstname TEXT, 
            Lastname TEXT, 
            Gender TEXT, 
            Birthdate TEXT, 
            Phone TEXT, 
            Textable INTEGER, 
            Email TEXT, 
            Street1 TEXT, 
            Street2 TEXT, 
            City TEXT, 
            State TEXT, 
            Zipcode TEXT, 
            EContactName TEXT, 
            EContactPhone TEXT, 
            EventID	INTEGER,
            RaceID	INTEGER,
            Bib	INTEGER,
            PRIMARY KEY(ParticipantID AUTOINCREMENT)
        )"""
    CUR.execute(sStmt)

    # Events Table
    sStmt = """CREATE TABLE Events (
            EventID	INTEGER UNIQUE,
            EventName	TEXT,
            Description	TEXT,
            Location	TEXT,
            Starttime	TEXT,
            Endtime	TEXT,
            PublicCode	TEXT UNIQUE,
            PRIMARY KEY(EventID AUTOINCREMENT)
        );"""
    CUR.execute(sStmt)

    # Courses Table
    sStmt = """CREATE TABLE Courses (
            CourseID	INTEGER UNIQUE,
            EventID	INTEGER,
            CourseName	TEXT,
            Distance	TEXT,
            Color	TEXT,
            Path    TEXT,
            PRIMARY KEY(CourseID AUTOINCREMENT)
        );"""
    CUR.execute(sStmt)

    # Checkpoints Table
    sStmt = """CREATE TABLE Checkpoints (
            CheckpointID	INTEGER UNIQUE,
            EventID	INTEGER,
            CPName	TEXT,
            Description	TEXT,
            Longitude	NUMERIC,
            Latitude	NUMERIC,
            PRIMARY KEY(CheckpointID AUTOINCREMENT)
        );"""
    CUR.execute(sStmt)

    # Sitings Table
    sStmt = """CREATE TABLE Sitings (
            SitingID	INTEGER UNIQUE,
            EventID	INTEGER,
            CheckpointID	INTEGER,
            ParticipantID	INTEGER,
            Sitingtime	TEXT,
            PRIMARY KEY(SitingID AUTOINCREMENT)
        );"""
    CUR.execute(sStmt)

    # Traffic Table
    sStmt = """CREATE TABLE Traffic (
            TrafficID	INTEGER UNIQUE,
            EventID	INTEGER,
            Logtime	TEXT,
            Message	TEXT,
            Source TEXT,
            AssignedTo	TEXT,
            CompletedTime	TEXT,
            Status	TEXT,
            PRIMARY KEY(TrafficID AUTOINCREMENT)
        );"""
    CUR.execute(sStmt)

    CONN.commit()

    sStmt = "CREATE TABLE IF NOT EXISTS Settings (SettingID INTEGER UNIQUE, SettingName TEXT, SettingValue TEXT, PRIMARY KEY(SettingID AUTOINCREMENT))"
    CUR.execute(sStmt)

    sStmt = "CREATE TABLE IF NOT EXISTS Recents (RecentID INTEGER UNIQUE, EventName TEXT, DBPath TEXT, PRIMARY KEY(RecentID AUTOINCREMENT))"
    CUR.execute(sStmt)

    # Add the settings fields
    # sStmt = 'INSERT INTO Settings (SettingName, SettingValue) VALUES ("DBVersion","1")'
    CUR.execute("""INSERT INTO Settings (SettingName, SettingValue) VALUES ('DBVersion','1')""")
    CONN.commit()

    # Local Users Table
    sStmt = "CREATE TABLE IF NOT EXISTS LocalUsers (UserID INTEGER, Username TEXT, Password TEXT, Permission INTEGER)"
    CUR.execute(sStmt)

    # Add a local admin user
    sStmt = "INSERT INTO LocalUsers (Username, Password, Permission) VALUEs ('admin', 'admin', 1)"
    CUR.execute(sStmt)
    CONN.commit()



# def create_settings_database(db_name: str = None) -> bool:
#     sStmt = "CREATE TABLE IF NOT EXISTS Settings (SettingID INTEGER UNIQUE, SettingName TEXT, SettingValue TEXT, PRIMARY KEY(SettingID AUTOINCREMENT))"
#     CUR.execute(sStmt)

#     sStmt = "CREATE TABLE IF NOT EXISTS Recents (RecentID INTEGER UNIQUE,	EventName TEXT,	DBPath TEXT, PRIMARY KEY(RecentID AUTOINCREMENT))"
#     CUR.execute(sStmt)

#     # Add the settings fields
#     # sStmt = 'INSERT INTO Settings (SettingName, SettingValue) VALUES ("DBVersion","1")'
#     CUR.execute("""INSERT INTO Settings (SettingName, SettingValue) VALUES ('DBVersion','1')""")
#     CONN.commit()

#     # Local Users Table
#     sStmt = "CREATE TABLE IF NOT EXISTS LocalUsers (UserID INTEGER, Username TEXT, Password TEXT, Permission INTEGER)"
#     CUR.execute(sStmt)

#     # Add a local admin user
#     sStmt = "INSERT INTO LocalUsers (Username, Password, Permission) VALUEs ('admin', 'admin', 1)"
#     CUR.execute(sStmt)
#     CONN.commit()


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
#  Sitings Window
# =============================================================================

def siting_window(main_frame: tk.Frame) -> tk.Frame:
    cn,cur = None,None
    checkpoints = []

    def sitings_filldata(tv:ttk.Treeview):
        for item in tv.get_children():
            tv.delete(item)
        
        cn = sqlite3.connect(DB_NAME)
        cur = cn.cursor()
        cur.execute("select s.SitingID, s.SitingTime, c.CPName, pa.Bib || ' ' || pa.Firstname || ' ' || pa.Lastname from Sitings as s, Checkpoints as c, Participants as pa where s.CheckpointID=c.CheckpointID and s.ParticipantID=pa.ParticipantID order by s.SitingTime DESC;")
        rows = cur.fetchall()

        for row in rows:
            tv.insert("",'end',values=row,tags=str(row[0]))

    def get_checkpoints() -> list:
        """return a list of checkpoints"""
        if len(checkpoints) > 0:
            checkpoints.clear()

        res = cur.execute("select CheckpointID,CPName from Checkpoints")
        for x in res:
            checkpoints.append(x)
        
        cps = []
        for x in checkpoints:
            cps.append(x[1])
        return cps

    def bib_enterkey(event):
        """Check if the Enter key was pressed from inside the bib text field"""
        if event.keysym == 'Return' or event.keysym == 'KP_Enter':
            submit_bibs()

    def update_status(message,color='green'):
        """set the value of the status label"""
        # consider incorporating a color: green for good; yellow for warning; red for error.
        lblStatus.configure(text=message,background=color)

    def validate_fields() -> bool:
        """make sure the checkpoint and bibs fields are valid"""
        return True

    def submit_bibs():
        """Write the sited bibs to the database"""
        if validate_fields():
            bibs = re.split(r',| |\.|\+',txtBibs.get())
            count = len(bibs)

            # Get the checkpoint ID
            cid = -1
            for c in checkpoints:
                if c[1] == cmbCheckpoint.get():
                    cid = c[0]
                    break
            if cid < 0:
                raise "Sitings: Checkpoint not found."
            
            # remove duplicate bibs (raise an error?)
            bibs = list(set(bibs))
            
            # iterate through the list of bibs
            for b in bibs:
                # check if it exists in the database; add it if it doesn't
                partID = -1
                stmt = "select ParticipantID from Participants where Bib=" + b + ";"
                res = list(cur.execute(stmt))
                if len(res) == 0:
                    # add the bib to Participants
                    stmt = "insert into Participants (EventID,Firstname,Lastname,RaceID,Bib) values (1,'','',0," + b + ");"
                cur.execute(stmt)
                cn.commit()

                # get the participantID belonging to this bib
                stmt = "select ParticipantID from Participants where Bib=" + b + ";"
                res = list(cur.execute(stmt))
                partID = res[0][0]

                # add the siting to the sitings table
                stmt = "insert into Sitings (EventID, CheckpointID, ParticipantID, Sitingtime) values (1," + str(cid) + "," + str(partID) + ",'" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "');"
                res =  cur.execute(stmt)
            cn.commit()

            status = str(count) + " bibs submitted Successfully at " + datetime.now().strftime("%H:%M:%S")

            update_status(status)
            txtBibs.delete(0,'end')
            sitings_filldata(tvSitings)
        else:
            update_status("Problem. Check checkpoints or bibs.")

    def update_clock():
        """Update the clock every second."""
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        lblTime.configure(text=current_time)
        main_frame.after(1000,update_clock)

    def sitings_edit_row(event):
        item = tvSitings.item(tvSitings.focus(),"values")
        print(item)


    # sf = tk.Frame(main_frame,highlightbackground='blue',highlightthickness=1)
    cn = sqlite3.connect(DB_NAME)
    cur = cn.cursor()

    lblTime = ttk.Label(main_frame,width=10,background='#ffffff')
    lblTime.grid(row=0,column=0,sticky='W', padx=5, pady=8)
    lblTime.config(anchor='center')

    cmbCheckpoint = ttk.Combobox(main_frame,width=10,values=get_checkpoints())
    cmbCheckpoint.grid(row=0,column=1,sticky='W',  padx=5, pady=8)
    cmbCheckpoint.set(checkpoints[0][1])

    txtBibs = ttk.Entry(main_frame,width=30)
    txtBibs.grid(row=0,column=2,sticky='W',  padx=5, pady=8)
    txtBibs.bind("<KeyPress>",bib_enterkey)

    butSubmit = ttk.Button(main_frame,text='Submit',width=10,command=submit_bibs)
    butSubmit.grid(row=0,column=3,sticky='W',  padx=5, pady=8)

    lblStatus = ttk.Label(main_frame,text='this is where the status goes', relief="sunken")
    lblStatus.grid(row=1,column=0,columnspan=4,sticky='we',padx=5)

    tvSitings = ttk.Treeview(main_frame,column=("c1","c2","c3","c4"),show='headings',selectmode='browse')
    tvSitings.column("#1",anchor='w',minwidth=30,width=60,stretch='no')
    tvSitings.heading("#1",text="ID",anchor='w')
    tvSitings.column("#2",anchor='w',minwidth=30,width=110,stretch='no')
    tvSitings.heading("#2",text="Time",anchor='w')
    tvSitings.column("#3",anchor='w',minwidth=30,width=100,stretch='no')
    tvSitings.heading("#3",text="Checkpoint",anchor='w')
    tvSitings.column("#4",anchor='w',minwidth=30,width=240,stretch='no')
    tvSitings.heading("#4",text="Participant",anchor='w')
    tvSitings.grid(row=2,column=0,columnspan=4,padx=5,pady=15)
    tvSitings.bind("<Double-1>",sitings_edit_row)

    yscrollbar = ttk.Scrollbar(main_frame,orient='vertical',command=tvSitings.yview)
    yscrollbar.grid(row=2, column=5, sticky='nse')
    yscrollbar.configure(command=tvSitings.yview)    
    tvSitings.configure(yscrollcommand=yscrollbar.set)

    sitings_filldata(tvSitings)
    

    update_clock()

    # return sf




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
#  Report/Status Panel
# =============================================================================

# Should these checkpoint functions be inside the checkpoint window definition?
def checkpoint_filldata(tv:ttk.Treeview) -> None:
    """Clear and then fill/refresh the Checkpoints table with data"""
    # clear the table
    for item in tv.get_children():
        tv.delete(item)

    # get the checkpoints from the database
    cn = sqlite3.connect(DB_NAME)
    cur = cn.cursor()
    cur.execute("select CheckpointID, CPName, Description, 'somewhere' from Checkpoints;")
    rows = cur.fetchall()
    for row in rows:
        tv.insert("",tk.END,values=row)

def checkpoint_edit(checkpoint,tv):
    if checkpoint:
        cpid,cname,cdescription,clocation = checkpoint
    else:
        cpid,cname,cdescription,clocation = '','','',''

    def cancel():
        croot.destroy()

    def save():
        """Create/insert a new Checkpoint"""
        cn = sqlite3.connect(DB_NAME)
        cur = cn.cursor()

        cpid = txtCPID.get()
        cname=txtName.get()
        cdescription = txtDescr.get()
        clocation = txtLoc.get()
        cur.execute("insert into Checkpoints (CPName, Description) values(?,?);",[cname,cdescription])
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
        clocation = txtLoc.get()
        cur.execute("update Checkpoints set CPName=?, Description=? where CheckpointID=?",[cname,cdescription,cpid])
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

    lblLoc = ttk.Label(croot,text="Location:")
    lblLoc.grid(row=3,column=0,sticky='e')
    txtLoc = ttk.Entry(croot)
    txtLoc.grid(row=3,column=1,columnspan=2,sticky='w')
    txtLoc.insert(0,clocation)

    if checkpoint:
        butSave = ttk.Button(croot,text="Update",command=update)
        butSave.grid(row=4,column=1,sticky='e')
    else:
        butSave = ttk.Button(croot,text="Save",command=save)
        butSave.grid(row=4,column=1,sticky='e')

    butCancel = ttk.Button(croot,text="Cancel",command=cancel)
    butCancel.grid(row=4,column=2,sticky='w')



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

    tvCheckpoints = ttk.Treeview(main_frame,column=("c1","c2","c3","c4"),show='headings',selectmode='browse')
    tvCheckpoints.column("#1",anchor='center')
    tvCheckpoints.heading("#1",text="CP ID")
    tvCheckpoints.column("#2",anchor='w')
    tvCheckpoints.heading("#2",text="Checkpoint")
    tvCheckpoints.column("#3",anchor='w')
    tvCheckpoints.heading("#3",text="Description")
    tvCheckpoints.column("#4",anchor='w')
    tvCheckpoints.heading("#4",text="Location")
    tvCheckpoints.grid(row=2,column=0,columnspan=3,padx=5,pady=5)
    tvCheckpoints.bind("<Double-1>",checkpoint_edit_row)
    checkpoint_filldata(tvCheckpoints)

    btnClose = ttk.Button(main_frame,text="Close",command=checkpoint_close)
    btnClose.grid(row=3,column=2,padx=5,pady=5,sticky='w')





# =============================================================================
#  Courses Window
# =============================================================================

# Should these course functions be inside the course window definition?
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
    courses_filldata(tvCourses)

    btnClose = ttk.Button(main_frame,text="Close",command=courses_close)
    btnClose.grid(row=3,column=2,padx=5,pady=5,sticky='w')







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
        root.geometry('825x340')
        ew = checkpoint_window(root)

    def courses_click():
        root = tk.Tk()
        root.title("MM: Courses")
        root.geometry('825x340')
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
        sitings.geometry('550x320')
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



# =============================================================================
# NOTES
# 
# how to store id "in" combobox: https://www.plus2net.com/python/tkinter-Combobox-mysql.php
# 

# =============================================================================
# TODO
# add hidden columns in tvSitings for CheckpointID and ParticipantID
# Create the edit siting window and function
# Is it possible to hide a CheckpointID in the cmbCheckpoint element?
#
# need to make sure tick (and quotes?) are not used in queries.

