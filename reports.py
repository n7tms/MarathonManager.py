# Marathon Manager - Reports
#
#
# Generate reports for:
#   lead runner (for each course, including unknowns)
#   last runner (for each course, including unknowns)
#   list of DNS
#   list of DNF
#   list of overdue runners (bib, name, phone, econtact, last checkpoint, elapsed time since last seen, next checkpoint)

import sqlite3
from constants import *

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
        cur.execute(stmt,[courseid])
        course_path = cur.fetchall()

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
            cur.execute(stmt,[cp,courseid])
            participants = cur.fetchall()
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
        cur.execute(stmt,[courseid])
        course_path = cur.fetchall()

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
            cur.execute(stmt,[cp,courseid])
            participants = cur.fetchall()
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

        




def show_report():
    r = Reports()
    r.lead_runner(1)    # find the lead runner for courseID 4 (30K)
    r.last_runner(1)