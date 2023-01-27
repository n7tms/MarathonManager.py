import sqlite3

class DB:
    def __init__(self):
        self.dbname = 'test.db'

DB_NAME = 'mm_test2.db'
checkpoints = {}

def get_checkpoints() -> list:
    """return a list of checkpoints"""
    cn,cur = None,None
    cn = sqlite3.connect(DB_NAME)
    cur = cn.cursor()

    if len(checkpoints) > 0:
        checkpoints.clear()


    res = cur.execute("select CheckpointID,CPName from Checkpoints")
    for x in res:
        checkpoints[x[1]] = x[0]
    
    print(list(checkpoints.values()))

    if 'M1' in checkpoints:
        print('is')

    print(list(checkpoints.keys())[0])
    return list(checkpoints.keys())



print(get_checkpoints())
