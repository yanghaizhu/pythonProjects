
from enum import Enum

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

class VOCAB_SET:
    def __init__(self, vocabs, dataIndex=0):
        self.vocabs = vocabs
        self.dataIndex = dataIndex

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
