import pygame
from sql_db import *
from vocab_set import *
from vocab_show import *
from pygame_frame import *

class VOCAB_PYGAME_SHOW:
    def __init__(self, dbName):
        # vocabulary table related parameters
        self.blackColor = (0, 0, 0)
        self.whiteColor = (255, 255, 255)
        self.pygameScreenWidth = 800
        self.pygameScreenHigh = 500
        self.pygameScreenSize = (self.pygameScreenWidth , self.pygameScreenHigh)

        # Init pygameFrame
        self.pygameFrame = PYGAME_FRAME(pygame, self.pygameScreenSize, "背单词")
        self.pygameFrame.pygameFrameInit()

        self.wordDetail = VOCAB_SET(dbName)


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