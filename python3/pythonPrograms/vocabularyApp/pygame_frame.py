import pygame
from pygame.locals import *
from pygame.color import THECOLORS

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
        self.pos = (0,0)
        self.pressedMouseType = -1
        self.continueFlag = True

    def pygameFrameInit(self):
        self.addImag("BG","bg.jpg",80)
        self.resizeImag("BG",(800,1500))
        self.addFond("font1",'fonts/msyh.ttc', 35)
        self.addFond("font2",'fonts/arial.ttf', 30)
        self.addFond("font3",'fonts/msyh.ttc', 15)

    def addFond(self, name, fontPath, size):
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
    def checkEvent(self):
        pygame = self.pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.continueFlag = False
            elif event.type == MOUSEBUTTONDOWN:
                self.continueFlag = True
                pressed_array = pygame.mouse.get_pressed()
                for index in range(len(pressed_array)):
                    if pressed_array[index]:
                        self.pressedMouseType = index
                        if (index == 2):
                            self.pos = pygame.mouse.get_pos()
        return self.pressedMouseType
    def resetEvent(self):
        self.pressedMouseType = -1

    def needContinue(self):
        return self.continueFlag

    def fillbgColor(self,color):
        self.screen.fill(color)

    def blitImg(self,name,pos):
        self.screen.blit(self.imgDict[name], pos)
    def quitPygameFrame(selfs):
        exit()