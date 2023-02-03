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
        stmt = """select Path from Courses where CourseID=?"""
        cur.execute(stmt,courseid)
        course_path = cur.fetchone()

        # Convert the checkpoints to courseid's (for convenience)
        path_by_id = []
        checkpoints = course_path.split(",").strip()
        for cp in checkpoints:
            stmt = """select CourseID from Courses where CourseName=?;"""
            cur.execute(stmt,cp)
            cpid = cur.fetchone()
            path_by_id.append(cpid)

        # Get a list of participants assigned to this course
        # TODO How do I deal with bibs that were added adhoc -- that are not assigned to a course?
        stmt = """select ParticipantID from Participants where CourseID=?;"""
        cur.execute(stmt,courseid)
        pids = cur.fetchall()

        # Iterate through the participants and the paths to determine which is the furtherest first
        for part in pids:
            p = part[0]
            # perform a query of the first time p arrived at each checkpoint order by time
            # TODO What if it is a circular course; One checkpoint and the participants repeatedly pass it; this query would only return the first time they visited the CP
            




        for row in rows:
            tv.insert("",tk.END,values=row)
        


# this gets the lead runner as long as there has only been one visit -- it gets the first visit; not the last visit
# select ParticipantID,CheckpointID,Sitingtime from Sitings where CheckpointID=4 and Sitingtime = (select min(Sitingtime) from Sitings where CheckpointID=4);
# need to modify this statement to only consider the minimum times of the last visit of each participant

# This statements gets all of the last visits from a checkpoint.
# select ParticipantID, max(Sitingtime) from Sitings where CheckpointID=2 group by ParticipantID;