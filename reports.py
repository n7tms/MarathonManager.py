# Marathon Manager - Reports
#
#
# Generate reports for:
#   lead runner (for each course, including unknowns)
#   last runner (for each course, including unknowns)
#   list of DNS
#   list of DNF
#   list of overdue runners (bib, name, phone, econtact, last checkpoint, elapsed time since last seen, next checkpoint)

from constants import *
from tkinter import *
from tkinter import ttk

class Reports:

    def __init__(self):
        pass

    def lead_runner(self, courseid):
        """determine the lead runner for each course"""

        # A list of courses (5K, 10K, Half, etc.) will be generated elsewhere.
        # This function returns the leader for the courseID specified in the arguments
        #
        # get the path
        # leader = ""
        # for each participant assigned to that course
        #   if participant.checkpoint > leader's
        #       set leader = this participant
        #   elif particpant.checkpoint == leader's and particpant.arrivaltime < leaders
        #       set leader = this participant
        # return leader

        # Get the path for this courseid
        stmt = "select CheckpointID from Paths where CourseID=? order by CPOrder ASC"
        course_path = DB.query(stmt,[courseid])

        # Convert the checkpoints to checkpoint ID's (for convenience)
        path_by_id = []
        for cp in course_path:
            path_by_id.append(cp[0])
        print(path_by_id)
        paths_to_test = path_by_id[:-1] # remove the finish

        # Reverse the path (we want to test from the finish back...but ignore the finish)
        # reverse_path = path_by_id[::-1]
        # print(reverse_path)
        # paths_to_test = reverse_path[1:]
        # print(paths_to_test)

       
        # Iterate through each checkpoint in reverse order
        # Get a list of the last visit by each participant
        # Determine who got there first (earliest time)
        # If the earliest runner is after what is stored in the lead_runner variable, replace the lead_runner
        lead_runner = {}    # {'ParticipantID': x, 'Arrival_Time': y}
        for cp in paths_to_test:
            lead_at_cp = {}
            stmt = "select s.ParticipantID, max(s.Sitingtime) from Sitings s inner join Participants p on s.ParticipantID = p.ParticipantID where s.CheckpointID=? and p.CourseID=? group by s.ParticipantID;"
            participants = DB.query(stmt,[cp,courseid])
            for p in participants:
                if len(lead_at_cp) == 0:
                    lead_at_cp["ParticipantID"] = p[0]
                    lead_at_cp["Arrival_Time"] = p[1]
                    lead_at_cp["Checkpoint"] = cp
                elif p[1] < lead_at_cp["Arrival_Time"]:
                    lead_at_cp.update({"ParticipantID": p[0]})
                    lead_at_cp.update({"Arrival_Time": p[1]})
                    lead_at_cp.update({"Checkpoint": cp})
            
            if len(lead_at_cp) > 0:
                if len(lead_runner) == 0:
                    # lead_runner["ParticipantID"] = lead_at_cp["ParticipantID"]
                    # lead_runner["Arrival_Time"] = lead_at_cp["Arrival_Time"]
                    lead_runner = lead_at_cp.copy()
                elif lead_at_cp["Arrival_Time"] > lead_runner["Arrival_Time"]:
                    lead_runner.update({"ParticipantID": lead_at_cp["ParticipantID"]})
                    lead_runner.update({"Arrival_Time": lead_at_cp["Arrival_Time"]})
                    lead_runner.update({"Checkpoint": lead_at_cp["Checkpoint"]})

        print("Lead:", lead_runner)

        
    def last_runner(self, courseid):
        """determine the last runner for each course"""

        # A list of courses (5K, 10K, Half, etc.) will be generated elsewhere.
        # This function returns the leader for the courseID specified in the arguments
        #
        # get the path
        # leader = ""
        # for each participant assigned to that course
        #   if participant.checkpoint > leader's
        #       set leader = this participant
        #   elif particpant.checkpoint == leader's and particpant.arrivaltime < leaders
        #       set leader = this participant
        # return leader

        # Get the path for this courseid
        stmt = "select CheckpointID from Paths where CourseID=? order by CPOrder ASC"
        course_path = DB.query(stmt,[courseid])

        # Convert the checkpoints to checkpoint ID's (for convenience)
        path_by_id = []
        for cp in course_path:
            path_by_id.append(cp[0])
        print(path_by_id)
        paths_to_test = path_by_id[:-1] # remove the finish

        # Reverse the path (we want to test from the finish back...but ignore the finish)
        # reverse_path = path_by_id[::-1]
        # print(reverse_path)
        # paths_to_test = reverse_path[1:]
        # print(paths_to_test)

       
        # Iterate through each checkpoint in reverse order
        # Get a list of the last visit by each participant
        # Determine who got there first (earliest time)
        # If the earliest runner is after what is stored in the lead_runner variable, replace the lead_runner
        last_runner = {}    # {'ParticipantID': x, 'Arrival_Time': y}
        for cp in paths_to_test:
            last_at_cp = {}
            stmt = "select s.ParticipantID, max(s.Sitingtime) from Sitings s inner join Participants p on s.ParticipantID = p.ParticipantID where s.CheckpointID=? and p.CourseID=? group by s.ParticipantID;"
            participants = DB.query(stmt,[cp,courseid])
            for p in participants:
                if len(last_at_cp) == 0:
                    last_at_cp["ParticipantID"] = p[0]
                    last_at_cp["Arrival_Time"] = p[1]
                    last_at_cp["Checkpoint"] = cp
                elif p[1] < last_at_cp["Arrival_Time"]:
                    last_at_cp.update({"ParticipantID": p[0]})
                    last_at_cp.update({"Arrival_Time": p[1]})
                    last_at_cp.update({"Checkpoint": cp})
            
            if len(last_at_cp) > 0:
                if len(last_runner) == 0:
                    last_runner = last_at_cp.copy()
                elif last_at_cp["Arrival_Time"] < last_runner["Arrival_Time"]:
                    last_runner.update({"ParticipantID": last_at_cp["ParticipantID"]})
                    last_runner.update({"Arrival_Time": last_at_cp["Arrival_Time"]})
                    last_runner.update({"Checkpoint": last_at_cp["Checkpoint"]})

        print("Last:", last_runner)

        
    def location_all_runners(self,cid: int) -> None:
        stmt = """Select s.ParticipantID, FirstName, LastName, Bib, SitingTime, s.CheckpointID cp, c.CPName cn, c.Description cd 
        FROM Sitings s, Participants p, Checkpoints c 
        WHERE s.ParticipantID=p.ParticipantID AND s.CheckpointID=c.CheckpointID AND s.SitingTime = (select max(s2.SitingTime) from Sitings s2  where s2.ParticipantID = s.ParticipantID and CourseID=?) 
        ORDER BY s.CheckpointID ASC, s.SitingTime ASC;"""
        results = DB.query(stmt,[cid])
        
        return results

    
