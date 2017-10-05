from abc import ABCMeta, abstractmethod
class GameState(type, metaclass=ABCMeta):
    @abstractmethod
    def Initialize(self): raise NotImplementedError()
    @abstractmethod
    def Finalize(self): raise NotImplementedError()
    @abstractmethod
    def Event(self, event, switcher, command): raise NotImplementedError()
    @abstractmethod
    def Draw(self, screen): raise NotImplementedError()
