# Marathon Manger - GUI Definitions

# Some good examples of combining layout managers -- including frames within frames.
# https://stackoverflow.com/questions/36506152/tkinter-grid-or-pack-inside-a-grid
# https://github.com/Akuli/tkinter-tutorial/blob/master/geometry-managers.md


import tkinter as tk
from tkinter import ttk
import sqlite3
import re
from datetime import datetime
# from PIL import ImageTk, Image

DB = 'mm_test.db'


def quick_links(main_frame: tk.Frame) -> tk.Frame:
    qlf = Frame(main_frame,highlightbackground="blue",highlightthickness=1)

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

def siting_window(main_frame: tk.Frame) -> tk.Frame:
    cn,cur = None,None
    checkpoints = []

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
                stmt = "select PersonID from Participants where Bib=" + b + ";"
                res = list(cur.execute(stmt))
                if len(res) == 0:
                    # add the bib
                    stmt = "insert into Participants (EventID,RaceID,Bib) values (1,0," + b + ");"
                cur.execute(stmt)
                cn.commit()

                # get the participantID belonging to this bib
                stmt = "select PersonID from Participants where Bib=" + b + ";"
                res = list(cur.execute(stmt))
                partID = res[0][0]

                # add the siting to the sitings table
                stmt = "insert into Sitings (EventID, CheckpointID, ParticipantID, Sitingtime) values (1," + str(cid) + "," + str(partID) + ",'" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "');"
                res =  cur.execute(stmt)
            cn.commit()

            status = str(count) + " bibs submitted Successfully at " + datetime.now().strftime("%H:%M:%S")

            update_status(status)
            txtBibs.delete(0,END)
        else:
            update_status("Problem. Check checkpoints or bibs.")

    def update_clock():
        """Update the clock every second."""
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        lblTime.configure(text=current_time)
        sf.after(1000,update_clock)


    sf = tk.Frame(main_frame,highlightbackground='blue',highlightthickness=1)
    cn = sqlite3.connect(DB)
    cur = cn.cursor()

    lblTime = ttk.Label(sf,width=10,background='#ffffff')
    lblTime.grid(row=0,column=0,sticky='W', padx=5, pady=8)
    lblTime.config(anchor='center')

    cmbCheckpoint = ttk.Combobox(sf,width=10,values=get_checkpoints())
    cmbCheckpoint.grid(row=0,column=1,sticky='W',  padx=5, pady=8)
    cmbCheckpoint.set(checkpoints[0][1])

    txtBibs = ttk.Entry(sf,width=30)
    txtBibs.grid(row=0,column=2,sticky='W',  padx=5, pady=8)
    txtBibs.bind("<KeyPress>",bib_enterkey)

    butSubmit = ttk.Button(sf,text='Submit',width=10,command=submit_bibs)
    butSubmit.grid(row=0,column=3,sticky='W',  padx=5, pady=8)

    lblStatus = ttk.Label(sf,text='this is where the status goes', relief="sunken")
    lblStatus.grid(row=1,column=0,columnspan=4,sticky='we')

    update_clock()

    return sf

def event_window(main_frame: tk.Frame) -> tk.Frame:
    cn,cur = None,None

    cn = sqlite3.connect(DB)
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

    lblEventName = ttk.Label(main_frame,text='Event Name:',width=10)
    lblEventName.grid(row=0,column=1,sticky='w', padx=5, pady=8)
    txtEventName = ttk.Entry(main_frame,width=25)
    txtEventName.grid(row=0,column=2, columnspan=2)
    
    lblDescription = ttk.Label(main_frame,text='Description:',width=10)
    lblDescription.grid(row=1,column=1)
    txtDescription = tk.Entry(main_frame,width=25)
    txtDescription.grid(row=1,column=2, columnspan=2)

    lblLocation = ttk.Label(main_frame,text='Location:',width=10)
    lblLocation.grid(row=2,column=1)
    txtLocation = tk.Entry(main_frame,width=10)
    txtLocation.grid(row=2,column=2,sticky='w')

    lblStartDate = ttk.Label(main_frame,text='Start Date:',width=10)
    lblStartDate.grid(row=3,column=1)
    txtStartDate = tk.Entry(main_frame,width=10)
    txtStartDate.grid(row=3,column=2,sticky='w')

    lblStartTime = ttk.Label(main_frame,text='Start Time:',width=10)
    lblStartTime.grid(row=4,column=1)
    txtStartTime = tk.Entry(main_frame,width=10)
    txtStartTime.grid(row=4,column=2,sticky='w')

    butSave = ttk.Button(main_frame,text='Save',command=event_save)
    butSave.grid(row=3,column=3)
    butCancel = ttk.Button(main_frame,text='Cancel',command=event_cancel)
    butCancel.grid(row=4,column=3)
    
    return main_frame

