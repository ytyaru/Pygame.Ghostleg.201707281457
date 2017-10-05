import pygame, sys
from pygame.locals import *
from abc import ABCMeta, abstractmethod
import ui.Screen
import framework.state.StateSwitcher
import framework.command.GameCommand

class Main:
    def __init__(self, title=None):
        self.__title = title
        self.__command = framework.command.GameCommand.GameCommand()
        self.__stateSwitcher = framework.state.StateSwitcher.StateSwitcher()
        self.__command.NewGhostleg()
    def Run(self):
        pygame.init()
        if self.__title: pygame.display.set_caption(self.__title)
        clock = pygame.time.Clock()
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit();
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE: pygame.quit(); sys.exit();
                self.__stateSwitcher.State.Event(event, self.__stateSwitcher, self.__command)
            self.__command.DrawGhostleg()
            self.__command.DrawCursor()
            self.__stateSwitcher.State.Draw(self.__command.Screen.Screen)
            pygame.display.flip()
            clock.tick(60) # 60 FPS


if __name__ == '__main__':
    main = Main(title="あみだくじ")
    main.Run()
