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

#import sqlite3
from datetime import datetime
from sql_db import *
from vocab_set import *
from vocab_show import *
from pygame_frame import *
import pygame
from pygame.locals import *
from pygame.color import THECOLORS
from collections import *
import speech
import threading
#from os import *
import os
import warnings
warnings.filterwarnings('ignore')

def readOutLoudly(sentence:str):
    speech.say(sentence)



if __name__ == '__main__':
    vocabShowInPygame = VOCAB_PYGAME_SHOW('vocabulary.db')
    vocabShowInPygame.wordDetail.next()
    leftClickCnt = 0
    vocabShowInPygame.showVocab((255,255,255), 800/2, leftClickCnt)
    vocabShowInPygame.showRecordInfo("正在学习第" + str(vocabShowInPygame.wordDetail.dataIndex) + "/" + "个单词...",(255,255,255),(0,0))
    vocabShowInPygame.updateDisp()
    t1 = threading.Thread(target=readOutLoudly, args=(vocabShowInPygame.wordDetail.Vocabulary,))
    t1.start()
    pressedMouseType = -1
    mousePosition = 0
    while vocabShowInPygame.pygameFrame.needContinue():
        pressedMouseType = vocabShowInPygame.pygameFrame.checkEvent()
        mousePosition = ((vocabShowInPygame.pygameFrame.pos[0] > 800/2) << 1) | (vocabShowInPygame.pygameFrame.pos[1] > 800/2) + 1
        vocabShowInPygame.wordDetail.updateCnt(mousePosition)
        if pressedMouseType < 0:
            continue
        elif pressedMouseType == 0:
            if t1.is_alive():
                continue
            leftClickCnt = leftClickCnt + 1
            vocabShowInPygame.showVocab((255,255,255), 800 / 2, leftClickCnt)
            vocabShowInPygame.showRecordInfo("正在学习第" + str(vocabShowInPygame.wordDetail.dataIndex) + "/" + "个单词...",(255, 255, 255), (0, 0))
            vocabShowInPygame.updateDisp()
            if leftClickCnt > 1:
                t1 = threading.Thread(target=readOutLoudly, args=(vocabShowInPygame.wordDetail.Sentence,))
                t1.start()
            else:
                t1 = threading.Thread(target=readOutLoudly, args=(vocabShowInPygame.wordDetail.Vocabulary,))
                t1.start()
        elif pressedMouseType == 2:
            if t1.is_alive():
                continue
            vocabShowInPygame.wordDetail.next()
            leftClickCnt = 0
            vocabShowInPygame.showVocab((255, 255, 255), 800 / 2, leftClickCnt)
            vocabShowInPygame.showRecordInfo("正在学习第" + str(vocabShowInPygame.wordDetail.dataIndex) + "/" + "个单词...",(255, 255, 255), (0, 0))
            vocabShowInPygame.updateDisp()
            t1 = threading.Thread(target=readOutLoudly, args=(vocabShowInPygame.wordDetail.Vocabulary,))
            t1.start()
        vocabShowInPygame.pygameFrame.resetEvent()
    sql = "UPDATE counter SET rateProgress="+str(vocabShowInPygame.wordDetail.dataIndex)
    vocabShowInPygame.wordDetail.db.run(sql)
    vocabShowInPygame.wordDetail.db.close()
    vocabShowInPygame.pygameFrame.quitPygameFrame()