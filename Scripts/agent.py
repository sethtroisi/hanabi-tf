import abc
import enum

class Agent:
    __metaclass__ = abc.ABCMeta

    def __init__(self, name="Agent"):
        self.name = name
        self.game = None

    def setGame(self, game):
        self.game = game

    @abc.abstractmethod
    def getPlay(self, slot):
        return

    @abc.abstractmethod
    def updateFromAction(self, action):
        return

    @abc.abstractmethod
    def updateFromPartnerAction(self, action):
        return

    def __str__(self):
        return "{}=...".format(
            self.name,
        )
