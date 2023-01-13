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
DB_NAME_SETTINGS = 'mmsettings.db'
CONN = None
CUR = None

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

def create_database(db_name: str = None) -> bool:
    """Create the initial Marathon Manager database and populate it with some
    global data."""
    global CONN
    global CUR

    # Users Table
    sStmt = """CREATE TABLE Users (UserID INTEGER, PersonID INTEGER, Username TEXT, Password TEXT, Permission INTEGER)"""
    CUR.execute(sStmt)

    # Volunteers Table
    sStmt = """CREATE TABLE Volunteers (
            VolunteerID	INTEGER UNIQUE,
            PersonID	INTEGER,
            EventID	INTEGER,
            Assignment	TEXT,
            Checkin	TEXT,
            Checkout	TEXT,
            PRIMARY KEY(VolunteerID AUTOINCREMENT)
        )"""
    CUR.execute(sStmt)

    # Participants Table
    sStmt = """CREATE TABLE Participants (
            PersonID	INTEGER UNIQUE,
            EventID	INTEGER,
            RaceID	INTEGER,
            Bib	INTEGER,
            PRIMARY KEY(PersonID AUTOINCREMENT)
        )"""
    CUR.execute(sStmt)

    # Events Table
    sStmt = """CREATE TABLE Events (
            EventID	INTEGER UNIQUE,
            EventName	TEXT,
            Description	TEXT,
            Location	TEXT,
            Starttime	TEXT,
            Endtime	TEXT,
            PublicCode	TEXT UNIQUE,
            PRIMARY KEY(EventID AUTOINCREMENT)
        );"""
    CUR.execute(sStmt)

    # Races Table
    sStmt = """CREATE TABLE Races (
            RaceID	INTEGER UNIQUE,
            EventID	INTEGER,
            RaceName	TEXT,
            Distance	TEXT,
            Color	TEXT,
            PRIMARY KEY(RaceID AUTOINCREMENT)
        );"""
    CUR.execute(sStmt)

    # Checkpoints Table
    sStmt = """CREATE TABLE Checkpoints (
            CheckpointID	INTEGER UNIQUE,
            EventID	INTEGER,
            CPName	TEXT,
            Description	TEXT,
            Longitude	NUMERIC,
            Latitude	NUMERIC,
            PRIMARY KEY(CheckpointID AUTOINCREMENT)
        );"""
    CUR.execute(sStmt)

    # Sitings Table
    sStmt = """CREATE TABLE Sitings (
            SitingID	INTEGER UNIQUE,
            EventID	INTEGER,
            CheckpointID	INTEGER,
            ParticipantID	INTEGER,
            Sitingtime	TEXT,
            PRIMARY KEY(SitingID AUTOINCREMENT)
        );"""
    CUR.execute(sStmt)

    # Traffic Table
    sStmt = """CREATE TABLE Traffic (
            TrafficID	INTEGER UNIQUE,
            EventID	INTEGER,
            Logtime	TEXT,
            Message	TEXT,
            AssignedTo	TEXT,
            CompletedTime	TEXT,
            Status	TEXT,
            PRIMARY KEY(TrafficID AUTOINCREMENT)
        );"""
    CUR.execute(sStmt)

    CONN.commit()


def create_settings_database(db_name: str = None) -> bool:
    sStmt = "CREATE TABLE IF NOT EXISTS Settings (SettingID INTEGER UNIQUE, SettingName TEXT, SettingValue TEXT, PRIMARY KEY(SettingID AUTOINCREMENT))"
    CUR.execute(sStmt)

    sStmt = "CREATE TABLE IF NOT EXISTS Recents (RecentID INTEGER UNIQUE,	EventName TEXT,	DBPath TEXT, PRIMARY KEY(RecentID AUTOINCREMENT))"
    CUR.execute(sStmt)

    # Add the settings fields
    # sStmt = 'INSERT INTO Settings (SettingName, SettingValue) VALUES ("DBVersion","1")'
    CUR.execute("""INSERT INTO Settings (SettingName, SettingValue) VALUES ('DBVersion','1')""")
    CONN.commit()

    # Persons Table
    sStmt = "CREATE TABLE IF NOT EXISTS Persons (PersonID INTEGER UNIQUE, Firstname TEXT, Lastname TEXT, Gender TEXT, Birthdate TEXT, Phone TEXT, Textable INTEGER, Email TEXT, Street1 TEXT, Street2 TEXT, City TEXT, State TEXT, Zipcode TEXT, EContactName TEXT, EContactPhone TEXT, Callsign TEXT, PRIMARY KEY(PersonID AUTOINCREMENT));"
    CUR.execute(sStmt)

    # Local Users Table
    sStmt = "CREATE TABLE IF NOT EXISTS LocalUsers (UserID INTEGER, PersonID INTEGER, Username TEXT, Password TEXT, Permission INTEGER)"
    CUR.execute(sStmt)

    # Add a local admin user
    sStmt = "INSERT INTO LocalUsers (Username, Password, PersonID, Permission) VALUEs ('admin', 'admin', -1, 1)"
    CUR.execute(sStmt)
    CONN.commit()


def initialize():
    global CONN 
    global CUR
    
    # open the database
    # TODO: this needs to be modified to check for valid fields (a db version?)
    if not database_exists(DB_NAME_SETTINGS):
        CONN = sqlite3.connect(DB_NAME_SETTINGS)
        CUR = CONN.cursor()
        create_settings_database()
        CONN.close()

    if not database_exists(DB_NAME):
        CONN = sqlite3.connect(DB_NAME)
        CUR = CONN.cursor()
        create_database()
        CONN.close()

    CONN = sqlite3.connect(DB_NAME)
    CUR = CONN.cursor()
    stmt = "ATTACH DATABASE '" + DB_NAME_SETTINGS + "' AS mmSettings;"
    CUR.execute(stmt)
    CONN.commit()

    # res = CUR.execute("""SELECT SettingValue from Settings WHERE SettingName = 'DBVersion'""")
    stmt = """SELECT * from mmSettings.Settings WHERE SettingName = 'DBVersion'"""
    res = CUR.execute(stmt)
    res.fetchall()
    for x in res:
        print(x)
    # print(list(res))

    stmt = """SELECT * FROM pragma_database_list;"""
    res = CUR.execute(stmt)
    res.fetchall()
    for x in res:
        print(x)

    



        


# =============================================================================
# Main
# 
if __name__ == "__main__":
    initialize()


    root = Tk()
    sg = mmgui.SitingWindow(root)
    root.mainloop()

