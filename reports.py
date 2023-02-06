# Marathon Manager - Reports
#
#
# Generate reports for:
#   lead runner (for each course)
#   last runner (for each course)
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

        cn = sqlite3.connect(DB_NAME)
        cur = cn.cursor()

        # Get the path for this courseid
        stmt = "select Path from Courses where CourseID=?"
        cur.execute(stmt,[courseid])
        course_path = cur.fetchone()

        # Convert the checkpoints to checkpoint ID's (for convenience)
        path_by_id = []
        checkpoints = course_path[0].split(",")
        for cp in checkpoints:
            stmt = "select CheckpointID from Checkpoints where CPName=?;"
            cur.execute(stmt,[cp])
            cpid = cur.fetchone()
            path_by_id.append(cpid[0])
        print(path_by_id)

        # Reverse the path (we want to test from the finish back...but ignore the finish)
        reverse_path = path_by_id[::-1]
        print(reverse_path)
        paths_to_test = reverse_path[1:]
        print(paths_to_test)

       
        # Iterate through each checkpoint in reverse order
        # Get a list of the last visit by each participant
        # Determine who got there first (earliest time)
        # If the earliest runner is after what is stored in the lead_runner variable, replace the lead_runner
        lead_runner = {}    # {'ParticipantID': x, 'Arrival_Time': y}
        for cp in paths_to_test:
            lead_at_cp = {}
            stmt = "select ParticipantID, max(Sitingtime) from Sitings where CheckpointID=? group by ParticipantID;"
            cur.execute(stmt,[cp])
            participants = cur.fetchall()
            for p in participants:
                if len(lead_at_cp) == 0:
                    lead_at_cp["ParticipantID"] = p[0]
                    lead_at_cp["Arrival_Time"] = p[1]
                elif p[1] < lead_at_cp["Arrival_Time"]:
                    lead_at_cp.update({"ParticipantID": p[0]})
                    lead_at_cp.update({"Arrival_Time": p[1]})
            
            if len(lead_at_cp) > 0:
                if len(lead_runner) == 0:
                    # lead_runner["ParticipantID"] = lead_at_cp["ParticipantID"]
                    # lead_runner["Arrival_Time"] = lead_at_cp["Arrival_Time"]
                    lead_runner = lead_at_cp.copy()
                elif lead_at_cp["Arrival_Time"] > lead_runner["Arrival_Time"]:
                    lead_runner.update({"ParticipantID": lead_at_cp["ParticipantID"]})
                    lead_runner.update({"Arrival_Time": lead_at_cp["Arrival_Time"]})

        print(lead_runner)


# TODO ===========================================================
# As this function stands, it finds the lead_runner is:
#   {'ParticipantID': 5, 'Arrival_Time': '2023-02-03 11:40'}
# Does this match with the example on the whiteboard
# TODO ===========================================================

        


# this gets the lead runner as long as there has only been one visit -- it gets the first visit; not the last visit
# select ParticipantID,CheckpointID,Sitingtime from Sitings where CheckpointID=4 and Sitingtime = (select min(Sitingtime) from Sitings where CheckpointID=4);
# need to modify this statement to only consider the minimum times of the last visit of each participant

# This statements gets all of the last visits from a checkpoint.
# select ParticipantID, max(Sitingtime) from Sitings where CheckpointID=2 group by ParticipantID;

def show_report():
    r = Reports()
    r.lead_runner(4)    # find the lead runner for courseID 4 (30K)