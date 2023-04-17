# Marathon Manager
#
# Main Window Manager
#

from tkinter import *
from tkinter import ttk

from checkpoints import *
from courses import *
# from database import *
from events import *
from sitings import *
from participants import *
from volunteers import *
from reports import *
# from database import MMDatabase as DB
from constants import *
import os.path
from functools import partial


class StatusBar(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.label = tk.Label(self, text='Using: No Database Open', bd=1, relief=SUNKEN)
        self.label.grid(row=0,column=0,columnspan=5,sticky=W+E, padx=5, pady=8)

    def set(self, newText):
        self.label.config(text=newText)

    def clear(self):
        self.label.config(text='')

class MainWindow:

    def __init__(self):
        self.root = Tk()
        self.root.title("Marathon Manager")
        self.root.geometry('450x225')
        self.root.minsize(400,100)
        self.db = None

        # Label(self.root,text="Hello").pack()

        # Main Menu Bar
        menubar = self.mainmenubar(self.root)
        self.root.config(menu=menubar)


        # Quick Buttons
        btnSitings = ttk.Button(self.root,text="Sitings",command=self.open_sitings)
        btnSitings.grid(row=1,column=0,padx=10,pady=10,sticky='news')

        btnParticipants = ttk.Button(self.root,text="Participants",command=self.participants_click)
        btnParticipants.grid(row=2,column=0,padx=10,pady=10,sticky='news')

        btnVolunteers = ttk.Button(self.root,text="Volunteers",command=self.open_volunteers)
        btnVolunteers.grid(row=3,column=0,padx=10,pady=10,sticky='news')

        btnReports = ttk.Button(self.root,text="Reports",command=self.open_reports)
        btnReports.grid(row=4,column=0,padx=10,pady=10,sticky='news')

        self.status = StatusBar(self.root)
        self.status.grid(row=10,column=0)

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



        self.root.mainloop()

    # =============================================================================
    #  Main Menu Bar
    # =============================================================================
    def mainmenubar(self,main_frame: Frame) -> Frame:
        """Main Menu Bar"""
        mmb = Menu(main_frame)


        filemenu = Menu(mmb, tearoff=0)
        filemenu.add_command(label="New", command=self.new_click)
        filemenu.add_separator()
        filemenu.add_command(label="Open", command=self.open_click)
        filemenu.add_command(label="Close", command=self.donothing)
        filemenu.add_separator()
        # History
        # TODO iterate through the history file and add menu options for the most recent 3
        history = []
        if os.path.exists('histfile.mm'):
            with open('histfile.mm','r') as f:
                history = [(line) for line in f.read().split('\n')]
                for i,h in enumerate(history):
                    if h:
                        hname,hpath = h.split(",")
                        filemenu.add_command(label=hname, command=partial(self.history_click, i))

        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.exit_app)
        mmb.add_cascade(label="File", menu=filemenu) 

        eventmenu = Menu(mmb, tearoff=0)
        eventmenu.add_command(label="Edit Event", command=self.event_click)
        eventmenu.add_separator()
        eventmenu.add_command(label="Checkpoints", command=self.checkpoints_click)
        eventmenu.add_command(label="Courses", command=self.courses_click)
        eventmenu.add_separator()
        eventmenu.add_command(label="Participants", command=self.participants_click)
        mmb.add_cascade(label="Event", menu=eventmenu)

        helpmenu = Menu(mmb, tearoff=0)
        helpmenu.add_command(label="Help Index", command=self.donothing)
        helpmenu.add_command(label="About...", command=self.donothing)
        mmb.add_cascade(label="Help", menu=helpmenu)

        return mmb

    def donothing(self):
        pass

    def new_database(self):
        # display form to collect event information
        # specify a path/name for the database
        # create it
        # open it
        pass


    def new_click(self):
        root = tk.Toplevel()
        ew = EventsWindow(root)
        ew.clear_fields()
        ew.change_id('0')
        ew.butSave.config(text='Create')
        ew.txtEventName.focus_set()
    
    def open_click(self):
        filetypes = (('database files','*.db'),('All files','*.*'))
        dbPath = filedialog.askopenfilename(title='MM: Open Database',filetypes=filetypes)
        if dbPath:
            DB.init_db(dbPath)
            self.status.set('Using: ' + dbPath)
        self.update_history(dbPath)


    def history_click(self,idx):
        out = []
        if os.path.exists('histfile.mm'):
            with open('histfile.mm','r') as f:
                out = [(line) for line in f.read().split('\n')]
            
                hname,hpath = out[idx].split(",")
                DB.init_db(hpath)
                self.status.set('Using: ' + hpath)


    def update_history(self,filepath):
        # read current history file into nested list
        # open the filepath db and read the event name
        # insert the event name and filepath in pos 0 of history list
        # write the first 3 items back to the history file
        out = []
        if os.path.exists('histfile.mm'):
            with open('histfile.mm','r') as f:
                out = [(line) for line in f.read().split('\n')]

        res = DB.query('select EventName from Events')
        eventname = res[0]['EventName']

        out.insert(0,f'{eventname},{filepath}')
        with open('histfile.mm','w') as f:
            for e in out[:3]:
                f.writelines(e + '\n')
        f.close()


    def event_click(self):
        root = tk.Toplevel()
        ew = EventsWindow(root)

    def checkpoints_click(self):
        root = tk.Tk()
        root.title("MM: Checkpoints")
        root.geometry('700x340')
        ew = checkpoint_window(root)

    def courses_click(self):
        root = tk.Tk()
        root.title("MM: Courses")
        root.geometry('735x380')
        ew = courses_window(root)

    def participants_click(self):
        root = tk.Toplevel()
        pw = ParticipantsWindow(root)


    def open_sitings(self):
        sitings = Tk()
        sitings.title("MM: Sitings")
        sitings.geometry('600x320')
        sw = siting_window(sitings)
        # sitings.grid(row=0,column=1,sticky='n')

    def open_reports(self):
        root = Tk()
        root.title("MM: Reports")
        root.geometry('525x340')
        # ew = checkpoint_window(root)
        show_report(root)

        
    def open_log(self):
        pass

    def open_volunteers(self):
        root = tk.Toplevel()
        vw = VolunteersWindow(root)


    def open_messages(self):
        pass

    def exit_app(self):
        self.root.quit()


# def main():
#     m = MainWindow()

# main()
