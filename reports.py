# Marathon Manager - Reports
#
#
# Generate reports for:
#   lead runner (for each course)
#   last runner (for each course)
#   list of DNS
#   list of DNF
#   list of overdue runners (bib, name, phone, econtact, last checkpoint, elapsed time since last seen, next checkpoint)

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

