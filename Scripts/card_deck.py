from enum import IntEnum
import functools
import random


class Color(IntEnum):
    WHITE = 1
    YELLOW = 2
    BLUE = 3
    RED = 4
    GREEN = 5


class Number(IntEnum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


@functools.total_ordering
class Card:
    def __init__(self, color, number):
        self._color = color
        self._number = number
        assert self._color in Color
        assert self._number in Number

    def getColor(self):
        return self._color

    def getNumber(self):
        return self._number

    def getState(self):
        return self._color, self._number

    def matches(self, color, number):
        assert (color is None) ^ (number is None)

        if number:
            return self._number == number
        if color:
            return self._color == color

    def __repr__(self):
        return "Card({}, {})".format(self.color, self.number)

    def __eq__(self, other):
        return (self.number, self.color) == (other.number, other.color)

    def __lt__(self, other):
        return (self.number, self.color) < (other.number, other.color)

    def __hash__(self):
        return self.number * len(self.COLORS) + self.color


# TODO take in the permutation numbering instead of seed
class Deck:
    def __init__(self, seed):
        self.seed = seed
        self.index = 0
        self.cards = None
        self.reset()

    def reset(self):
        r = random.Random(self.seed)
        self.cards = [Card(color, number) for color in Color for number in Number]
        r.shuffle(self.cards)
        self.index = 0

    def draw(self):
        self.index += 1
        return self.cards[self.index - 1]

    def __len__(self):
        return len(self.cards)

    def getState(self):
        return self.seed, self.index

    def setState(self, status):
        self.seed = status[0]
        self.reset()
        self.index = status[1]
