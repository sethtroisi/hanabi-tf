import random
import functools

@functools.total_ordering
class Card:
    COLORS = ["White", "Yellow", "Blue", "Red", "Green"] 
    NUMBERS = [1, 2, 3, 4, 5]
    
    def __init__(self, color, number):
        self.color = color
        self.number = number
        assert self.color in Card.COLORS
        assert self.number in Card.NUMBERS

    def getColor(self):
        return self.color

    def getNumber(self):
        return self.number

    def getState(self):
        return (self.color, self.number)

    def matches(self, color, number):
        assert (color == None) ^ (number == None)
        
        if number != None:
            return self.number == number
        if color != None:
            return self.color == color

    def __repr__(self):
        return "Card({}, {})".format(self.color, self.number)

    def __eq__(self, other):
        return (self.number, self.color) == (other.number, other.color)
    
    def __lt__(self, other):
        return (self.number, self.color) < (other.number, other.color)

    def __hash__(self):
        return self.NUMBERS.index(self.number) * len(self.COLORS) + \
               self.COLORS.index(self.color)


# TODO take in the permutation numbering instead of seed
class Deck:
    def __init__(self, seed):
        self.seed = seed
        self.index = 0
        self.reset()

    def reset(self):
        r = random.Random()
        r.seed(self.seed)
        self.cards = [Card(color, number) for color in Card.COLORS for number in Card.NUMBERS]
        r.shuffle(self.cards)
        self.index = 0

    def draw(self):
        self.index += 1
        return self.cards[self.index - 1]

    def __len__(self):
        return len(self.cards)

    def getState(self):
        return (self.seed, self.index)

    def setState(self, status):
        self.seed = status[0]
        self.reset()
        self.index = status[1]
