from game.Ghostleg import Ghostleg
from game.LinesAnimation import LinesAnimation
from game.PointList import PointList
from game.Cursor import Cursor
from game.GhostlegDrawerPyGame import GhostlegDrawerPyGame
from ui.Screen import Screen
from ui.CalcSize import CalcSize
class GameCommand:
    def __init__(self):
        self.__ghostleg = Ghostleg()
        self.__ghostleg.Create()
        self.__screen = Screen()
        self.__calcSize = CalcSize(self.__ghostleg, self.__screen)
        self.__cursor = Cursor(self.__ghostleg, self.__calcSize, self.__screen)
        self.__drawer = GhostlegDrawerPyGame(self.__ghostleg, self.__calcSize, self.__screen)

    @property
    def Ghostleg(self): return self.__ghostleg
    @property
    def Screen(self): return self.__screen
    @property
    def CalcSize(self): return self.__calcSize
    @property
    def Pointlist(self): return self.__pointlist
    @property
    def LinesAnimation(self): return self.__linesAnimation
    @property
    def Cursor(self): return self.__cursor
    
    def NewGhostleg(self):
        self.__cursor.Clear()
        self.__drawer.Clear()
        self.__ghostleg.Create()
        self.__calcSize.Calculate()
    def SelectCursor(self, event): return self.__cursor.Input(event)
    def DrawGhostleg(self): self.__drawer.Draw()
    def DrawCursor(self): self.__cursor.Draw()
    def StartAnimation(self): self.__drawer.Select(self.__cursor.SelectedIndex)
    def Animation(self): self.__drawer.Draw()
    def EndAnimation(self):
        self.__drawer.FinishAnimation()
        print('EndAnimation()')
    def StartGoalPerformance(self):
        print('StartGoalPerformance()')
    def EndGoalPerformance(self):
        print('EndGoalPerformance()')
