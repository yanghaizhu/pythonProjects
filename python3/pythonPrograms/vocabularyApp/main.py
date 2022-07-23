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
from datetime import datetime

import pygame
from pygame.locals import *
from pygame.color import THECOLORS
from collections import *
import speech
import threading
#from os import *
import os
from enum import Enum
import warnings
warnings.filterwarnings('ignore')

def readOutLoudly(sentence:str):
    speech.say(sentence)


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

class WORD_DETAIL:
    def __init__(self, vocab):
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

    def update(self, vocab):
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
        if (mousePosition == 0):
            self.EasyCnt += 1
        elif (mousePosition == 1):
            self.NormalCnt += 1
        elif (mousePosition == 2):
            self.HardCnt += 1
        elif (mousePosition == 3):
            self.HardestCnt += 1
        self.sql = "update vocabulary set EasyDegree=" + str(self.EasyDegree) + ",  easyCnt=" + str(self.EasyCnt) \
                   + " , normalCnt=" + str(self.NormalCnt) + ",  hardCnt=" + str(self.HardCnt) + " , hardestCnt=" + str(self.HardestCnt) \
                   + " where ID =" + str(self.ID)
        print(self.sql)

class PYGAME_FRAME:
    def __init__(self, pygame, screenSize, title):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(title)
        self.screenSize = screenSize
        self.pygame = pygame
        self.screen = pygame.display.set_mode(screenSize, pygame.DOUBLEBUF, 32)
        self.fontDict = dict()
        self.imgDict = dict()
        self.fontDict["default"] = self.pygame.font.Font('fonts/arial.ttf', 10)

    def addFond(self,name,fontPath,size):
        self.fontDict[name] = self.pygame.font.Font(fontPath, size)

    def addImag(self,name,imgPath,aphal):
        self.imgDict[name] = self.pygame.image.load(imgPath)
        if (aphal < 100):
            self.imgDict[name].set_alpha(aphal)


    def resizeImag(self,name,size):
        print(name)
        print(self.imgDict)
        if(name in self.imgDict.keys()):
            self.imgDict[name] = self.pygame.transform.scale(self.imgDict[name], size)
    def blitText(self,fontName,textStr,color,position,centFlag):
        text = self.fontDict[fontName].render(textStr, True, color)
        w, h = text.get_size()
        if (centFlag):
            posStart = (position[0]-w/2, position[1]-h/2)
        else:
            posStart = position
        self.screen.blit(text, posStart)
    def updateDisp(self,):
        self.pygame.display.update()
        self.fillbgColor(blackColor)
        self.blitImg("BG",(0,0))
    def fillbgColor(self,color):
        self.screen.fill(color)
    def blitImg(self,name,pos):
        self.screen.blit(self.imgDict[name], pos)

class VOCAB_APP:
    def __init__(self,pygameFrame,wordDetail):
        self.pygameFrame = pygameFrame
        self.wordDetail = wordDetail
    def showVocab(self,color,pos_x,clickCnt):
        self.pygameFrame.blitText("font1", self.wordDetail.Vocabulary, color, (pos_x, 40), True)
        self.pygameFrame.blitText("font2", self.wordDetail.Pronounce, color, (pos_x, 80), True)
        if(clickCnt > 0):
            pygameFrame.blitText("font3", self.wordDetail.Chinese, color, (pos_x, 120), True)
            pygameFrame.blitText("font3", self.wordDetail.Split, color, (pos_x, 160), True)
            pygameFrame.blitText("font3", self.wordDetail.RememberImage, color, (pos_x, 190), True)
        if(clickCnt > 1):
            pygameFrame.blitText("font3", self.wordDetail.Sentence, color, (pos_x, 230), True)
            pygameFrame.blitText("font3", self.wordDetail.SentenceChinese, color, (pos_x, 260), True)

    def showRecordInfo(self,infoStr,color,pos):
        pygameFrame.blitText("font3", infoStr, color,pos, False)


