# 選択肢からゴールまでの頂点リストを生成する
class PointList:
    def __init__(self, ghostleg, calcSize, screen):
        self.__ghostleg = ghostleg
        self.__calcSize = calcSize
        self.__screen = screen
        self.__to_goal_pointlist = None # ゴールまでの頂点リスト（self.__legから生成する）

    @property
    def PointList(self): return self.__to_goal_pointlist

    # 選択肢からゴールまでの頂点リストを生成する
    def Create(self, select_line_index):
        self.__to_goal_pointlist = None
        self.__to_goal_pointlist = []
        now_line_index = select_line_index
        x = self.__get_leg_index_first_horizon_line(now_line_index, 0)
        self.__to_goal_pointlist.append([self.__calcSize.StartPoint[0] + now_line_index * self.__calcSize.WidthInterval, self.__calcSize.StartPoint[1]])
        for y in range(len(self.__ghostleg.Ghostleg[0])):
            if 0 == now_line_index:
                if 1 == self.__ghostleg.Ghostleg[now_line_index][y]: # └
                    self.__set_pointlist_value(now_line_index, y+1)
                    self.__append_point(now_line_index+1, y+1)
                    now_line_index += 1
                else: # │
                    self.__set_pointlist_value(now_line_index, y+1)
                    self.__append_point(now_line_index, y+2)
            elif len(self.__ghostleg.Ghostleg) == now_line_index:
                if 1 == self.__ghostleg.Ghostleg[now_line_index-1][y]: # ┘
                    self.__set_pointlist_value(now_line_index, y+1)
                    self.__append_point(now_line_index-1, y+1)
                    now_line_index += -1
                else: # ｜
                    self.__set_pointlist_value(now_line_index, y+1)
                    self.__append_point(now_line_index, y+2)
            else:
                if 1 == self.__ghostleg.Ghostleg[now_line_index][y]: # └
                    self.__set_pointlist_value(now_line_index, y+1)
                    self.__append_point(now_line_index+1, y+1)
                    now_line_index += 1
                elif 1 == self.__ghostleg.Ghostleg[now_line_index-1][y]: # ┘                
                    self.__set_pointlist_value(now_line_index, y+1)
                    self.__append_point(now_line_index-1, y+1)
                    now_line_index += -1
                else: # ｜
                    self.__set_pointlist_value(now_line_index, y+1)
                    self.__append_point(now_line_index, y+2)
        self.__to_goal_pointlist.append([self.__to_goal_pointlist[-1][0], self.__screen.Size[1] - (self.__calcSize.FontPixcelSize * self.__calcSize.GoalStrMaxLen)])
        print(self.__to_goal_pointlist)
        return self.__to_goal_pointlist

    # 1つ前のと同じ座標ならセットしない
    def __set_pointlist_value(self, now_line_index, y):
        if (self.__to_goal_pointlist[-1][0] != self.__calcSize.StartPoint[0] + now_line_index * self.__calcSize.WidthInterval
            or self.__to_goal_pointlist[-1][1] != self.__calcSize.StartPoint[1] + (y * self.__calcSize.HeightInterval)):
            self.__append_point(now_line_index, y)

    def __append_point(self, now_line_index, y):
        self.__to_goal_pointlist.append(self.__get_pos(now_line_index, y))

    def __get_pos(self, xi, yi): return [self.__calcSize.StartPoint[0] + xi * self.__calcSize.WidthInterval, self.__calcSize.StartPoint[1] + yi * self.__calcSize.HeightInterval]
    
    def __get_last_pos(self, xi): return [self.__calcSize.StartPoint[0] + xi * self.__calcSize.WidthInterval, self.__screen.Size[1] - self.__calcSize.FontPixcelSize * self.__calcSize.GoalStrMaxLen]

    def __get_leg_index_first_horizon_line(self, now_line_index, horizon_start_index):
        if 0 == now_line_index: return now_line_index
        elif len(self.__ghostleg.Ghostleg) == now_line_index: return now_line_index-1
        else:
            for h in range(horizon_start_index, len(self.__ghostleg.Ghostleg[0])):
                if 1 == self.__ghostleg.Ghostleg[now_line_index][h]:return now_line_index
                elif 1 == self.__ghostleg.Ghostleg[now_line_index-1][h]: return now_line_index-1
            return now_line_index # 左右のlegとも横線が1本もない場合

