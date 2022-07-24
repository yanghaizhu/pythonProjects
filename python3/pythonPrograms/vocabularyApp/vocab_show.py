import pygame
from sql_db import *
from vocab_set import *
from vocab_show import *
from pygame_frame import *

sqlCmd = dict()
sqlCmd["all"] = "SELECT * FROM  vocabulary"
sqlCmd["noEasy"] = "SELECT * FROM vocabulary where easyDegree > 1 or easyDegree = 0"
sqlCmd["normal"] = "SELECT * FROM vocabulary where easyDegree =2 or easyDegree =3 or easyDegree=0"
sqlCmd["hard"] = "SELECT * FROM vocabulary where easyDegree =3 or easyDegree=0"
sqlCmd["noRecord"] = "SELECT * FROM vocabulary where easyDegree =0"
sqlCmd["dataIndex"] = "SELECT * FROM counter"
sqlCmd["initDataIndex"] = "INSERT INTO  counter (rateProgress) VALUES (0)"

class VOCAB_SHOW:
    def __init__(self, dbName):
        # vocabulary table related parameters
        WINDOW_W, WINDOW_H = 800, 500
        blackColor = (0, 0, 0)
        whiteColor = (255, 255, 255)
        screenSize = (WINDOW_W, WINDOW_H)

        # Init pygameFrame
        pygameFrame = PYGAME_FRAME(pygame, screenSize, "背单词")

        # get content to show
        db = SQL_DB(dbName)
        rets = db.run(sqlCmd["dataIndex"], True)
        dataIndex = rets[0][0]
        rets = db.run(sqlCmd["all"], True)
        wordDetail = VOCAB_SET(rets, dataIndex)

        self.pygameFrame = pygameFrame
        self.wordDetail = wordDetail
        self.db = db


    def showVocab(self,color,pos_x,clickCnt):
        self.pygameFrame.blitText("font1", self.wordDetail.Vocabulary, color, (pos_x, 40), True)
        self.pygameFrame.blitText("font2", self.wordDetail.Pronounce, color, (pos_x, 80), True)
        if(clickCnt > 0):
            self.pygameFrame.blitText("font3", self.wordDetail.Chinese, color, (pos_x, 120), True)
            self.pygameFrame.blitText("font3", self.wordDetail.Split, color, (pos_x, 160), True)
            self.pygameFrame.blitText("font3", self.wordDetail.RememberImage, color, (pos_x, 190), True)
        if(clickCnt > 1):
            self.pygameFrame.blitText("font3", self.wordDetail.Sentence, color, (pos_x, 230), True)
            self.pygameFrame.blitText("font3", self.wordDetail.SentenceChinese, color, (pos_x, 260), True)

    def showRecordInfo(self,infoStr,color,pos):
        self.pygameFrame.blitText("font3", infoStr, color,pos, False)

    def updateDisp(self,):
        self.pygameFrame.pygame.display.update()
        self.pygameFrame.fillbgColor((0,0,0))
        self.pygameFrame.blitImg("BG",(0,0))