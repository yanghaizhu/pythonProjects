
from enum import Enum

from sql_db import *

class columEnum(Enum):
    ID = 0
    Vocabulary = 1
    Pronounce = 2
    Chinese = 3
    Split = 4
    RememberTips = 5
    RememberImage = 6
    Sentence = 7
    SentenceChinese = 8
    EasyDegree = 9
    EasyCnt = 10
    NormalCnt = 11
    HardCnt = 12
    HardestCnt = 13

sqlCmd = dict()
sqlCmd["all"] = "SELECT * FROM  vocabulary"
sqlCmd["total"] = "SELECT count(*) FROM  vocabulary"
sqlCmd["noEasy"] = "SELECT * FROM vocabulary where easyDegree > 1 or easyDegree = 0"
sqlCmd["normal"] = "SELECT * FROM vocabulary where easyDegree =2 or easyDegree =3 or easyDegree=0"
sqlCmd["hard"] = "SELECT * FROM vocabulary where easyDegree =3 or easyDegree=0"
sqlCmd["noRecord"] = "SELECT * FROM vocabulary where easyDegree =0"
sqlCmd["dataIndex"] = "SELECT * FROM counter"
sqlCmd["initDataIndex"] = "INSERT INTO  counter (rateProgress) VALUES (0)"

class VOCAB_SET:
    def __init__(self, dbName, typeStr = "all"):
        self.db = SQL_DB(dbName)
        rets = self.db.run(sqlCmd["dataIndex"], True)
        self.dataIndex = rets[0][0]
        self.vocabs = self.db.run(sqlCmd[typeStr], True)
        rets = self.db.run(sqlCmd["total"], True)
        self.totalVocab = rets[0][0]


    def next(self, ):
        vocab = self.vocabs[self.dataIndex]
        self.dataIndex += 1
        self.ID = vocab[columEnum.ID.value]
        self.Vocabulary = vocab[columEnum.Vocabulary.value]
        self.Pronounce = vocab[columEnum.Pronounce.value]
        self.Split = vocab[columEnum.Split.value]
        self.Chinese = vocab[columEnum.Chinese.value]
        self.RememberTips = vocab[columEnum.RememberTips.value]
        self.RememberImage = vocab[columEnum.RememberImage.value]
        self.Sentence = vocab[columEnum.Sentence.value]
        self.SentenceChinese = vocab[columEnum.SentenceChinese.value]
        self.EasyDegree = vocab[columEnum.EasyDegree.value]
        self.EasyCnt = vocab[columEnum.EasyCnt.value]
        self.NormalCnt = vocab[columEnum.NormalCnt.value]
        self.HardCnt = vocab[columEnum.HardCnt.value]
        self.HardestCnt = vocab[columEnum.HardestCnt.value]

    def updateCnt(self, mousePosition):
        self.EasyDegree = mousePosition
        if (mousePosition == 1):
            self.EasyCnt += 1
        elif (mousePosition == 2):
            self.NormalCnt += 1
        elif (mousePosition == 3):
            self.HardCnt += 1
        elif (mousePosition == 4):
            self.HardestCnt += 1
        self.sql = "update vocabulary set EasyDegree=" + str(self.EasyDegree) + ",  easyCnt=" + str(self.EasyCnt) \
                   + " , normalCnt=" + str(self.NormalCnt) + ",  hardCnt=" + str(self.HardCnt) + " , hardestCnt=" + str(self.HardestCnt) \
                   + " where ID =" + str(self.ID)
