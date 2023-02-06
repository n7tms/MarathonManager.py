# Marathon Manager
#
# Database creation functions
#
#

import sqlite3
from pathlib import Path
from constants import *


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

    # # Users Table
    # sStmt = """CREATE TABLE Users (UserID INTEGER, PersonID INTEGER, Username TEXT, Password TEXT, Permission INTEGER)"""
    # cur.execute(sStmt)

    # Volunteers Table
    sStmt = """CREATE TABLE IF NOT EXISTS Volunteers (
            VolunteerID INTEGER UNIQUE, 
            Firstname TEXT, 
            Lastname TEXT, 
            Gender TEXT, 
            Birthdate TEXT, 
            Phone TEXT, 
            Textable INTEGER, 
            Email TEXT, 
            Street1 TEXT, 
            Street2 TEXT, 
            City TEXT, 
            State TEXT, 
            Zipcode TEXT, 
            EContactName TEXT, 
            EContactPhone TEXT, 
            Callsign TEXT, 
            Username TEXT,
            Password TEXT,
            Permission INTEGER,
            PRIMARY KEY(VolunteerID AUTOINCREMENT)
            );"""
    cur.execute(sStmt)

    # Volunteer Log Table (history of assignments, check-ins and -outs)
    sStmt = """CREATE TABLE IF NOT EXISTS VolLog (
            LogID	INTEGER UNIQUE,
            VolunteerID INTEGER,
            EventID	INTEGER,
            Assignment	TEXT,
            Checkin	TEXT,
            Checkout	TEXT,
            PRIMARY KEY(LogID AUTOINCREMENT)
        )"""
    cur.execute(sStmt)

    # Participants Table
    sStmt = """CREATE TABLE IF NOT EXISTS Participants (
            ParticipantID	INTEGER UNIQUE,
            Firstname TEXT, 
            Lastname TEXT, 
            Gender TEXT, 
            Age INTEGER
            Birthdate TEXT, 
            Phone TEXT, 
            Textable INTEGER, 
            Email TEXT, 
            Street1 TEXT, 
            Street2 TEXT, 
            City TEXT, 
            State TEXT, 
            Zipcode TEXT, 
            Country TEXT,
            EContactName TEXT, 
            EContactPhone TEXT, 
            EventID	INTEGER,
            CourseID INTEGER,
            Bib	INTEGER,
            PRIMARY KEY(ParticipantID AUTOINCREMENT)
        )"""
    cur.execute(sStmt)

    # Events Table
    sStmt = """CREATE TABLE IF NOT EXISTS Events (
            EventID	INTEGER UNIQUE,
            EventName	TEXT,
            Description	TEXT,
            Location	TEXT,
            Starttime	TEXT,
            Endtime	TEXT,
            PublicCode	TEXT UNIQUE,
            PRIMARY KEY(EventID AUTOINCREMENT)
        );"""
    cur.execute(sStmt)

    # Courses Table
    sStmt = """CREATE TABLE IF NOT EXISTS Courses (
            CourseID	INTEGER UNIQUE,
            EventID	INTEGER,
            CourseName	TEXT,
            Distance	TEXT,
            Color	TEXT,
            Path    TEXT,
            PRIMARY KEY(CourseID AUTOINCREMENT)
        );"""
    cur.execute(sStmt)

    # Checkpoints Table
    sStmt = """CREATE TABLE IF NOT EXISTS Checkpoints (
            CheckpointID	INTEGER UNIQUE,
            EventID	INTEGER,
            CPName	TEXT,
            Description	TEXT,
            Longitude	NUMERIC,
            Latitude	NUMERIC,
            PRIMARY KEY(CheckpointID AUTOINCREMENT)
        );"""
    cur.execute(sStmt)

    # Paths Table (order of checkpoints)
    sStmt = """CREATE TABLE IF NOT EXISTS Paths (
            PathID	INTEGER UNIQUE,
            EventID	INTEGER,
            CourseID INTEGER,
            CheckpointID INTEGER,
            CPOrder INTEGER,
            PRIMARY KEY(PathID AUTOINCREMENT)
        );"""
    cur.execute(sStmt)

    # Sitings Table
    sStmt = """CREATE TABLE IF NOT EXISTS Sitings (
            SitingID	INTEGER UNIQUE,
            EventID	INTEGER,
            CheckpointID	INTEGER,
            ParticipantID	INTEGER,
            Sitingtime	TEXT,
            PRIMARY KEY(SitingID AUTOINCREMENT)
        );"""
    cur.execute(sStmt)

    # Traffic Table
    sStmt = """CREATE TABLE IF NOT EXISTS Traffic (
            TrafficID	INTEGER UNIQUE,
            EventID	INTEGER,
            Logtime	TEXT,
            Message	TEXT,
            Source TEXT,
            AssignedTo	TEXT,
            CompletedTime	TEXT,
            Status	TEXT,
            PRIMARY KEY(TrafficID AUTOINCREMENT)
        );"""
    cur.execute(sStmt)

    cn.commit()

    sStmt = "CREATE TABLE IF NOT EXISTS Settings (SettingID INTEGER UNIQUE, SettingName TEXT, SettingValue TEXT, PRIMARY KEY(SettingID AUTOINCREMENT))"
    cur.execute(sStmt)

    sStmt = "CREATE TABLE IF NOT EXISTS Recents (RecentID INTEGER UNIQUE, EventName TEXT, DBPath TEXT, PRIMARY KEY(RecentID AUTOINCREMENT))"
    cur.execute(sStmt)

    # Add the settings fields
    stmt = "select SettingName from Settings where SettingName='DBVersion';"
    cur.execute(stmt)
    setting_exists = cur.fetchone()
    if not setting_exists:
        cur.execute("""INSERT INTO Settings (SettingName, SettingValue) VALUES ('DBVersion','1')""")
        cn.commit()

    # Local Users Table
    sStmt = "CREATE TABLE IF NOT EXISTS LocalUsers (UserID INTEGER, Username TEXT, Password TEXT, Permission INTEGER)"
    cur.execute(sStmt)

    # Add a local admin user
    stmt = "select Username from LocalUsers where Username='admin';"
    cur.execute(stmt)
    user_exists = cur.fetchone()
    if not user_exists:
        sStmt = "INSERT INTO LocalUsers (Username, Password, Permission) VALUEs ('admin', 'admin', 1)"
        cur.execute(sStmt)
        cn.commit()
