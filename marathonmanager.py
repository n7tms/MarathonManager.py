# Marathon Manager v4.0
# marathonmanager.py

# This is an attempt to create a cross-platform instance of previous versions of
# the Marathon Manager and MarathonLog.

# Design Doc:       https://docs.google.com/document/d/1VVr96XDRAQdNaRYn9vpivIfoGgfj0RA9UhD9_bLc_cM/edit#heading=h.ik9a8ixasni9
# Requirements Doc: https://docs.google.com/document/d/1BqDi_qj6UHPEp5H2pAipckIPRC01c_GxmwDunDiP-oE/edit#
#
# =============================================================================
# Imports
import random
import sqlite3
from pathlib import Path
import mmgui
from tkinter import Tk


# =============================================================================
# Constants
DB_NAME = 'mm_test.db'


# =============================================================================
# Function Definitions
#
def database_exists(db_name: str) -> bool:
    """Test if the specified database file exists."""
    path = Path(db_name)
    if path.is_file():
        return True
    else:
        return False

def create_database(db_name: str) -> bool:
    """Create the initial Marathon Manager database and populate it with some
    global data."""
    pass







# =============================================================================
# Main
# 
if __name__ == "__main__":
    print(database_exists(DB_NAME))

    root = Tk()
    sg = mmgui.SitingWindow(root)
    root.mainloop()

