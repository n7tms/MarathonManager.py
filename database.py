# Marathon Manager
#
# Database creation functions
#
#

import sqlite3
from pathlib import Path
# from constants import *

class MMDatabase:
    def __init__(self, dbname) -> None:
        self.dbName = dbname
        self.cn = None
        self.cur = None
        self.open = False

        if dbname:
            self.init_db(self.dbName)
            self.open = True


    def init_db(self, dbname):
        self.dbName = dbname
        self.cn = sqlite3.connect(self.dbName)
        self.cn.row_factory = sqlite3.Row
        self.cur = self.cn.cursor()


    def database_exists(self,db_name: str) -> bool:
        """Test if the specified database file exists."""
        path = Path(db_name)
        if path.is_file():
            return True
        else:
            return False

    def create_database(self) -> bool:
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
        self.cur.execute(sStmt)

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
        self.cur.execute(sStmt)

        # Participants Table
        sStmt = """CREATE TABLE IF NOT EXISTS Participants (
                ParticipantID	INTEGER UNIQUE,
                Firstname TEXT, 
                Lastname TEXT, 
                Gender TEXT, 
                Age INTEGER,
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
                Team TEXT,
                PRIMARY KEY(ParticipantID AUTOINCREMENT)
            )"""
        self.cur.execute(sStmt)

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
        self.cur.execute(sStmt)

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
        self.cur.execute(sStmt)

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
        self.cur.execute(sStmt)

        # Paths Table (order of checkpoints)
        sStmt = """CREATE TABLE IF NOT EXISTS Paths (
                PathID	INTEGER UNIQUE,
                EventID	INTEGER,
                CourseID INTEGER,
                CheckpointID INTEGER,
                CPOrder INTEGER,
                PRIMARY KEY(PathID AUTOINCREMENT)
            );"""
        self.cur.execute(sStmt)

        # Sitings Table
        sStmt = """CREATE TABLE IF NOT EXISTS Sitings (
                SitingID	INTEGER UNIQUE,
                EventID	INTEGER,
                CheckpointID	INTEGER,
                ParticipantID	INTEGER,
                SitingTime	TEXT,
                PRIMARY KEY(SitingID AUTOINCREMENT)
            );"""
        self.cur.execute(sStmt)

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
        self.cur.execute(sStmt)

        self.cn.commit()

        sStmt = "CREATE TABLE IF NOT EXISTS Settings (SettingID INTEGER UNIQUE, SettingName TEXT, SettingValue TEXT, PRIMARY KEY(SettingID AUTOINCREMENT))"
        self.cur.execute(sStmt)

        sStmt = "CREATE TABLE IF NOT EXISTS Recents (RecentID INTEGER UNIQUE, EventName TEXT, DBPath TEXT, PRIMARY KEY(RecentID AUTOINCREMENT))"
        self.cur.execute(sStmt)

        # Add the settings fields
        stmt = "select SettingName from Settings where SettingName='DBVersion';"
        self.cur.execute(stmt)
        setting_exists = self.cur.fetchone()
        if not setting_exists:
            self.cur.execute("""INSERT INTO Settings (SettingName, SettingValue) VALUES ('DBVersion','1')""")
            self.cn.commit()

        # Local Users Table
        sStmt = "CREATE TABLE IF NOT EXISTS LocalUsers (UserID INTEGER, Username TEXT, Password TEXT, Permission INTEGER)"
        self.cur.execute(sStmt)

        # Add a local admin user
        stmt = "select Username from LocalUsers where Username='admin';"
        self.cur.execute(stmt)
        user_exists = self.cur.fetchone()
        if not user_exists:
            sStmt = "INSERT INTO LocalUsers (Username, Password, Permission) VALUEs ('admin', 'admin', 1)"
            self.cur.execute(sStmt)
            self.cn.commit()

        return True

    def nonQuery(self, stmt: str, args: list=None) -> int:
        """Used to execute inserts, deletes, and updates"""
        if args:
            rowcount = self.cur.execute(stmt,args)
        else:
            rowcount = self.cur.execute(stmt)
        self.cn.commit()
        return rowcount

    def query(self, stmt: str, args: list=None) -> list:
        """used to return rows e.g. from a select statement"""
        if args:
            rows = self.cur.execute(stmt,args).fetchall()
        else:
            rows = self.cur.execute(stmt).fetchall()

        # turn the results into something useful
        list_acc = []
        for item in rows:
            list_acc.append({k: item[k] for k in item.keys()})
        return list_acc



        