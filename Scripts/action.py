from enum import Enum


class Action:
    """
        Action performed on a turn
        PLAY, [1-5]
        DISCARD, [1-5]
        HINT_NUMBER, [1-5]
        HINT_COLOR, <COLOR>
    """

    class Action(Enum):
        PLAY = 1
        DISCARD = 2
        HINT_NUMBER = 3
        HINT_COLOR = 4

    def __init__(self, action, index):
        self.action = action
        self.index = index

    @staticmethod
    def play(index):
        return Action(Action.Action.PLAY, index)

    @staticmethod
    def discard(index):
        return Action(Action.Action.PLAY, index)

    @staticmethod
    def hintColor(index):
        return Action(Action.Action.PLAY, index)
