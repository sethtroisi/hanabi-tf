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


    def otherPlayerAction(self, action):
        return

    def __str__(self):
        return "{}=...".format(
            self.name,
        )
