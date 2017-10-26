import random

from agent import Agent


class RandomAgent(Agent):
    NAMES = ["Alyssa", "Ben", "Cooper", "Daisy"]
    HURRY_UP = 0
    MAX_SCORE = 0

    def __init__(self, name=None):
        Agent.__init__(
            self,
            name or RandomAgent._getRandomName())

        self.hand = None
        self.playable = None

    def start(self, hand):
        assert self.game
        assert hand
        self.hand = hand
        self.playable = []

    def getPlay(self, slot):
        # 1. Play any card that has been clued
        # 2. Clue a non-empty set of cards that are all playable
        # 3. Discard

        if self.playable:
            return "PLAY"


        pass

    def otherPlayerAction(self, action):
        pass

    @staticmethod
    def _getRandomName():
        return "RandomAgent-" + random.choice(RandomAgent.NAMES)
