# Marathon Manager
#
# Sitings Functions
#



from pathlib import Path
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from tkinter import colorchooser
import re
from datetime import datetime
from constants import *


# =============================================================================
#  Sitings Window
# =============================================================================

def siting_window(main_frame: tk.Frame) -> tk.Frame:
    checkpoints = {}
    after_id = ''

    def sitings_filldata(tv:ttk.Treeview):
        for item in tv.get_children():
            tv.delete(item)
        
        stmt = "select s.SitingID, s.SitingTime, c.CPName, pa.ParticipantID,pa.Bib || ' ' || pa.Firstname || ' ' || pa.Lastname as BibName from Sitings as s, Checkpoints as c, Participants as pa where s.CheckpointID=c.CheckpointID and s.ParticipantID=pa.ParticipantID order by s.SitingTime DESC;"
        rows = DB.query(stmt)

        for row in rows:
            rowvalues = (row['SitingID'], row['SitingTime'], row['CPName'], row['ParticipantID'], row['BibName'])
            tv.insert("",'end',values=rowvalues,tags=str(row['SitingID']))

    def get_checkpoints() -> list:
        """return a list of checkpoints"""
        if len(checkpoints) > 0:
            checkpoints.clear()

        res = DB.query("select CheckpointID,CPName from Checkpoints")
        for x in res:
            checkpoints[x["CPName"]] = x["CheckpointID"]
        
        return list(checkpoints.keys()) 


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
            # for c in checkpoints:
            #     if c[1] == cmbCheckpoint.get():
            #         cid = c[0]
            #         break
            # if cid < 0:
            #     raise "Sitings: Checkpoint not found."
            
            if cmbCheckpoint.get() not in checkpoints:
                raise "Sitings: Checkpoint not found."
            else:
                cid = checkpoints[cmbCheckpoint.get()]
            
            # remove duplicate bibs (raise an error?)
            bibs = list(set(bibs))
            
            # iterate through the list of bibs
            for b in bibs:
                # check if bib exists in the database; add it if it doesn't
                partID = -1
                stmt = """select ParticipantID from Participants where Bib=?"""
                res = DB.query(stmt,[b])
                if len(res) == 0:
                    # add the bib to Participants
                    stmt = "insert into Participants (EventID,Firstname,Lastname,CourseID,Bib) values (1,'','',0,?);"
                    DB.nonQuery(stmt,[b])

                # get the participantID belonging to this bib
                stmt = "select ParticipantID from Participants where Bib=?;"
                res = DB.query(stmt,[b])
                partID = res[0]['ParticipantID']

                # add the siting to the sitings table
                stmt = "insert into Sitings (EventID, CheckpointID, ParticipantID, SitingTime) values (1," + str(cid) + "," + str(partID) + ",'" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "');"
                res =  DB.nonQuery(stmt)

            status = str(count) + " bibs submitted Successfully at " + datetime.now().strftime("%H:%M:%S")

            update_status(status)
            txtBibs.delete(0,'end')
            sitings_filldata(tvSitings)
        else:
            update_status("Problem. Check checkpoints or bibs.")

    def update_clock():
        """Update the clock every second."""
        global after_id
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        lblTime.configure(text=current_time)
        # TODO: after() returns an id, but the id changes with each call.
        # I need to keep the id so the after() call can be cancelled when the 
        # window is destroyed.
        after_id = main_frame.after(1000,update_clock)

    def on_closing():
        # called when the window closes.
        # Ideally, this would cancel the last after() call. [doesn't work]

        # main_frame.after_cancel(after_id)
        main_frame.destroy()
        return

    # TODO Implement the edit siting function
    def sitings_edit_row(event):
        eTime = tk.StringVar()
        eBib = tk.StringVar()

        def submit_edit(xsid,xtime,xbib):
            pass
    
        item = tvSitings.item(tvSitings.focus(),"values")
        sid,timestamp,cp,pid,participant = tvSitings.item(tvSitings.focus(),"values")
        # print(item)
        # messagebox.showinfo(title="MM: Info",message="Edit not yet implemented.",parent=main_frame)

        # Retrieve the siting data from the database
        stmt = 'select SitingID, s.CheckpointID, CPName, s.ParticipantID, Bib, SitingTime from Sitings s, Participants p, Checkpoints c where s.CheckpointID=c.CheckpointID and s.ParticipantID = p.ParticipantID and s.SitingID = ?'
        result = DB.query(stmt,[sid])

        # Create a new window with SitingID, Time, Checkpoint and Bib
        edit_win = tk.Tk()
        edit_win.title("MM: Edit Siting")

        txtTime = ttk.Entry(edit_win,width=20,background='#ffffff',textvariable=eTime)
        txtTime.grid(row=0,column=0,sticky='W', padx=5, pady=8)

        cmbCheckpoint = ttk.Combobox(edit_win,width=10,values=get_checkpoints())
        cmbCheckpoint.grid(row=0,column=1,sticky='W',  padx=5, pady=8)
        cmbCheckpoint.set(list(checkpoints.keys())[0]) 

        txtBibs = ttk.Entry(edit_win,width=10,textvariable=eBib)
        txtBibs.grid(row=0,column=2,sticky='W', padx=5, pady=8)

        butSubmit = ttk.Button(edit_win,text='Submit',width=10,command=submit_edit)
        butSubmit.grid(row=0,column=3,sticky='W', padx=5, pady=8)

        txtTime.delete(0,'end')
        txtTime.insert(0,result[0]['SitingTime'])

        txtBibs.delete(0,'end')
        txtBibs.insert(0,str(result[0]['Bib']))
        cmbCheckpoint.delete(0,'end')
        cmbCheckpoint.insert(0,result[0]['CPName'])


        # Is there a way to make this form modal?


    # sf = tk.Frame(main_frame,highlightbackground='blue',highlightthickness=1)

    lblTime = ttk.Label(main_frame,width=10,background='#ffffff')
    lblTime.grid(row=0,column=0,sticky='W', padx=5, pady=8)
    lblTime.config(anchor='center')

    cmbCheckpoint = ttk.Combobox(main_frame,width=10,values=get_checkpoints())
    cmbCheckpoint.grid(row=0,column=1,sticky='W',  padx=5, pady=8)
    cmbCheckpoint.set(list(checkpoints.keys())[0])

    txtBibs = ttk.Entry(main_frame,width=30)
    txtBibs.grid(row=0,column=2,sticky='W',  padx=5, pady=8)
    txtBibs.bind("<KeyPress>",bib_enterkey)

    butSubmit = ttk.Button(main_frame,text='Submit',width=10,command=submit_bibs)
    butSubmit.grid(row=0,column=3,sticky='W',  padx=5, pady=8)

    lblStatus = ttk.Label(main_frame,text=' ', relief="sunken")
    lblStatus.grid(row=1,column=0,columnspan=4,sticky='we',padx=5)

    tvSitings = ttk.Treeview(main_frame,column=("sid","time","cp","pid","part"),show='headings',selectmode='browse')
    tvSitings.column("sid",anchor='w',minwidth=0,width=0,stretch='no')  # hidden
    tvSitings.heading("sid",text="SID",anchor='w')
    tvSitings.column("time",anchor='w',minwidth=30,width=160,stretch='no')
    tvSitings.heading("time",text="Time",anchor='w')
    tvSitings.column("cp",anchor='w',minwidth=30,width=100,stretch='no')
    tvSitings.heading("cp",text="Checkpoint",anchor='w')
    tvSitings.column("pid",anchor='w',minwidth=0,width=0,stretch='no')  # hidden
    tvSitings.heading("pid",text="PID",anchor='w')
    tvSitings.column("part",anchor='w',minwidth=30,width=290,stretch='no')
    tvSitings.heading("part",text="Participant",anchor='w')
    tvSitings.grid(row=2,column=0,columnspan=4,padx=5,pady=15)
    tvSitings.bind("<Double-1>",sitings_edit_row)

    yscrollbar = ttk.Scrollbar(main_frame,orient='vertical',command=tvSitings.yview)
    yscrollbar.grid(row=2, column=5,pady=15,sticky='nse')
    yscrollbar.configure(command=tvSitings.yview)    
    tvSitings.configure(yscrollcommand=yscrollbar.set)

    sitings_filldata(tvSitings)

    main_frame.protocol("WM_DELETE_WINDOW",on_closing)

    update_clock()

    # return sf


