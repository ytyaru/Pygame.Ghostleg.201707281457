import pygame
class Screen:
    def __init__(self, width=320, height=240, color=[0,0,0]):
        self.__color = color
        self.__size = (width, height)
        self.__screen = pygame.display.set_mode(self.__size)
    @property
    def Screen(self): return self.__screen
    @property
    def Size(self): return self.__size
    @property
    def Color(self): return self.__color
    def Fill(self): self.__screen.fill(self.__color)

