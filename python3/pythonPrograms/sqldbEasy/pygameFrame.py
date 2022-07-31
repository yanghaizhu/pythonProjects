from typing import Tuple, Any

import pygame
from pygame.locals import *
from pygame.color import THECOLORS
import string
from Pinyin2Hanzi import DefaultDagParams
from Pinyin2Hanzi import dag

import pygame
from Pinyin2Hanzi import DefaultDagParams
from Pinyin2Hanzi import dag
import sqlite3
import string
from pygame import *
from pygame.locals import *
from pygame.color import THECOLORS
from pygameFrame import *
from enumDefine import *

class SQL_DB:
    def __init__(self, dbName):
        self.conn = sqlite3.connect(dbName)
        self.c = self.conn.cursor()

    def close(self,):
        # TODO Save (commit) the changes
        self.conn.commit()
        # TODO  Close the connection
        self.conn.close()

    def lookup(self, cmd):
        self.c.execute(cmd)
        self.rets = self.c.fetchall()
        return self.rets

    def modify(self, cmd):
        self.c.execute(cmd)

    def lookupHeader(self, sql):
        self.c.execute(sql)
        # TODO 获取查询结果的列名
        columns_tuple = self.c.description
        columns_list = [field_tuple[0] for field_tuple in columns_tuple]
        # TODO 获取查询结果
        return columns_list

    def lookupWithHeader(self, sql):
        self.c.execute(sql)
        # TODO 获取查询结果的列名
        columns_tuple = self.c.description
        columns_list = [field_tuple[0] for field_tuple in columns_tuple]
        # TODO 获取查询结果
        query_result = self.c.fetchall()
        return columns_list,query_result

