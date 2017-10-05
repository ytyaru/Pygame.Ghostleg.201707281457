#!python3.6
import sys, pathlib, copy, pygame
from .PointList import PointList
from .LinesAnimation import LinesAnimation

# あみだくじを描画する
class GhostlegDrawerPyGame:
    def __init__(self, ghostleg, calcSize, screen):
        self.__leg = None
        self.__ghostleg = ghostleg
        self.__screen = screen
        self.__width = 8
        self.__color = (255,255,255)
        self.__select_line_color = (255,0,0)
        self.__select_line_width = 2
        self.__linesanim = None
        self.__calcSize = calcSize
        self.__pointlist = None
        self.__font = pygame.font.Font(str(pathlib.Path('../res/font/mplus-1m-regular.ttf').resolve()), 12)
#        print(pygame.font.get_fonts()) # 使えるフォント名

    def Clear(self):
        self.__pointlist = None
        self.__linesanim = None

    def Select(self, select_line_index):
        if len(self.__ghostleg.Ghostleg) < select_line_index: raise Exception('select_line_indexは {} 以下にして下さい。'.format(len(self.__ghostleg.Ghostleg)))
        self.__pointlist = PointList(self.__ghostleg, self.__calcSize, self.__screen)
        self.__pointlist.Create(select_line_index)
        self.__linesanim = LinesAnimation(self.__pointlist.PointList, self.__select_line_color, self.__select_line_width)
    
    # あみだくじを描画する
    def Draw(self):
        self.__screen.Fill()
        self.__draw_vartical_lines()
        self.__draw_horizon_lines()
        self.__draw_goals()
        self.__draw_select_lines()

    # アニメーションを即時完了させる
    def FinishAnimation(self): self.__linesanim.Finish()

    def __draw_vartical_lines(self):
        for xi in range(len(self.__ghostleg.Ghostleg)+1):
            start = self.__get_pos(xi, 0)
            end = self.__get_last_pos(xi)
            pygame.draw.line(self.__screen.Screen, self.__color, start, end, self.__width)

    def __draw_goals(self):
        if self.__linesanim and self.__linesanim.IsFinished():
            for i in range(len(self.__ghostleg.Goals)):
                self.__screen.Screen.blit(self.__font.render(self.__ghostleg.Goals[i], False, self.__color), self.__get_goal_pos(i))

    def __draw_horizon_lines(self):
        for yi in range(len(self.__ghostleg.Ghostleg[0])):
            for xi in range(len(self.__ghostleg.Ghostleg)):
                if 1 == self.__ghostleg.Ghostleg[xi][yi]:
                    start = self.__get_pos(xi, yi+1)
                    end = self.__get_pos(xi+1, yi+1)
                    pygame.draw.line(self.__screen.Screen, self.__color, start, end, self.__width)

    def __get_leg_index_first_horizon_line(self, now_line_index, horizon_start_index):
        if 0 == now_line_index: return now_line_index
        elif len(self.__ghostleg.Ghostleg) == now_line_index: return now_line_index-1
        else:
            for h in range(horizon_start_index, len(self.__ghostleg.Ghostleg[0])):
                if 1 == self.__ghostleg.Ghostleg[now_line_index][h]:return now_line_index
                elif 1 == self.__ghostleg.Ghostleg[now_line_index-1][h]: return now_line_index-1
            return now_line_index # 左右のlegとも横線が1本もない場合

    def __get_pos(self, xi, yi): return [self.__calcSize.StartPoint[0] + xi * self.__calcSize.WidthInterval, self.__calcSize.StartPoint[1] + yi * self.__calcSize.HeightInterval]
    
    def __get_last_pos(self, xi): return [self.__calcSize.StartPoint[0] + xi * self.__calcSize.WidthInterval, self.__screen.Size[1] - self.__calcSize.FontPixcelSize * self.__calcSize.GoalStrMaxLen]

    def __get_goal_pos(self, xi):
        return [
            self.__calcSize.StartPoint[0] + (xi * self.__calcSize.WidthInterval) - (self.__calcSize.Font.size(self.__ghostleg.Goals[xi])[0] / 2) + (self.__calcSize.LineWidth / 2),
            self.__screen.Size[1] - self.__calcSize.FontPixcelSize * self.__calcSize.GoalStrMaxLen]

    def __draw_select_lines(self):
        if self.__pointlist:
            if self.__linesanim:
                self.__linesanim.Draw(self.__screen.Screen)