if __name__ == '__main__':

    conn = sqlite3.connect('vocabulary.db')
    c = conn.cursor()
    c.execute('''SELECT count(*) FROM  counter''')
    rets = c.fetchall()
    if(rets[0][0] == 0):
        c.execute('''INSERT INTO  counter(rateProgress) VALUES (0)''')

    c.execute('''SELECT * FROM  counter''')
    rets = c.fetchall()
    Dataindex = rets[0][0]

    # vocabulary table related parameters
    leftClickNumber = 0
    recordTimes = 0
    recordDone = 0
    rowNumber = 5473
    WINDOW_W, WINDOW_H = 800, 500
    blackColor = (0,0,0)
    whiteColor = (255,255,255)
    screenSize = (WINDOW_W, WINDOW_H)

    continueFlag = True
    leftClickCnt = 0

# Init pygameFrame
    pygameFrame = PYGAME_FRAME(pygame,screenSize,"背单词")
    pygameFrame.addImag("BG","bg.jpg",80)
    pygameFrame.resizeImag("BG",(800,1500))
    pygameFrame.addFond("font1",'fonts/msyh.ttc', 35)
    pygameFrame.addFond("font2",'fonts/arial.ttf', 30)
    pygameFrame.addFond("font3",'fonts/msyh.ttc', 15)
    pygameFrame.updateDisp()

# get content to show
    sql = "SELECT * FROM vocabulary"
    c.execute(sql)
    retrievedData = c.fetchall()
    ret = retrievedData[Dataindex]
    wordDetail = WORD_DETAIL(ret)

    Dataindex += 1

    vocabShowInApp = VOCAB_APP(pygameFrame,wordDetail)
    vocabShowInApp.showVocab(whiteColor, WINDOW_W/2, leftClickCnt)
    vocabShowInApp.showRecordInfo("正在学习第" + str(Dataindex) + "/" + "个单词...",whiteColor,(0,0))

    pygameFrame.updateDisp()

    t1 = threading.Thread(target=readOutLoudly, args=(wordDetail.Vocabulary,))
    t1.start()

    pressedMousePos = -1
    mousePosition = 0
    while continueFlag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continueFlag = False
            elif event.type == MOUSEBUTTONDOWN:
                continueFlag = True
                pressed_array = pygame.mouse.get_pressed()
                for index in range(len(pressed_array)):
                    if pressed_array[index]:
                        pressedMousePos = index
                        if (index == 2):
                            pos = pygame.mouse.get_pos()
                            mousePosition = ((pos[0] > WINDOW_W/2) << 1) | (pos[1] > WINDOW_H/2)
                            wordDetail.updateCnt(mousePosition)
        if pressedMousePos < 0:
            continue
        elif pressedMousePos == 0:
            if t1.is_alive():
                continue
            #print('Pressed LEFT Button!')
            leftClickCnt = leftClickCnt + 1
            vocabShowInApp = VOCAB_APP(pygameFrame, wordDetail)
            vocabShowInApp.showVocab(whiteColor, WINDOW_W / 2, leftClickCnt)
            vocabShowInApp.showRecordInfo("正在学习第" + str(Dataindex) + "/" + "个单词...",whiteColor,(0,0))

            pygameFrame.updateDisp()

            if leftClickCnt > 1:
                t1 = threading.Thread(target=readOutLoudly, args=(wordDetail.Sentence,))
                t1.start()
            else:
                t1 = threading.Thread(target=readOutLoudly, args=(wordDetail.Vocabulary,))
                t1.start()
        elif pressedMousePos == 2:
            if t1.is_alive():
                continue

            c.execute(wordDetail.sql)
            ret = retrievedData[Dataindex]
            wordDetail.update(ret)
            Dataindex += 1
            leftClickCnt = 0
            vocabShowInApp = VOCAB_APP(pygameFrame, wordDetail)
            vocabShowInApp.showVocab(whiteColor, WINDOW_W / 2, leftClickCnt)
            vocabShowInApp.showRecordInfo("正在学习第" + str(Dataindex) + "/" + "个单词...",whiteColor,(0,0))
            pygameFrame.updateDisp()
            t1 = threading.Thread(target=readOutLoudly, args=(wordDetail.Vocabulary,))
            t1.start()
        pressedMousePos = -1

    sql = "UPDATE counter SET rateProgress="+str(Dataindex)
    c.execute(sql)
    # Save (commit) the changes
    conn.commit()
    # Close the connection
    conn.close()
    exit()