# Marathon Manager - Events Window

import sqlite3
from tkinter import ttk, filedialog
import tkinter as tk
from tkinter.messagebox import showerror
from constants import *
import datetime

class EventsWindow:

    def __init__(self,master):

        # self.root = tk.Tk()
        self.master = master

        self.root = tk.Frame(master)
        self.root.pack()

        master.title("MM: Events")
        master.geometry('450x200')
        master.minsize(400,100)


        # img2 = ImageTk.PhotoImage(file='runner_blue.png')
        # imgLogo = ttk.Label(main_frame,image=img2)
        self.imgLogo = ttk.Label(self.root,text="logo placeholder")
        self.imgLogo.grid(row=0,column=0,rowspan=5)

        # self.lblID = ttk.Label(self.root,width=10)
        # self.lblID.grid(row=0,column=1, columnspan=2,sticky='w')
        # self.lblID.grid_remove()

        self.lblEventName = ttk.Label(self.root,text='Event Name:',width=12)
        self.lblEventName.grid(row=1,column=1,sticky='e', padx=5, pady=8)
        self.txtEventName = ttk.Entry(self.root,width=25)
        self.txtEventName.grid(row=1,column=2, columnspan=2,sticky='w')

        self.lblDescription = ttk.Label(self.root,text='Description:',width=12)
        self.lblDescription.grid(row=2,column=1,sticky='e',padx=5, pady=8)
        self.txtDescription = tk.Entry(self.root,width=25)
        self.txtDescription.grid(row=2,column=2, columnspan=2,sticky='w',padx=5, pady=8)

        self.lblLocation = ttk.Label(self.root,text='Location:',width=12)
        self.lblLocation.grid(row=3,column=1,sticky='e')
        self.txtLocation = tk.Entry(self.root,width=10)
        self.txtLocation.grid(row=3,column=2,sticky='w')

        self.lblStartDate = ttk.Label(self.root,text='Start Date:',width=12)
        self.lblStartDate.grid(row=4,column=1,sticky='e')
        self.txtStartDate = tk.Entry(self.root,width=10)
        self.txtStartDate.grid(row=4,column=2,sticky='w')

        self.lblStartTime = ttk.Label(self.root,text='Start Time:',width=12)
        self.lblStartTime.grid(row=5,column=1,sticky='e')
        self.txtStartTime = tk.Entry(self.root,width=10)
        self.txtStartTime.grid(row=5,column=2,sticky='w')

        self.butSave = ttk.Button(self.root,text='Save',command=self.event_save)
        self.butSave.grid(row=3,column=3)
        self.butCancel = ttk.Button(self.root,text='Cancel',command=self.event_cancel)
        self.butCancel.grid(row=4,column=3)

        self.lblID = ttk.Label(self.root,width=10,text='0')
        self.lblID.grid(row=5,column=3)
        # self.lblID.grid_remove()


        self.event_load()

        

    def change_id(self,newText):
        self.lblID.config(text=newText)
    
    def clear_fields(self):
        self.txtEventName.delete(0,tk.END)
        self.txtDescription.delete(0,tk.END)
        self.txtLocation.delete(0,tk.END)
        self.txtStartDate.delete(0,tk.END)
        self.txtStartTime.delete(0,tk.END)

    def event_load(self):
        """Load the field values from the database"""

        def set_text(tw: tk.Entry, text: str):
            tw.delete(0,'end')
            tw.insert(0,text)

        stmt = "select EventID, EventName, Description, Location, Starttime from Events;"
        res = DB.query(stmt)

        if res[0]['Starttime']:
            sd,st = res[0]['Starttime'].split(' ')
        else:
            sd,st = '',''

        # put the data into the fields
        if res[0]['EventID']:
            self.lblID.config(text=res[0]['EventID'])
        
        if res[0]['EventName']:
            set_text(self.txtEventName,res[0]['EventName'])

        if res[0]['Description']:
            set_text(self.txtDescription,res[0]['Description'])

        if res[0]['Location']:
            set_text(self.txtLocation,res[0]['Location'])
        
        set_text(self.txtStartDate,sd)
        set_text(self.txtStartTime,st)
        

    def event_save(self):
        # get the field values
        eID = self.lblID['text']
        eName = self.txtEventName.get()
        eDescription = self.txtDescription.get()
        eLocation = self.txtLocation.get()
        eDate = self.txtStartDate.get()
        eTime = self.txtStartTime.get()
        eStart = eDate + ' ' + eTime

        # conduct some error checking for valid value formats
        sError = '' 
        if len(eName.strip()) < 1:
            sError += 'Event Name cannot be blank.\n'
        
        date_format = '%Y-%m-%d'
        time_format = '%H:%M'
        try:
            eDate = datetime.datetime.strptime(eDate,date_format)
        except ValueError:
            sError += 'Start date must be a valid date (yyyy-mm-dd).'
        
        try:
            eTime = datetime.datetime.strptime(eTime,time_format)
        except ValueError:
            sError += 'Start time must be a valid time (HH:MM).'
        
        if sError:
            sError = 'Values in one or more fields needs attention.\n\n' + sError
            showerror(title='MM: Error',message=sError)

        elif eID == '0':    # Create a new event
            # ask for a path for the new database
            filetypes = (('database files','*.db'),('All files','*.*'))
            dbPath = filedialog.asksaveasfilename(title='New Database Path/Name',filetypes=filetypes)
            
            # create the database (and tables)
            DB.init_db(dbPath)
            if not DB.create_database():
                showerror(title='MM: Error',message='An error occurred while creating the database.')
            else:
                # insert this event information
                DB.nonQuery("""INSERT INTO Events (EventName, Description, Location, Starttime) VALUES (?,?,?,?)""",[eName,eDescription,eLocation,eStart])

                self.master.destroy()

        else:               # Update existing event
            stmt = "update Events set EventName=?,Description=?,Location=?,Starttime=? where EventID=?"
            DB.nonQuery(stmt,[eName,eDescription,eLocation,eStart,eID])
            self.master.destroy()

    def event_cancel(self):
        self.master.destroy()



