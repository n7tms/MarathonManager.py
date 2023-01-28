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



def import_filldata(tv:ttk.Treeview,data:list) -> None:
    """Clear and then fill/refresh the Checkpoints table with data"""
    # clear the table
    for item in tv.get_children():
        tv.delete(item)

    for row in data:
        tv.insert("",tk.END,values=row)

def import_import():
    pass

def import_edit_row():
    pass

def import_cancel():
    pass

def import_read(lbl:tk.Label, tv:ttk.Treeview) -> None:
    out = []

    filename = filedialog.askopenfilename(title="MM: Select File to Import",filetypes=(("csv","*.csv"),("txt","*.txt"),("All Files","*.*")))
    lbl.config(text=filename)
    print(filename)

    with open(filename,'r', encoding="utf8", errors="surrogateescape") as f:
        line = f.readline()
        while line:
            x = line.split(',')
            out.append(x)
            line = f.readline()
    
    # Assign indices to headers
    # distance,First Name,Last Name,gender,Age,DOB,Email,Address,City,State,Zip,Country,Phone,Bib,emergency_name,emergency_phone
    # idistance,ifirst,ilast,igender,iage,idob,iemail,iaddress,icity,istate,izip,icountry,iphone,ibib,iename,iephone = list([None] * 16)
    # for i,h in enumerate(out[0].split(',')):
    #     match h:
    #         case "distance": idistance = i
    #         case "First Name": ifirst = i
    #         case "Last Name": ilast = i
    #         case "gender": igender = i
    #         case "Age": iage = i
    #         case "DOB": idob = i
    #         case "Email": iemail = i
    #         case "Address": iaddress = i
    #         case "City": iaddress = i
    #         case "State": istate = i
    #         case "Zip": izip = i
    #         case "Country": icountry = i
    #         case "Phone": iphone = i
    #         case "Bib": ibib = i
    #         case "emergency_name": iename = i
            # case "emergency_phone": iephone = i

    h_index = {}
    for i,h in enumerate(out[0].split(',')):
        match h:
            case "distance": h_index["Course"] = i
            case "First Name": h_index["First"] = i
            case "Last Name": h_index["Last"] = i
            case "gender": h_index["Gender"] = i
            case "Age": h_index["Age"] = i
            case "DOB": h_index["Birthdate"] = i
            case "Email": h_index["Email"] = i
            case "Address": h_index["Street1"] = i
            case "City": h_index["City"] = i
            case "State": h_index["State"] = i
            case "Zip": h_index["Zipcode"] = i
            case "Country": h_index["Country"] = i
            case "Phone": h_index["Phone"] = i
            case "Bib": h_index["Bib"] = i
            case "emergency_name": h_index["eName"] = i
            case "emergency_phone": h_index["ePhone"] = i

# id, course, bib, first, last, gender, age, email, phone, birthday, address, city, state, zip, country, ename, ephone

    # normalize the data (put it in the correct order)
    normalized_data = []
    for row in out[1:]:
        x = row.split(',')
        for j,a in enumerate(x):
            

    
    import_filldata(tv,out)

    



def import_window(main_frame:tk.Frame) -> tk.Frame:

    title = ttk.Label(main_frame,text='Participant Import',font=('Arial',18))
    title.grid(row=0,column=0,columnspan=2,sticky='nw')

    lblLogo = ttk.Label(main_frame,text="Logo Placeholder")
    lblLogo.grid(row=0,column=2,rowspan=2,sticky='news')

    btnRead = ttk.Button(main_frame,text="Read File",command=lambda: import_read(lblFile,tvImport))
    btnRead.grid(row=2,column=0,padx=5,pady=5,sticky='w')

    lblFile = ttk.Label(main_frame,text="<file name>")
    lblFile.grid(row=3,column=0,columnspan=2,sticky='w')

    tvImport = ttk.Treeview(main_frame,column=("0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16"),show='headings',selectmode='browse')
    
    tvImport.column("0",anchor='center',minwidth=0,width=50)
    tvImport.heading("0",text="ID")
    tvImport.column("1",anchor='center',minwidth=0,width=50)
    tvImport.heading("1",text="Course")
    tvImport.column("2",anchor='w',minwidth=0,width=50)
    tvImport.heading("2",text="Bib",anchor='w')
    tvImport.column("3",anchor='w',minwidth=0,width=50)
    tvImport.heading("3",text="First",anchor='w')
    tvImport.column("4",anchor='w',minwidth=0,width=50)
    tvImport.heading("4",text="Last",anchor='w')
    tvImport.column("5",anchor='w',minwidth=0,width=50)
    tvImport.heading("5",text="Gender",anchor='w')
    tvImport.column("6",anchor='w',minwidth=0,width=50)
    tvImport.heading("6",text="Age",anchor='w')
    tvImport.column("7",anchor='w',minwidth=0,width=50)
    tvImport.heading("7",text="Email",anchor='w')
    tvImport.column("8",anchor='w',minwidth=0,width=50)
    tvImport.heading("8",text="Phone",anchor='w')
    tvImport.column("9",anchor='w',minwidth=0,width=50)
    tvImport.heading("9",text="Birthdate",anchor='w')
    tvImport.column("10",anchor='w',minwidth=0,width=50)
    tvImport.heading("10",text="Address",anchor='w')
    tvImport.column("11",anchor='w',minwidth=0,width=50)
    tvImport.heading("11",text="City",anchor='w')
    tvImport.column("12",anchor='w',minwidth=0,width=50)
    tvImport.heading("12",text="State",anchor='w')
    tvImport.column("13",anchor='w',minwidth=0,width=50)
    tvImport.heading("13",text="Zip",anchor='w')
    tvImport.column("14",anchor='w',minwidth=0,width=50)
    tvImport.heading("14",text="Country",anchor='w')
    tvImport.column("15",anchor='w',minwidth=0,width=50)
    tvImport.heading("15",text="EName",anchor='w')
    tvImport.column("16",anchor='w',minwidth=0,width=50)
    tvImport.heading("16",text="EPhone",anchor='w')

    tvImport.grid(row=4,column=0,columnspan=3,padx=5,pady=5)
    tvImport.bind("<Double-1>",import_edit_row)

    yscrollbar = ttk.Scrollbar(main_frame,orient='vertical',command=tvImport.yview)
    yscrollbar.grid(row=4, column=3,pady=15,sticky='nse')
    yscrollbar.configure(command=tvImport.yview)    
    tvImport.configure(yscrollcommand=yscrollbar.set)

    # import_filldata(tvImport)

    btnCancel = ttk.Button(main_frame,text="Import",command=import_import)
    btnCancel.grid(row=5,column=2,padx=5,pady=5,sticky='w')

    btnCancel = ttk.Button(main_frame,text="Cancel",command=import_cancel)
    btnCancel.grid(row=6,column=3,padx=5,pady=5,sticky='w')

