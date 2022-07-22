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
    Vocabulary = 1
    Pronounce = 2
    Chinese = 3
    Split = 4
    RememberTips = 5
    RememberImage = 6
    Sentence = 7
    SentenceChinese = 8
    RecordTimes = 9
    RecordDone = 10

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
    def fillbgColor(self,color):
        self.screen.fill(color)
    def blitImg(self,name,pos):
        self.screen.blit(self.imgDict[name], pos)
class vocabularyDict:
    def __init__(self,app,vocabularyDict):
        self.app = app
        self.vocab = vocabularyDict
    def showVocab(self,color,pos_x,clickCnt):
        self.app.blitText("font1", self.vocab["Vocabulary"], color, (pos_x, 40), True)
        self.app.blitText("font2", self.vocab["Pronounce"], color, (pos_x, 80), True)
        if(clickCnt > 0):
            app.blitText("font3", self.vocab["Chinese"], color, (pos_x, 120), True)
            app.blitText("font3", self.vocab["Split"], color, (pos_x, 160), True)
            app.blitText("font3", self.vocab["RememberImage"], color, (pos_x, 190), True)
        if(clickCnt > 1):
            app.blitText("font3", self.vocab["Sentence"], color, (pos_x, 230), True)
            app.blitText("font3", self.vocab["SentenceChinese"], color, (pos_x, 260), True)

    def showRecordInfo(self,infoStr,color,pos):
        app.blitText("font3", infoStr, color,pos, False)


if __name__ == '__main__':

    conn = sqlite3.connect('vocabulary.db')
    c = conn.cursor()
#   execute('''DROP TABLE IF EXISTS vocabulary''')
#   execute('''CREATE TABLE IF NOT EXISTS vocabulary (ID INTEGER PRIMARY KEY, Vocabulary TEXT, Pronounce TEXT, Split TEXT, Chinese TEXT, RememberTips TEXT, RememberImage TEXT, Sentence TEXT, SentenceChinese TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS counter (rateProgress INTEGER)''')
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



    app = PYGAME_FRAME(pygame,screenSize,"背单词")
    app.addImag("BG","bg.jpg",40)
    app.resizeImag("BG",(800,1500))
    app.addFond("font1",'fonts/msyh.ttc', 35)
    app.addFond("font2",'fonts/arial.ttf', 30)
    app.addFond("font3",'fonts/msyh.ttc', 15)

    app.fillbgColor(blackColor)
    app.blitImg("BG",(0,0))

    sql = "SELECT * FROM vocabulary"
    c.execute(sql)
    retrievedData = c.fetchall()
    ret = retrievedData[Dataindex]
    myDict = dict()
    myDict["Vocabulary"] = ret[columEnum.Vocabulary.value]
    myDict["Pronounce"] = ret[columEnum.Pronounce.value]
    myDict["Split"] = ret[columEnum.Split.value]
    myDict["Chinese"] = ret[columEnum.Chinese.value]
    myDict["RememberTips"] = ret[columEnum.RememberTips.value]
    myDict["RememberImage"] = ret[columEnum.RememberImage.value]
    myDict["Sentence"] = ret[columEnum.Sentence.value]
    myDict["SentenceChinese"] = ret[columEnum.SentenceChinese.value]
    Dataindex += 1
    print(myDict)
    vocabShowInApp = vocabularyDict(app,myDict)
    vocabShowInApp.showVocab(whiteColor,WINDOW_W/2, leftClickCnt)
    vocabShowInApp.showRecordInfo("正在学习第" + str(Dataindex) + "/" + "个单词...",whiteColor,(0,0))

    app.updateDisp()

    t1 = threading.Thread(target=readOutLoudly, args=(myDict["Vocabulary"],))
    t1.start()

    a = 10
    pressedMousePos = -1
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
                        print(pressedMousePos)
                        print(a)
                        a += 1

        if pressedMousePos < 0:
            continue
        elif pressedMousePos == 0:
            if t1.is_alive():
                continue

            app.fillbgColor(blackColor)
            app.blitImg("BG",(0,0))
            #print('Pressed LEFT Button!')
            leftClickCnt = leftClickCnt + 1
            vocabShowInApp = vocabularyDict(app, myDict)
            vocabShowInApp.showVocab(whiteColor, WINDOW_W / 2, leftClickCnt)
            vocabShowInApp.showRecordInfo("正在学习第" + str(Dataindex) + "/" + "个单词...",whiteColor,(0,0))

            app.updateDisp()

            if leftClickCnt > 1:
                t1 = threading.Thread(target=readOutLoudly, args=(myDict["Sentence"],))
                t1.start()
            else:
                t1 = threading.Thread(target=readOutLoudly, args=(myDict["Vocabulary"],))
                t1.start()
        elif pressedMousePos == 2:
            if t1.is_alive():
                continue
            ret = retrievedData[Dataindex]
            myDict = dict()
            myDict["Vocabulary"] = ret[columEnum.Vocabulary.value]
            myDict["Pronounce"] = ret[columEnum.Pronounce.value]
            myDict["Split"] = ret[columEnum.Split.value]
            myDict["Chinese"] = ret[columEnum.Chinese.value]
            myDict["RememberTips"] = ret[columEnum.RememberTips.value]
            myDict["RememberImage"] = ret[columEnum.RememberImage.value]
            myDict["Sentence"] = ret[columEnum.Sentence.value]
            myDict["SentenceChinese"] = ret[columEnum.SentenceChinese.value]
            Dataindex += 1

            leftClickCnt = 0
            app.fillbgColor(blackColor)
            app.blitImg("BG",(0,0))
            vocabShowInApp = vocabularyDict(app, myDict)
            vocabShowInApp.showVocab(whiteColor, WINDOW_W / 2, leftClickCnt)
            vocabShowInApp.showRecordInfo("正在学习第" + str(Dataindex) + "/" + "个单词...",whiteColor,(0,0))
            app.updateDisp()
            t1 = threading.Thread(target=readOutLoudly, args=(myDict["Vocabulary"],))
            t1.start()
        pressedMousePos = -1

    sql = "UPDATE counter SET rateProgress="+str(Dataindex)
    c.execute(sql)
    # Save (commit) the changes
    conn.commit()
    # Close the connection
    conn.close()
    exit()