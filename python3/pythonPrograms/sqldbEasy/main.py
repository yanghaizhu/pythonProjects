import sqlite3
import string
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

    def queryall(self, sql):
        """
        查询所有的数据及对应的列名
        :param sql:
        :return:
        """
        self.c.execute(sql)
        # TODO 获取查询结果的列名
        columns_tuple = self.c.description
        # columns_tuple示例： (('TACHE_NAME', None, None, None, None, None, None), ('avgtime', None, None, None, None, None, None), ('DATE', None, None, None, None, None, None), ('ANALYSIS_TIME', None, None, None, None, None, None))
        columns_list = [field_tuple[0] for field_tuple in columns_tuple]
        # TODO 获取查询结果
        query_result = self.c.fetchall()
        return columns_list,query_result




#List tables
sql = "select * from sqlite_master"
#Add new table
table = "table"
sql = "CREATE TABLE IF NOT EXISTS " + table + " (ID INTEGER PRIMARY KEY)"
#Delete table
table = "table"
sql = "DROP TABLE IF EXISTS " + table
#Add new column
table = "table"
column = "column"
type = "int"
sql = "alter table " + table +  " add " + column + " " + type
#Modify  column
table = "table"
newcolumn = "newcolumn"
sql = "alter table " + table +  " rename " + column + " to "
#Delete  column
table = "plan"
column = "column"
sql = "alter table " + table +  " drop column " + column

if __name__ == '__main__':
    sqlEasy = SQL_DB("IKnow.db")

    # Add new table
    table = "plan"
    sql = "CREATE TABLE IF NOT EXISTS " + table + " (ID INTEGER PRIMARY KEY)"
    sqlEasy.run(sql, False)

#    sql = "DROP TABLE IF EXISTS " + table
#    sqlEasy.run(sql, False)

    column = "test"
    type = "int"
    sql = "alter table " + table + " add " + column + " " + type
#    sqlEasy.run(sql, False)
    sql = "insert into " + table + " (test) values ('1')"
#    sqlEasy.run(sql, False)

    newcolumn = "test2"
    sql = "alter table " + table + " rename " + column + " to " + newcolumn
#    sqlEasy.run(sql, False)

#    column = "test"
#    sql = "alter table " + table + " drop column " + column
#    sqlEasy.run(sql, False)

    #    sqlEasy.run(sql, False)
    sql = "select * from plan"
    rets = sqlEasy.queryall(sql)
    print(rets)
    sql = "select * from sqlite_master"
    rets = sqlEasy.queryall(sql)
    print(rets)

    sql = "update plan set  test2=2 "
    sqlEasy.run(sql, False)

    loopFlag = True
    while loopFlag:
        print("0:history\n1:plan\n10:new table")
        select = input("please input you table number:")
        i = int(select)
        if(i==0):
            table = input("new table name")
            sql = "CREATE TABLE IF NOT EXISTS " + table + " (ID INTEGER PRIMARY KEY)"
            sqlEasy.run(sql, False)
            sql = "select * from " + table
            rets = sqlEasy.queryall(sql)
            print(rets)
#        if select == "quit":

        loopFlag = False

    sqlEasy.close()