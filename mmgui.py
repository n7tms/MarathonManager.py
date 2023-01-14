# Marathon Manager GUI objects
# mmgui.py

# https://www.studytonight.com/tkinter/python-tkinter-geometry-manager
# use a grid() geometry manager
# python tkinter widgets: https://www.studytonight.com/tkinter/python-tkinter-widgets
# Good tutorial/doc: https://python-textbok.readthedocs.io/en/1.0/Introduction_to_GUI_Programming.html
# Good walkthru: https://www.youtube.com/watch?v=ibf5cx221hk


# import tkinter as tk
from tkinter import ttk, Label, Entry, Button, END
from datetime import datetime
import re
import sqlite3

class SitingWindow:
    """The windows used to enter sitings."""

    db = 'mm_test.db'
    cn,cur = None,None
    checkpoints = []


    def __init__(self, master) -> None:
        self.master = master
        master.title("MM4: Sitings")

        master.geometry("575x150")


        self.cn = sqlite3.connect(self.db)
        self.cur = self.cn.cursor()

        self.lblTime = Label(master,width=10)
        self.lblTime.grid(row=0,column=0,sticky='W', padx=2, pady=2)

        self.cmbCheckpoint = ttk.Combobox(master,width=10,values=self.get_checkpoints())
        self.cmbCheckpoint.grid(row=0,column=1,sticky='W',  padx=2, pady=2)
        self.cmbCheckpoint.set(self.checkpoints[0][1])

        self.txtBibs = Entry(master,width=30)
        self.txtBibs.grid(row=0,column=2,sticky='W',  padx=2, pady=2)
        self.txtBibs.bind("<KeyPress>", self.bib_enterkey)

        self.butSubmit = Button(master,text='Submit',width=10,command=self.submit_bibs)
        self.butSubmit.grid(row=0,column=3,sticky='W',  padx=2, pady=2)

        self.lblStatus = Label(master,text='this is where the status goes')
        self.lblStatus.grid(row=1,column=0,columnspan=3,padx=10,pady=2)


        # self.update_clock()



    def get_checkpoints(self) -> list:
        """return a list of checkpoints"""
        if len(self.checkpoints) > 0:
            self.checkpoints.clear()

        res = self.cur.execute("select CheckpointID,CPName from Checkpoints")
        for x in res:
            self.checkpoints.append(x)
        
        cps = []
        for x in self.checkpoints:
            cps.append(x[1])
        return cps

    def bib_enterkey(self, event):
        """Check if the Enter key was pressed from inside the bib text field"""
        if event.keysym == 'Return' or event.keysym == 'KP_Enter':
            self.submit_bibs()

    def update_status(self,message):
        """set the value of the status label"""
        self.lblStatus.configure(text=message)

    def validate_fields(self) -> bool:
        """make sure the checkpoint and bibs fields are valid"""
        return True

    def submit_bibs(self):
        if self.validate_fields():
            bibs = re.split(r',| |\.|\+',self.txtBibs.get())
            count = len(bibs)

            # Get the checkpoint ID
            cid = -1
            for c in self.checkpoints:
                if c[1] == self.cmbCheckpoint.get():
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
                res = self.cur.execute(stmt)
                if res.rowcount < 0:
                    # add the bib
                    stmt = "insert into Participants (EventID,RaceID,Bib) values (1,0," + b + ");"
                    self.cur.execute(stmt)
                    self.cn.commit()

                # get the participantID belonging to this bib
                stmt = "select PersonID from Participants where Bib=" + b + ";"
                res = self.cur.execute(stmt)
                partID = list(res)[0][0]

                # add the siting to the sitings table
                stmt = "insert into Sitings (EventID, CheckpointID, ParticipantID, Sitingtime) values (1," + str(cid) + "," + str(partID) + ",'" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "');"
                res = self.cur.execute(stmt)
                self.cn.commit()

            status = str(count) + " bibs submitted Successfully at " + datetime.now().strftime("%H:%M:%S")
            self.update_status(status)
            self.txtBibs.delete(0,END)
        else:
            self.update_status("Problem. Check checkpoints or bibs.")

    def update_clock(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        self.lblTime.configure(text=current_time)
        self.master.after(1000, self.update_clock)
