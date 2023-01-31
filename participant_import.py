# Marathon Manager
#
# Participant Functions
#
# Description
# Reads the file supplied by the timers and adds runners to the database
#
# Explanation
# This process is looking for the following headers/fields in the file:
# RACE_NAME    (5K, Half Marathon, 10K, Marathon, etc.)
# BIB          (34, 947, 1071, etc.)
# FIRST_NAME   
# LAST_NAME
# GENDER       (F, M)
# RACE_AGE     (21, 33, 56, etc.)
# EMAIL        
# PHONE        (10 digits)

# distance	Firstname	Lastname	gender	Age	DOB	Email	Address	City	State	Zip	Country	Phone	Bib	ename	ephone


import sqlite3
from pathlib import Path
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from constants import *
import csv


class ImportParticipantsWindow():

    def __init__(self,master):

        self.master = master

        self.root = tk.Frame(master)
        self.root.pack()

        master.title("MM: Import Participants")
        master.geometry('1000x600')

        self.cn = sqlite3.connect(DB_NAME)
        self.cur = self.cn.cursor()


        self.title = ttk.Label(self.root,text='Participant Import',font=('Arial',18))
        self.title.grid(row=0,column=0,columnspan=2,sticky='nw')

        self.lblLogo = ttk.Label(self.root,text="Logo Placeholder")
        self.lblLogo.grid(row=0,column=2,rowspan=2,sticky='news')

        self.btnRead = ttk.Button(self.root,text="Read File",command=lambda: self.import_read(self.lblFile,self.tvImport))
        self.btnRead.grid(row=2,column=0,padx=5,pady=5,sticky='w')

        self.lblFile = ttk.Label(self.root,text="<file name>")
        self.lblFile.grid(row=3,column=0,columnspan=2,sticky='w')

        self.tvImport = ttk.Treeview(self.root,column=("0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16"),show='headings',selectmode='browse')
        
        self.tvImport.column("0",anchor='center',minwidth=0,width=50)
        self.tvImport.heading("0",text="ID")
        self.tvImport.column("1",anchor='center',minwidth=0,width=50)
        self.tvImport.heading("1",text="Course")
        self.tvImport.column("2",anchor='w',minwidth=0,width=50)
        self.tvImport.heading("2",text="Bib",anchor='w')
        self.tvImport.column("3",anchor='w',minwidth=0,width=50)
        self.tvImport.heading("3",text="First",anchor='w')
        self.tvImport.column("4",anchor='w',minwidth=0,width=50)
        self.tvImport.heading("4",text="Last",anchor='w')
        self.tvImport.column("5",anchor='w',minwidth=0,width=50)
        self.tvImport.heading("5",text="Gender",anchor='w')
        self.tvImport.column("6",anchor='w',minwidth=0,width=50)
        self.tvImport.heading("6",text="Age",anchor='w')
        self.tvImport.column("7",anchor='w',minwidth=0,width=50)
        self.tvImport.heading("7",text="Email",anchor='w')
        self.tvImport.column("8",anchor='w',minwidth=0,width=50)
        self.tvImport.heading("8",text="Phone",anchor='w')
        self.tvImport.column("9",anchor='w',minwidth=0,width=50)
        self.tvImport.heading("9",text="Birthdate",anchor='w')
        self.tvImport.column("10",anchor='w',minwidth=0,width=50)
        self.tvImport.heading("10",text="Address",anchor='w')
        self.tvImport.column("11",anchor='w',minwidth=0,width=50)
        self.tvImport.heading("11",text="City",anchor='w')
        self.tvImport.column("12",anchor='w',minwidth=0,width=50)
        self.tvImport.heading("12",text="State",anchor='w')
        self.tvImport.column("13",anchor='w',minwidth=0,width=50)
        self.tvImport.heading("13",text="Zip",anchor='w')
        self.tvImport.column("14",anchor='w',minwidth=0,width=50)
        self.tvImport.heading("14",text="Country",anchor='w')
        self.tvImport.column("15",anchor='w',minwidth=0,width=50)
        self.tvImport.heading("15",text="EName",anchor='w')
        self.tvImport.column("16",anchor='w',minwidth=0,width=50)
        self.tvImport.heading("16",text="EPhone",anchor='w')

        self.tvImport.grid(row=4,column=0,columnspan=3,padx=5,pady=5)
        self.tvImport.bind("<Double-1>",self.import_edit_row)

        self.yscrollbar = ttk.Scrollbar(self.root,orient='vertical',command=self.tvImport.yview)
        self.yscrollbar.grid(row=4, column=3,pady=15,sticky='nse')
        self.yscrollbar.configure(command=self.tvImport.yview)    
        self.tvImport.configure(yscrollcommand=self.yscrollbar.set)

        # import_filldata(tvImport)

        self.btnImport = ttk.Button(self.root,text="Import",command=lambda: self.import_import(self.tvImport))
        self.btnImport.grid(row=5,column=2,padx=5,pady=5,sticky='w')

        self.btnCancel = ttk.Button(self.root,text="Cancel",command=self.import_cancel)
        self.btnCancel.grid(row=6,column=3,padx=5,pady=5,sticky='w')

