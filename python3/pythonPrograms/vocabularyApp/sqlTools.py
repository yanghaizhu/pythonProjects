# Information: help you to remamber IELTS vocabulary.
#
# 1. IELTS vocabulary saved in vocabulary.db;
# 2. Use the pygame module to control show the vocabulary one by one;
# 3. Assume the one you skip without looking for detail information is the
#    one you have remembered.
# 4. LeftClick mouse will show more information, rightClick mouse will
#    skip to next no-remembered word.
# 5. Use speech module to read the word and the sentence
# 6. Use threading module to control click while reading is not finished.

import sqlite3
import warnings
warnings.filterwarnings('ignore')



if __name__ == '__main__':

    conn = sqlite3.connect('vocabulary.db')
    c = conn.cursor()
#   execute('''DROP TABLE IF EXISTS vocabulary''')
#   execute('''CREATE TABLE IF NOT EXISTS vocabulary (ID INTEGER PRIMARY KEY, Vocabulary TEXT, Pronounce TEXT, Split TEXT, Chinese TEXT, RememberTips TEXT, RememberImage TEXT, Sentence TEXT, SentenceChinese TEXT)''')

    ### Add a new column
#    c.execute("alter table vocabulary add esayCnt INT")
#    c.execute("alter table vocabulary add normalCnt INT")
#    c.execute("alter table vocabulary add hardCnt INT")
#    c.execute("alter table vocabulary add hardestCnt INT")

    ### Set all value in the column = 0
    c.execute("update vocabulary set  easyDegree=0")
    c.execute("update vocabulary set  easyCnt=0")
#    c.execute("update vocabulary set  normalCnt=0")
#    c.execute("update vocabulary set  hardCnt=0")
#    c.execute("update vocabulary set  hardestCnt=0")

    c.execute("alter table vocabulary rename easyCnt to easyCnt")

#    c.execute('''CREATE TABLE IF NOT EXISTS counter (rateProgress INTEGER)''')
#    c.execute('''SELECT count(*) FROM  counter''')
#    rets = c.fetchall()
#    if(rets[0][0] == 0):
#        c.execute('''INSERT INTO  counter(rateProgress) VALUES (0)''')

#    c.execute('''SELECT * FROM  counter''')
#    rets = c.fetchall()
#    Dataindex = rets[0][0]


# get content to show
    sql = "SELECT * FROM vocabulary where easyCnt=0"
    c.execute(sql)
    rets = c.fetchall()
    print(rets[0])

#    Dataindex = 0
#    sql = "UPDATE counter SET rateProgress="+str(Dataindex)
#    c.execute(sql)
    # Save (commit) the changes
    conn.commit()
    # Close the connection
    conn.close()