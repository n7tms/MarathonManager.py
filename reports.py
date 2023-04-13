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
        
        print(results)


class TableOfRunners:
    """A class to create the table(s) used to display the location of the runners."""
    def __init__(self) -> None:
        aframe = ttk.Frame()
    
        pass

    def the_view(self) -> ttk.Frame:
        aframe = ttk.Frame()
        aframe.pack()

        tv = ttk.Treeview(aframe)
        tv['columns'] = ('Participant','Bib','Checkpoint','Time')
        tv.column("#0",width=0, stretch="NO")
        tv.column("Participant",anchor="w",width=80)
        tv.column("Bib",anchor="w",width=50)
        tv.column("Checkpoint",anchor="w",width=80)
        tv.column("Time",anchor="w",width=80)

        tv.heading("#0",text="",anchor="w")
        tv.heading("Participant",text="Participant",anchor="w")
        tv.heading("Bib",text="Bib",anchor="w")
        tv.heading("Time",text="Time",anchor="w")

        tv.pack()

        return aframe
            



def show_report():
    r = Reports()
    # r.lead_runner(1)    # find the lead runner for courseID 4 (30K)
    # r.last_runner(1)

    # get a list of all of the course in this event
    stmt = """Select CourseID, CourseName, Color FROM Courses"""
    courses = DB.query(stmt)
    # interate through all courses
    for course in courses:
        # {'CourseID': 7, 'CourseName': '12K', 'Color': '#4f53f2'}
        r.location_all_runners(course["CourseID"])
