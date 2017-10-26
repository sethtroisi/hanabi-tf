import random

from Agent import Agent


class NaiveAgent(Agent):
    NAMES = ["Alyssa", "Ben", "Cooper", "Daisy"]
    HURRY_UP = 0
    MAX_SCORE = 0

    def __init__(self, game, name=None):
        Agent.__init__(
            self,
            game,
            name or NaiveAgent._getRandomName())


    @staticmethod
    def _getRandomName():
        return "NaiveAgent-" + random.choice(NaiveAgent.NAMES)

    def getPlay(self, slot):
        pass


    def otherPlayerMove(self, action):
        pass
