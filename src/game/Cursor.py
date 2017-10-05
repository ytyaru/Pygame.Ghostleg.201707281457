from pygame.locals import *
class Cursor:
    def __init__(self, ghostleg, calcSize, screen):
        self.__select_index = 0
        self.__cursor_character = '▼'
        self.__ghostleg = ghostleg
        self.__screen = screen
        self.__calcSize = calcSize
    @property
    def SelectedIndex(self): return self.__select_index
    @property
    def CursorCharacter(self): return self.__cursor_character
    def Clear(self): self.__select_index = 0
    def Input(self, event):
        if event.type == KEYDOWN:  # キーを押したとき
            if event.key == K_LEFT or event.key == K_a:
                self.__select_index = self.__select_index-1 if 0 < self.__select_index else len(self.__ghostleg.Goals)-1
            if event.key == K_RIGHT or event.key == K_d:
                self.__select_index = self.__select_index+1 if self.__select_index < len(self.__ghostleg.Goals)-1 else 0
            if event.key == K_RETURN or event.key == K_SPACE or event.key == K_z:
                return True
        return False
                
    def Draw(self):
        self.__screen.Screen.blit(self.__calcSize.Font.render(self.__cursor_character, False, self.__calcSize.LineColor), self.__get_last_pos(self.__select_index))
        
    def __get_last_pos(self, xi): return [self.__calcSize.StartPoint[0] + (xi * self.__calcSize.WidthInterval) - (self.__calcSize.LineWidth / 2), 0]
