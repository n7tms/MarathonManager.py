# Marathon Manager
#
# Main Window Manager
#

from tkinter import *
from tkinter import ttk

from checkpoints import *
from courses import *
from database import *
# from events import *
from events import *
from sitings import *
from participants import *
from volunteers import *


class MainWindow:

    def __init__(self):
        self.root = Tk()
        self.root.title("Marathon Manager")
        self.root.geometry('450x200')
        self.root.minsize(400,100)

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
        filemenu.add_command(label="New", command=self.donothing)
        filemenu.add_separator()
        filemenu.add_command(label="Open", command=self.donothing)
        filemenu.add_command(label="Close", command=self.donothing)
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
        pass

    
    def event_click(self):
        root = tk.Toplevel()
        ew = EventsWindow(root)

    def checkpoints_click(self):
        # root = tk.Tk()
        # root.title("MM: Checkpoints")
        # root.geometry('700x340')
        # ew = checkpoint_window(root)
        pass

    def courses_click(self):
        # root = tk.Tk()
        # root.title("MM: Courses")
        # root.geometry('735x380')
        # ew = courses_window(root)
        pass

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
        root.title("MM: Checkpoints")
        root.geometry('825x340')
        ew = checkpoint_window(root)

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
