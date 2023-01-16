# Marathon Manger - GUI Definitions

# Some good examples of combining layout managers -- including frames within frames.
# https://stackoverflow.com/questions/36506152/tkinter-grid-or-pack-inside-a-grid
# https://github.com/Akuli/tkinter-tutorial/blob/master/geometry-managers.md


from tkinter import *
from tkinter import ttk
import sqlite3
import re
from datetime import datetime


def quick_links(main_frame: Frame) -> Frame:
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

def siting_window(main_frame: Frame) -> Frame:
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


    sf = Frame(main_frame,highlightbackground="blue",highlightthickness=1)
    cn = sqlite3.connect(db)
    cur = cn.cursor()

    lblTime = ttk.Label(sf,width=10)
    lblTime.grid(row=0,column=0,sticky='W', padx=5, pady=8)

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

def reports_status(main_frame: Frame) -> Frame:
    rsf = Frame(main_frame,highlightbackground="blue",highlightthickness=1)
    rsf.highlightbackground="blue"
    rsf.highlightthickness=1

    lblTitle = ttk.Label(rsf,text='Reports/Status')

    lblTitle.grid(row=0,column=0,sticky='W', padx=5, pady=8)

    return rsf

def logs(main_frame: Frame) -> Frame:
    lf = Frame(main_frame,highlightbackground="blue",highlightthickness=1)

    lblTitle = ttk.Label(lf,text='Log')

    lblTitle.grid(row=0,column=0,sticky='W', padx=5, pady=8)

    return lf

def volunteers(main_frame: Frame) -> Frame:
    vf = Frame(main_frame,highlightbackground="blue",highlightthickness=1)

    lblTitle = ttk.Label(vf,text='Volunteers')

    lblTitle.grid(row=0,column=0,sticky='W', padx=5, pady=8)

    return vf

def messages(main_frame: Frame) -> Frame:
    mf = Frame(main_frame,highlightbackground="blue",highlightthickness=1)

    lblTitle = ttk.Label(mf,text='Messages')

    lblTitle.grid(row=0,column=0,sticky='W', padx=5, pady=8)

    return mf   

def mainmenubar(main_frame: Frame) -> Frame:
    mmb = Menu(main_frame)

    def donothing():
        pass

    filemenu = Menu(mmb, tearoff=0)
    filemenu.add_command(label="New", command=donothing)
    filemenu.add_separator()
    filemenu.add_command(label="Open", command=donothing)
    filemenu.add_command(label="Close", command=donothing)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=main_frame.quit)
    mmb.add_cascade(label="File", menu=filemenu) 

    editmenu = Menu(mmb, tearoff=0)
    editmenu.add_command(label="Undo", command=donothing)
    editmenu.add_separator()
    editmenu.add_command(label="Cut", command=donothing)
    editmenu.add_command(label="Copy", command=donothing)
    editmenu.add_command(label="Paste", command=donothing)
    editmenu.add_command(label="Delete", command=donothing)
    editmenu.add_command(label="Select All", command=donothing)
    mmb.add_cascade(label="Edit", menu=editmenu)

    helpmenu = Menu(mmb, tearoff=0)
    helpmenu.add_command(label="Help Index", command=donothing)
    helpmenu.add_command(label="About...", command=donothing)
    mmb.add_cascade(label="Help", menu=helpmenu)

    return mmb
        