class PYGAME_FRAME:




    def __init__(self, pygame, screenWidth = 800, screenHeight=1000, title = "title", textBoxHeight = 15):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(title)
        screenSize = (screenWidth, screenHeight, )
        screen = pygame.display.set_mode(screenSize, pygame.DOUBLEBUF, 32)
        self.sqlEasy = None
        self.pygame = pygame
        self.screenSize = screenSize
        self.screen = screen
        self.fontDict = dict()
        self.imgDict = dict()
        self.fontDict["default"] = pygame.font.Font('fonts/arial.ttf', 10)
        self.fontDict["song"] = pygame.font.Font('fonts/msyh.ttc', 10)



        self.pos = (0,0)
        self.pressedMouseType = -1
        self.continueFlag = True

        self.textBoxWidth = screenWidth
        self.textBoxHeight = textBoxHeight
        self.textBoxPosX = 0
        self.textBoxPosY = screenHeight - textBoxHeight



        self.dagparams = DefaultDagParams()
        self.state = 0  # 0初始状态 1输入拼音状态
        self.page = 1  # 第几页
        self.limit = 5  # 显示几个汉字
        self.pinyin = ''
        self.word_list = []  # 候选词列表
        self.word_list_surf = None  # 候选词surface
        self.buffer_text = ''  # 联想缓冲区字符串

        self.key = None
        self.unicode = None
        self.keyPressed = False
        self.keyAgain = False
        self.timerDiff = 300
        self.preTimer = None

        self.textList = []

        self.dbStatus = dbStatus.showDbs.value

        self.dbList = []
        self.dbIdx = -1
        self.tableList = []
        self.tableIdx = -1
        self.columnList = []
        self.columnIdx = -1
        self.rowList = []
        self.rowIdx = -1

        self.dbListFileName = "dbList.txt"
        self.readDbListFp = open(self.dbListFileName, 'r')
        self.dbList = [db.rstrip() for db in self.readDbListFp.readlines()]
        self.readDbListFp.close()
        self.updateTextList(self.dbList)

        self.targetSta = targetE.db.name
        self.actionSta = actionE.show.name
        self.targetStr = ["DB","Table","Column","Row"]
        self.actionStr = ["Show","Add","Modify","Delete"]
        self.controlSta = controlE.pending.value

        self.inputStr = ""
        self.remindText = ""
        self.cmdStr = ""

        self.backColorList = [(102,61,116),(127,159,175),(40,60,62),(221,107,123)]
        self.fontColorList = [(235,225,169),(212,229,239),(226,162,172),(212,221,225)]

    # TODO Key event. Just record it.
    def keyEvent(self, event):

        if(event.type == pygame.KEYDOWN):
            self.key = event.key
            self.unicode = event.unicode
            self.keyPressed = True
            print(str(self.unicode) + " : " + str(self.key))
        elif(event.type == pygame.KEYUP):
            self.key = None
            self.unicode = None
            self.keyPressed = False
            self.preTimer = None

    # TODO Check if key need to trigger, which may impact the inputStr.
    def isKeyAgain(self):
        if self.keyPressed and self.key < 123:
            if self.preTimer == None:
                self.keyAgain = True
                self.timerDiff = 300
                self.preTimer = pygame.time.get_ticks()
            elif pygame.time.get_ticks() - self.preTimer > self.timerDiff:
                self.keyAgain = True
                self.timerDiff = 80
                self.preTimer = pygame.time.get_ticks()
            else:
                self.keyAgain = False
        else:
            self.keyAgain = False
        return self.keyAgain

    def updateInputStr(self,):
        if self.isKeyAgain == False:
            return

        key = self.key
        unicode = self.unicode
        char = None
        # 退位键
        if key == 8:
            self.inputStr = self.inputStr[:-1]
        # 回车键
        elif key == 13:
            if(self.inputStr != ""):
                self.cmdStr = self.inputStr
            print(self.inputStr)
            self.inputStr = ""
        elif key < 123:
            self.inputStr += unicode

    def constructCmd(self):
        if self.cmdStr == "":
            return
        if self.cmdStr == ">":# TODO Show
            self.actionSta = actionE.show.name
        elif self.cmdStr == "+":# TODO Add
            self.actionSta = actionE.add.name
        elif self.cmdStr == "-":# TODO Delete
            self.actionSta = actionE.delete.name
        elif self.cmdStr == "/":# TODO Replace
            self.actionSta = actionE.modify.name
        elif self.cmdStr == "<":
            if self.targetSta == targetE.db.name:
                self.targetSta = targetE.db.name
                self.updateTextList(self.dbList)
            if self.targetSta == targetE.table.name:
                self.targetSta = targetE.db.name
                self.updateTextList(self.dbList)
            if self.targetSta == targetE.column.name:
                self.targetSta = targetE.table.name
                self.updateTextList(self.tableList)
            if self.targetSta == targetE.row.name:
                self.targetSta = targetE.table.name
                self.updateTextList(self.tableList)
        elif self.cmdStr == "<<":
            self.targetSta = targetE.db.name
            self.updateTextList(self.dbList)

        elif self.cmdStr.isdigit():
            digit = int(self.cmdStr)
            # TODO DB target start
            if self.targetSta == targetE.db.name:
                if digit < len(self.dbList):
                    self.dbIdx = digit
                    if self.actionSta == actionE.delete.value:
                        self.dbList.pop(digit)
                        self.dbIdx -= 1
                        print(self.dbList)
                        dblistStr = [db + "\n" for db in self.dbList]
                        fp = open(self.dbListFileName, 'w')
                        fp.writelines(dblistStr)
                        fp.close()

                        self.updateTextList(self.dbList)
                        if len(self.dbList) == 0:
                            self.actionSta == actionE.add.name
                    elif self.actionSta == actionE.add.name:
                        self.remindText = "should input a new db name you want to add."
                    elif self.actionSta == actionE.show.name:
                        if self.sqlEasy != None:
                            self.sqlEasy.close()
                        self.sqlEasy = SQL_DB(self.dbList[self.dbIdx])
                        self.sql = "select * from sqlite_master"
                        rets = self.lookup(self.sql)
                        self.tableList = [table[2] for table in rets]
                        self.updateTextList(self.tableList)
                        self.targetSta = targetE.table.name

                else:
                    self.remindText = "input number out of range for {db}"
                    if (len(self.dbList)) == 0:
                        self.actionSta = actionE.add.name
            # TODO DB target end
            # TODO Table target start
            elif self.targetSta == targetE.table.name:
                if digit < len(self.tableList):
                    self.tableIdx = digit
                    if self.actionSta == actionE.delete.name:
                        self.tableList.pop(digit)
                        self.tableIdx -= 1
                        print(self.tableList)
                        self.updateTextList(self.tableList)
                        if len(self.tableList) == 0:
                            self.actionSta == actionE.add.name
                    elif self.actionSta == actionE.add.name:
                        self.remindText = "should input a new db name you want to add."
                    elif self.actionSta == actionE.show.name:
                        self.sql = "select * from " + self.tableList[self.tableIdx]
                        rets = self.lookupHeader(self.sql)
                        print(rets)
                        self.columnList = [column for column in rets]
                        self.updateTextList(self.columnList)
                        self.targetSta = targetE.column.name
                else:
                    self.remindText = "input number out of range for {db}"
                    if (len(self.columnList)) == 0:
                        self.actionSta = actionE.add.name
            # TODO table target end
            # TODO column target start
            elif self.targetSta == targetE.column.name:
                if digit < len(self.columnList):
                    self.columnIdx = digit
                    if self.actionSta == actionE.delete.name:
                        self.columnList.pop(digit)
                        self.columnIdx = 0
                        print(self.columnList)
                        self.updateTextList(self.columnList)
                        if len(self.columnList) == 1:
                            self.actionSta == actionE.add.name
                    elif self.actionSta == actionE.add.name:
                        self.remindText = "should input a new db name you want to add."
                    elif self.actionSta == actionE.show.name:
                        self.sql = "select * from " + self.tableList[self.tableIdx]
                        rets = self.lookupHeader(self.sql)
                        print(rets)
                        self.columnList = [column for column in rets]
                        self.updateTextList(self.columnList)
                        self.targetSta = targetE.column.name
                else:
                    self.remindText = "input number out of range for {db}"
                    if (len(self.columnList)) == 0:
                        self.actionSta = actionE.add.name
            # TODO column target end

            elif self.targetSta == targetE.row.name:
                self.targetSta = targetE.table.name
        # TODO input is a string.
        else:
            if self.actionSta == actionE.add.name:
                if self.targetSta == targetE.db.name:
                    self.dbList.append(self.cmdStr)
                    self.dbIdx = len(self.dbList) - 1
                    dblistStr = [db + "\n" for db in self.dbList]
                    fp = open(self.dbListFileName, 'w')
                    fp.writelines(dblistStr)
                    fp.close()
                    self.updateTextList(self.dbList)

                if self.targetSta == targetE.table.name:
                    self.sql = "CREATE TABLE IF NOT EXISTS " + self.cmdStr + " (ID INTEGER PRIMARY KEY)"
                    self.sqlEasy.modify(self.sql)
                    self.tableList.append(self.cmdStr)
                    self.updateTextList(self.tableList)
                    self.tableIdx = len(self.tableList) - 1

                if self.targetSta == targetE.column.name:
                    self.columnName = self.cmdStr
                    self.sql = "alter table " + self.tableList[self.tableIdx] +  " add column " + self.columnName
                    self.sqlEasy.modify(self.sql)

                    self.sql = "select * from " + self.tableList[self.tableIdx]
                    rets = self.lookupHeader(self.sql)
                    print(rets)
                    self.columnList = [column for column in rets]

                    self.updateTextList(self.columnList)
                    self.columnIdx = len(self.columnList) - 1


        self.cmdStr = ""
        self.remindText = f"{self.targetSta}  --  {self.actionSta}"

    def noused(self):
        text = "5"
        if self.targetSta == targetE.db.name:
            if self.actionSta == actionE.show.name:
                a = 0
        # show db list
        if self.dbStatus == dbStatus.selectDb.value:
            self.readDbListFp = open(self.dbListFileName, 'r')
            self.dbList = [db.rstrip() for db in self.readDbListFp.readlines()]
            self.readDbListFp.close()
            self.updateTextList(self.dbList)
            self.dbStatus = dbStatus.selectTable.value
        elif self.dbStatus == dbStatus.selectTable.value:
            i = int(text)
            dbStr = self.dbList[i]
            if (self.sqlEasy != None):
                self.sqlEasy.close()
            self.sqlEasy = SQL_DB(dbStr)
            self.sql = "select * from sqlite_master"
            rets = self.lookup(self.sql)
            self.tableList = [table[2] for table in rets]
            #print(self.tableList)
            self.updateTextList(self.tableList)
            self.dbStatus = dbStatus.showTables.value
        elif self.dbStatus == dbStatus.showTables.value:
            self.dbStatus = dbStatus.selectTable.value
            i = int(text)
            tableName = self.tableList[i]
            #print(tableName)
            self.sql = "select * from " + tableName
            rets = self.lookupHeader(self.sql)
            #print(rets)
            self.columnList = [column for column in rets]
            #print(self.columnList)
            self.updateTextList(self.columnList)
        elif self.dbStatus == dbStatus.selectTable.value:
            self.dbStatus = dbStatus.selectTable.value

    def showInputStr(self):
        self.showTextLine(self.inputStr,(0,self.textBoxPosY))
        self.showTextLine(self.remindText,(0,self.textBoxPosY - 15))
        self.showTextList(0)

    def setTarget(self, target):
        self.target = target

    def setAction(self, action):
        self.action = action

    def setControl(self, control):
        self.control = control

    def pendingCtr(self):
        self.control = controlE.pending.value

    def actCmdCtr(self):
        self.control = controlE.run.value

    def selectDb(self, dbName):
        if (self.sqlEasy != None):
            self.sqlEasy.close()
        self.sqlEasy = SQL_DB(dbName)

    def lookupHeader(self,sql):
        return self.sqlEasy.lookupHeader(sql)

    def updateTextList(self,dbList):
        self.textList = []
        for i in range(0, len(dbList)):
            self.appendTextList(" " + str(i) + "  |  "+ dbList[i])

    def appendTextList(self, text):
        self.textList.append(text)
        #print(self.textList)

    def close(self):
        self.sqlEasy.close()

    def lookup(self,sql):
        return self.sqlEasy.lookup(sql)

    def addFond(self, name, fontPath, size):
        self.fontDict[name] = self.pygame.font.Font(fontPath, size)

    def addImag(self,name,imgPath,aphal):
        self.imgDict[name] = self.pygame.image.load(imgPath)
        if (aphal < 100):
            self.imgDict[name].set_alpha(aphal)

    def resizeImag(self,name,size):
        if(name in self.imgDict.keys()):
            self.imgDict[name] = self.pygame.transform.scale(self.imgDict[name], size)

    def showTextList(self,startY):
        for text in self.textList:
            textStr = text
            self.showTextLine(textStr, (0,startY))
            startY += 15

    def showTextLine(self, textStr, position):
        self.blitText("song",textStr,(255,255,255),position,False)

    def blitText(self,fontName,textStr,color,position,centFlag):
        text = self.fontDict[fontName].render(textStr, True, color)
        w, h = text.get_size()
        if (centFlag):
            posStart = (position[0]-w/2, position[1]-h/2)
        else:
            posStart = position
        self.screen.blit(text, posStart)

    def resetEvent(self):
        self.pressedMouseType = -1

    def needContinue(self):
        return self.continueFlag

    def fillbgColor(self,color):
        self.screen.fill(color)

    def update(self):
        self.pygame.display.update()
        self.fillbgColor(self.backColorList[2])

    def blitImg(self,name,pos):
        self.screen.blit(self.imgDict[name], pos)
    def quitPygameFrame(selfs):
        exit()