import pygame
from pygame.locals import *
from .GameState import GameState
class SelectState(metaclass=GameState):
    def __init__(self):
        print(dir(self))
    def Initialize(self):
        print('あみだくじ新規作成。')
    def Finalize(self): pass
    def Event(self, event, switcher, command):
        if command.SelectCursor(event):
            command.StartAnimation() # 本当はAnimateState.Initializeで実行したいが、commandが渡せない
            switcher.Next()
    def Draw(self, screen): pass