def reports_status(main_frame: tk.Frame) -> tk.Frame:
    rsf = tk.Frame(main_frame,highlightbackground="blue",highlightthickness=1)
    rsf.highlightbackground="blue"
    rsf.highlightthickness=1

    lblTitle = ttk.Label(rsf,text='Reports/Status')

    lblTitle.grid(row=0,column=0,sticky='w', padx=5, pady=8)

    return rsf

def logs(main_frame: tk.Frame) -> tk.Frame:
    lf = tk.Frame(main_frame,highlightbackground="blue",highlightthickness=1)

    lblTitle = ttk.Label(lf,text='Log')

    lblTitle.grid(row=0,column=0,sticky='W', padx=5, pady=8)

    return lf

def volunteers(main_frame: tk.Frame) -> tk.Frame:
    vf = tk.Frame(main_frame,highlightbackground="blue",highlightthickness=1)

    lblTitle = ttk.Label(vf,text='Volunteers')

    lblTitle.grid(row=0,column=0,sticky='W', padx=5, pady=8)

    return vf

def messages(main_frame: tk.Frame) -> tk.Frame:
    mf = tk.Frame(main_frame,highlightbackground="blue",highlightthickness=1)

    lblTitle = ttk.Label(mf,text='Messages')

    lblTitle.grid(row=0,column=0,sticky='W', padx=5, pady=8)

    return mf   


def checkpoint_window(main_frame:tk.Frame) -> tk.Frame:
    cn,cur = None,None

    cn = sqlite3.connect(DB)
    cur = cn.cursor()

    def checkpoint_save():
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

    def checkpoint_cancel():
        main_frame.destroy()

    def checkpoint_new():
        print("New Checkpoint")

    def checkpoint_map():
        print("Map Checkpoint")

    def checkpoint_filldata():
        cur.execute("select CPName, Description, 'somewhere','edit' from Checkpoints;")
        rows = cur.fetchall()
        for row in rows:
            print(row)
            tvCheckpoints.insert("",tk.END,values=row)

    title = ttk.Label(main_frame,text='Checkpoints',font=('Arial',18))
    title.grid(row=0,column=0,columnspan=2,sticky='nw')

    lblLogo = ttk.Label(main_frame,text="Logo Placeholder")
    lblLogo.grid(row=0,column=2,rowspan=2,sticky='news')

    btnNew = ttk.Button(main_frame,text="New Checkpoint",command=checkpoint_new)
    btnNew.grid(row=1,column=0,padx=5,pady=5,sticky='e')

    btnMap = ttk.Button(main_frame,text="Map Checkpoints",command=checkpoint_map)
    btnMap.grid(row=1,column=1,padx=5,pady=5,sticky='w')

    # tvCheckpoints = ttk.Treeview(main_frame,column=("Checkpoint","Description","Location","Edit"),show='headings')
    tvCheckpoints = ttk.Treeview(main_frame,column=("c1","c2","c3","c4"),show='headings',selectmode='browse')
    tvCheckpoints.column("#1",anchor='w')
    tvCheckpoints.heading("#1",text="Checkpoint")
    tvCheckpoints.column("#2",anchor='w')
    tvCheckpoints.heading("#2",text="Description")
    tvCheckpoints.column("#3",anchor='w')
    tvCheckpoints.heading("#3",text="Location")
    tvCheckpoints.column("#4",anchor='center')
    tvCheckpoints.heading("#4",text="Edit")
    tvCheckpoints.grid(row=2,column=0,columnspan=3,padx=5,pady=5)
    checkpoint_filldata()

    btnSave = ttk.Button(main_frame,text="Save",command=checkpoint_save)
    btnSave.grid(row=3,column=1,padx=5,pady=5,sticky='e')

    btnCancel = ttk.Button(main_frame,text="Cancel",command=checkpoint_cancel)
    btnCancel.grid(row=3,column=2,padx=5,pady=5,sticky='w')