class the_view:

    def __init__(self,parent) -> None:
        self.parent_frame = parent

        self.tv = ttk.Treeview(self.parent_frame)
        self.tv['columns'] = ('Participant','Bib','Checkpoint','Time')
        self.tv.column("#0",width=0, stretch="NO")
        self.tv.column("Participant",anchor="w",width=160)
        self.tv.column("Bib",anchor="w",width=60)
        self.tv.column("Checkpoint",anchor="w",width=100)
        self.tv.column("Time",anchor="w",width=160)

        self.tv.heading("#0",text="",anchor="w")
        self.tv.heading("Participant",text="Participant",anchor="w")
        self.tv.heading("Bib",text="Bib",anchor="w")
        self.tv.heading("Checkpoint",text="Checkpoint",anchor="w")
        self.tv.heading("Time",text="Time",anchor="w")

        self.tv.pack()

            

def show_report(win):
    r = Reports()
    nb = ttk.Notebook(win)

    # r.lead_runner(1)    # find the lead runner for courseID 4 (30K)
    # r.last_runner(1)

    # get a list of all of the course in this event
    stmt = """Select CourseID, CourseName, Color FROM Courses"""
    courses = DB.query(stmt)

    # interate through all courses
    for i,course in enumerate(courses):
        # Create a tab for a course
        newtab = Frame(nb)
        ttk.Label(newtab,text='Course: ' + course["CourseName"],width=50).pack()

        # query the database for runners in this course
        # {'CourseID': 7, 'CourseName': '12K', 'Color': '#4f53f2'}
        results = r.location_all_runners(course["CourseID"])

        # Display the results on this tab
        v = the_view(newtab)
        for res in results:
            row = [res['Firstname'] + ' ' + res['Lastname'],res['Bib'],res['cn'],res['SitingTime']]
            v.tv.insert("",'end',values=row)

        # add THIS tab to the notebook
        nb.add(newtab,text=course["CourseName"])

    # pack the whole notebook
    nb.pack(expand=True,fill='both')
