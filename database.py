# Marathon Manager
#
# Database creation functions
#
#

import sqlite3
from pathlib import Path


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

    # # Users Table
    # sStmt = """CREATE TABLE Users (UserID INTEGER, PersonID INTEGER, Username TEXT, Password TEXT, Permission INTEGER)"""
    # CUR.execute(sStmt)

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
    CUR.execute(sStmt)

    # Volunteer Log Table (history of assignments, check-ins and -outs)
    sStmt = """CREATE TABLE VolLog (
            LogID	INTEGER UNIQUE,
            VolunteerID INTEGER,
            EventID	INTEGER,
            Assignment	TEXT,
            Checkin	TEXT,
            Checkout	TEXT,
            PRIMARY KEY(LogID AUTOINCREMENT)
        )"""
    CUR.execute(sStmt)

    # Participants Table
    sStmt = """CREATE TABLE Participants (
            ParticipantID	INTEGER UNIQUE,
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
            EventID	INTEGER,
            RaceID	INTEGER,
            Bib	INTEGER,
            PRIMARY KEY(ParticipantID AUTOINCREMENT)
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

    # Courses Table
    sStmt = """CREATE TABLE Courses (
            CourseID	INTEGER UNIQUE,
            EventID	INTEGER,
            CourseName	TEXT,
            Distance	TEXT,
            Color	TEXT,
            Path    TEXT,
            PRIMARY KEY(CourseID AUTOINCREMENT)
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
            Source TEXT,
            AssignedTo	TEXT,
            CompletedTime	TEXT,
            Status	TEXT,
            PRIMARY KEY(TrafficID AUTOINCREMENT)
        );"""
    CUR.execute(sStmt)

    CONN.commit()

    sStmt = "CREATE TABLE IF NOT EXISTS Settings (SettingID INTEGER UNIQUE, SettingName TEXT, SettingValue TEXT, PRIMARY KEY(SettingID AUTOINCREMENT))"
    CUR.execute(sStmt)

    sStmt = "CREATE TABLE IF NOT EXISTS Recents (RecentID INTEGER UNIQUE, EventName TEXT, DBPath TEXT, PRIMARY KEY(RecentID AUTOINCREMENT))"
    CUR.execute(sStmt)

    # Add the settings fields
    # sStmt = 'INSERT INTO Settings (SettingName, SettingValue) VALUES ("DBVersion","1")'
    CUR.execute("""INSERT INTO Settings (SettingName, SettingValue) VALUES ('DBVersion','1')""")
    CONN.commit()

    # Local Users Table
    sStmt = "CREATE TABLE IF NOT EXISTS LocalUsers (UserID INTEGER, Username TEXT, Password TEXT, Permission INTEGER)"
    CUR.execute(sStmt)

    # Add a local admin user
    sStmt = "INSERT INTO LocalUsers (Username, Password, Permission) VALUEs ('admin', 'admin', 1)"
    CUR.execute(sStmt)
    CONN.commit()
