import pygame
from pygame.locals import *
from .GameState import GameState
class AnimateState(metaclass=GameState):
    def Initialize(self):
        print('アニメーション開始。')
    def Finalize(self):
        print('アニメーション演出終了。たとえばアニメーションの最中なら強制的に完了した状態にする。')
    def Event(self, event, switcher, command):
        if event.type == KEYDOWN:
            if event.key == K_RETURN or event.key == K_SPACE or event.key == K_z:
                command.EndAnimation()
                switcher.Next()
    def Draw(self, screen): pass
