# Marathon Manger - GUI Definitions

# Some good examples of combining layout managers -- including frames within frames.
# https://stackoverflow.com/questions/36506152/tkinter-grid-or-pack-inside-a-grid
# https://github.com/Akuli/tkinter-tutorial/blob/master/geometry-managers.md


import tkinter as tk
from tkinter import ttk
import sqlite3
import re
from datetime import datetime


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
    db = 'mm_test.db'
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

    def update_status(message):
        """set the value of the status label"""
        # consider incorporating a color: green for good; yellow for warning; red for error.
        lblStatus.configure(text=message)

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
    cn = sqlite3.connect(db)
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
    db = 'mm_test.db'
    cn,cur = None,None

    cn = sqlite3.connect(db)
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

    frame = tk.Frame(main_frame)
    canvas = tk.Canvas(frame,width=300, height=300, bg='blue')
    canvas.pack(expand='yes', fill='both')
    gif1 = tk.PhotoImage(file='runner_blue.png')
    canvas.create_image(10, 10, image=gif1, anchor='nw')

    # imgLogo = ttk.canvas()
    # imgLogo = Tk.Canvas(width=100,height=100,bg='white')
    # imgLogo = ttk.Label(main_frame,text="Logo goes here")
    frame.grid(row=0,column=0,rowspan=5)

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

def mainmenubar(main_frame: tk.Frame) -> tk.Frame:
    mmb = tk.Menu(main_frame)

    def donothing():
        pass

    def event_click():
        e_root = tk.Tk()
        e_root.title("MM: Event")
        e_root.geometry('410x150')
        ew = event_window(e_root)

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
    eventmenu.add_command(label="Checkpoints", command=donothing)
    eventmenu.add_command(label="Courses", command=donothing)
    eventmenu.add_command(label="Paths", command=donothing)
    eventmenu.add_separator()
    eventmenu.add_command(label="Participants", command=donothing)
    mmb.add_cascade(label="Event", menu=eventmenu)

    helpmenu = tk.Menu(mmb, tearoff=0)
    helpmenu.add_command(label="Help Index", command=donothing)
    helpmenu.add_command(label="About...", command=donothing)
    mmb.add_cascade(label="Help", menu=helpmenu)

    return mmb
        