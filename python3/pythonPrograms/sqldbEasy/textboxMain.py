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

if __name__ == '__main__':
    screenWidth = 1200
    screenHight = 800
    textBoxHeight = 15
    showApp = PYGAME_FRAME(pygame, screenWidth, screenHight, "titleName", textBoxHeight)
    flag = 0
    retStr = ""

    whileFlag = True
    while whileFlag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                whileFlag = False # TODO: Quit the while loop
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                showApp.keyEvent(event) # TODO: Set and clean Key information
        if (showApp.isKeyAgain()):
            showApp.updateInputStr()
        showApp.constructCmd()
        showApp.showInputStr()
        showApp.update()

    showApp.close()
    exit()
