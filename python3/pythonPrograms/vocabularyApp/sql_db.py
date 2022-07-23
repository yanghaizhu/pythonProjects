import sqlite3

class SQL_DB:
    def __init__(self, dbName):
        self.conn = sqlite3.connect(dbName)
        self.c = self.conn.cursor()

    def close(self,):
        # Save (commit) the changes
        self.conn.commit()
        # Close the connection
        self.conn.close()

    def run(self, cmd, isSearchCmd = False):
        self.c.execute(cmd)
        if (isSearchCmd):
            self.rets = self.c.fetchall()
            return self.rets