def course_edit(item):
    # display the form
    # fill the form
    # save the edited form
    cid,cname,cdistance,ccolor = item
    print("Editing:",cid,cname,cdistance,ccolor)


    def cancel():
        print("course edit canceled")
        c_root.destroy()
    
    def save():
        cn = sqlite3.connect(DB)
        cur = cn.cursor()

        cname=txtName.get()
        cdistance=txtDistance.get()
        ccolor=txtColor.get()
        # cur.execute("update Courses set CourseName=?, Distance=?, Color=? where CourseID=?",[cname,cdistance,ccolor,cid])
        cur.execute("update Courses set CourseName='Full', Distance='26.2' where CourseID=3")
        cn.commit

        c_root.destroy()


    c_root = tk.Tk()
    c_root.title("MM: Edit Course")
    c_root.geometry('250x150')

    lblCID = ttk.Label(c_root,text="Course ID:")
    lblCID.grid(row=0,column=0,sticky='e')
    txtCID = ttk.Entry(c_root)
    txtCID.grid(row=0,column=1,columnspan=2,sticky='w')
    txtCID.insert(0,cid)
    txtCID.config(state="disabled")

    lblName = ttk.Label(c_root,text="Name:")
    lblName.grid(row=1,column=0,sticky='e')
    txtName = ttk.Entry(c_root)
    txtName.grid(row=1,column=1,columnspan=2,sticky='w')
    txtName.insert(0,cname)

    lblDistance = ttk.Label(c_root,text="Distance:")
    lblDistance.grid(row=2,column=0,sticky='e')
    txtDistance = ttk.Entry(c_root)
    txtDistance.grid(row=2,column=1,columnspan=2,sticky='w')
    txtDistance.insert(0,cdistance)

    lblColor = ttk.Label(c_root,text="Color:")
    lblColor.grid(row=3,column=0,sticky='e')
    txtColor = ttk.Entry(c_root)
    txtColor.grid(row=3,column=1,columnspan=2,sticky='w')
    txtColor.insert(0,ccolor)

    butSave = ttk.Button(c_root,text="Save",command=save)
    butSave.grid(row=4,column=1,sticky='e')

    butCancel = ttk.Button(c_root,text="Cancel",command=cancel)
    butCancel.grid(row=4,column=2,sticky='w')


def courses_window(main_frame:tk.Frame) -> tk.Frame:
    cn,cur = None,None

    cn = sqlite3.connect(DB)
    cur = cn.cursor()

    def courses_save():
        # get the field values
        # eName = txtEventName.get()
        # eDescription = txtDescription.get()
        # eLocation = txtLocation.get()
        # eDate = txtStartDate.get()
        # eTime = txtStartTime.get()
        # eStart = eDate + ' ' + eTime

        # # TODO: Error checking; Do the fields contain valid information

        # stmt = "insert into Events (EventName, Description, Location, Starttime) values ('" + eName + "','" + eDescription + "','" + eLocation + "','" + eStart + "');"
        # res =  cur.execute(stmt)
        # cn.commit()
        print("courses saved")
        main_frame.destroy()

    def courses_cancel():
        main_frame.destroy()

    def courses_new():
        print("New Course")

    def courses_filldata():
        # clear the table
        for item in tvCourses.get_children():
            tvCourses.delete(item)

        # get the courses from the database
        cur.execute("select CourseID, CourseName, Distance, Color from Courses;")
        rows = cur.fetchall()
        
        # populate the treeview with the data
        for row in rows:
            tvCourses.tag_configure(str(row[0]),background=row[3])
            tvCourses.insert("",tk.END,values=row,tags=str(row[0]))

    def courses_edit_row(event):
        item = tvCourses.item(tvCourses.focus(),"values")
        print("Clicked:",item)
        course_edit(item)
        courses_filldata()

    title = ttk.Label(main_frame,text='Courses',font=('Arial',18))
    title.grid(row=0,column=0,sticky='nw')

    lblLogo = ttk.Label(main_frame,text="Logo Placeholder")
    lblLogo.grid(row=0,column=2,rowspan=2,sticky='news')

    btnNew = ttk.Button(main_frame,text="New Course",command=courses_new)
    btnNew.grid(row=1,column=0,padx=5,pady=5,sticky='w')

    tvCourses = ttk.Treeview(main_frame,column=("c1","c2","c3","c4"),show='headings',selectmode='browse')
    tvCourses.column("#1",anchor='w')
    tvCourses.heading("#1",text="CourseID")
    tvCourses.column("#2",anchor='w')
    tvCourses.heading("#2",text="Course")
    tvCourses.column("#3",anchor='w')
    tvCourses.heading("#3",text="Distance")
    tvCourses.column("#4",anchor='w')
    tvCourses.heading("#4",text="Color")
    tvCourses.grid(row=2,column=0,columnspan=3,padx=5,pady=5)
    tvCourses.bind("<Double-1>",courses_edit_row)
    courses_filldata()

    btnSave = ttk.Button(main_frame,text="Save",command=courses_save)
    btnSave.grid(row=3,column=1,padx=5,pady=5,sticky='e')

    btnCancel = ttk.Button(main_frame,text="Cancel",command=courses_cancel)
    btnCancel.grid(row=3,column=2,padx=5,pady=5,sticky='w')



def mainmenubar(main_frame: tk.Frame) -> tk.Frame:
    mmb = tk.Menu(main_frame)

    def donothing():
        pass

    def event_click():
        e_root = tk.Tk()
        e_root.title("MM: Event")
        e_root.geometry('500x150')
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
    eventmenu.add_command(label="Paths", command=donothing)
    eventmenu.add_separator()
    eventmenu.add_command(label="Participants", command=donothing)
    mmb.add_cascade(label="Event", menu=eventmenu)

    helpmenu = tk.Menu(mmb, tearoff=0)
    helpmenu.add_command(label="Help Index", command=donothing)
    helpmenu.add_command(label="About...", command=donothing)
    mmb.add_cascade(label="Help", menu=helpmenu)

    return mmb
        