# =============================================


    def import_filldata(self,tv:ttk.Treeview,data:list) -> None:
        """Clear and then fill/refresh the Checkpoints table with data"""
        # clear the table
        for item in tv.get_children():
            tv.delete(item)

        for row in data:
            tv.insert("",tk.END,values=row)


    def import_import(self,tv:ttk.Treeview) -> None:
        """write the data in the treeview to the database"""
        data = []
        for x in tv.get_children():
            print(tv.item(x)['values'][1:])
            data.append(tv.item(x)['values'][1:])

        # Get a list of courseID's into a dictionary for quick reference.
        stmt = """select CourseID, CourseName from Courses;"""
        cn

        for x in data:
            # does the bib already exist? If so, update data
            stmt = """insert into Participants ("""

    

    def import_edit_row(self,tv:ttk.Treeview) -> None:
        """Double-clicking a row fills the fields below. The fields can be changed and then saved back to the treeview."""
        # https://www.youtube.com/watch?v=lKiNlSs_cms
        pass


    def import_read(self,lbl:tk.Label, tv:ttk.Treeview) -> None:
        out = []

        filename = filedialog.askopenfilename(title="MM: Select File to Import",filetypes=(("csv","*.csv"),("txt","*.txt"),("All Files","*.*")))
        lbl.config(text=filename)
        print(filename)

        with open(filename,'r', encoding="utf8", errors="surrogateescape") as f:
            line = f.readline()
            while line:
                x = [ '"{}"'.format(x) for x in list(csv.reader([line], delimiter=','))[0] ]
                y = [z.replace('"','') for z in x]
                out.append(y)
                line = f.readline()
        
        # Assign indices to headers
        # distance,First Name,Last Name,gender,Age,DOB,Email,Address,City,State,Zip,Country,Phone,Bib,emergency_name,emergency_phone

        h_index = [None] * 16
        for i,h in enumerate(out[0]):
            match h:
                case "distance": h_index[0] = i
                case "First Name": h_index[2] = i
                case "Last Name": h_index[3] = i
                case "gender": h_index[4] = i
                case "Age": h_index[5] = i
                case "DOB": h_index[8] = i
                case "Email": h_index[6] = i
                case "Address": h_index[9] = i
                case "City": h_index[10] = i
                case "State": h_index[11] = i
                case "Zip": h_index[12] = i
                case "Country": h_index[13] = i
                case "Phone": h_index[7] = i
                case "Bib": h_index[1] = i
                case "emergency_name": h_index[14] = i
                case "emergency_phone": h_index[15] = i

    # id, course, bib, first, last, gender, age, email, phone, birthday, address, city, state, zip, country, ename, ephone

        # normalize the data (put it in the correct order)
        normalized_data = []
        for i,row in enumerate(out[1:]):
            tmp=[]
            tmp.append(i)
            for j in range(0,len(row)):
                tmp.append(row[h_index[j]])
            normalized_data.append(tmp)
        
        self.import_filldata(tv,normalized_data)

    

    def import_cancel(self):
        self.master.destroy()




