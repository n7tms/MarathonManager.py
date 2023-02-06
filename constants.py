import sqlite3

# =============================================================================
# Constants
DB_NAME = 'mm_test3.db'
DB_NAME_SETTINGS = 'mmsettings.db'
CONN = None
CUR = None
cn = sqlite3.connect(DB_NAME)
cur = cn.cursor()
