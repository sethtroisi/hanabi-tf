from card_deck import Color, Card, Deck

# TODO getState(): string
# TODO loadState(string)
# investigate jsonpickle
# TODO get/set Note(player, turn)


class Game:
    PLAYERS = 2

    STARTING_HINTS = 8
    STARTING_BLANKS = 4

    HAND_SIZE = 5

    def __init__(self, seed):
        self.players = 2

        # status Vars
        self.result = None
        self.turn = 0
        self.toPlay = 0
        self.remainingTurns = None

        self.hints = Game.STARTING_HINTS
        self.blanksLeft = Game.STARTING_BLANKS

        self.deck = Deck(seed)
        self.deck.reset()

        self.piles = dict((color, 0) for color in Color)
        self.discards = []

        self.hands = [[self.deck.draw() for _ in range(self.HAND_SIZE)]
                      for _ in range(self.players)]

        self.actions = []

    def play(self, slot):
        assert self.result is None
        assert self.remainingTurns != 0

        card = self.__pop(slot)
        if self.piles[card.getColor()] == card.getNumber() - 1:
            self.piles[card.getColor()] = card.getNumber()
            self.actions.append("Successfully played {} from slot {}".format(card, slot))
        else:
            self.discards.append(card)
            self.blanksLeft -= 1
            self.actions.append("Failed to play {} from slot {}".format(card, slot))
            if self.blanksLeft < 0:
                self.__end()

        self.__draw()
        self.__advanceTurn()

    def discard(self, slot):
        assert self.result is None
        assert self.remainingTurns != 0

        card = self.__pop(slot)
        self.discards.append(card)
        self.hints = min(self.hints, Game.STARTING_HINTS)
        self.actions.append("Discarded {} from slot {} (now have {} hints)".format(
                                card, slot, self.hints))

        self.__draw()
        self.__advanceTurn()

    def hint(self, otherPlayer, color, number):
        assert self.result is None
        assert self.remainingTurns != 0
        assert self.hints > 0

        assert (color is None) ^ (number is None)

        otherPlayerHand = self.hands[otherPlayer]
        slots = [i for i, card in otherPlayerHand if card.matches(color, number)]
        assert slots, "Can't give empty hint {} to {}".format(
            (color, number), otherPlayerHand
        )
        self.hints -= 1
        self.actions.append("Player {} hinted Player {} that slots {} are {}".format(
                                self.toPlay, otherPlayer, slots, color or number))
        self.__advanceTurn()

    def __pop(self, slot):
        assert self.toPlay < self.players

        hand = self.hands[self.toPlay]
        assert 0 <= slot < len(hand)
        card = hand.pop(slot)
        return card

    def __draw(self):
        assert self.toPlay < self.players

        if len(self.deck) > 0:
            newCard = self.deck.draw()
            self.hands[self.toPlay].append(newCard)

            if len(self.deck) == 0:
                self.remainingTurns = self.players
                # Log to UI that game is ending soon

    def __advanceTurn(self):
        self.turn += 1
        self.toPlay = self.turn % self.players
        if self.remainingTurns:
            self.remainingTurns -= 1
            if self.remainingTurns == 0:
                self.__end()

    def __end(self):
        self.result = self.getScore()
        self.actions.append("Game Ended with score {}".format(self.getScore()))

    def canHint(self):
        return self.hints > 0

    def getScore(self):
        return sum(self.piles.values())

    def maxScore(self):
        # TODO improve based on discards
        return len(Card.COLORS) * len(Card.NUMBERS)

    def __str__(self):
        return self.status(False)

    def getState(self):
        return (
            self.players, self.result, self.turn, self.toPlay,
            self.remainingTurns, self.hints, self.blanksLeft,
            self.deck.getState(),
            tuple(self.piles.items()),
            tuple(card.getState() for card in self.discards),
            tuple(tuple(card.getState() for card in hand) for hand in self.hands),
            tuple(self.actions))

    def status(self, printHands=False):
        statusLines = list()
        statusLines.append("Game with {} players, turn {}, player {} to play"
                           .format(self.players, self.turn, self.toPlay))

        statusLines.append("\t" + " ".join(sorted(self.piles.items())))

        statusLines.append("\thints: {}, blanks: {}, cards left: {}".format(
            self.hints, self.blanksLeft, len(self.deck)))

        statusLines.append("")
        statusLines.append("\tActions:")
        statusLines += map(lambda a: "\t\t" + str(a), self.actions)

        statusLines.append("")
        statusLines.append("\tDiscards:")
        statusLines += map(lambda c: "\t\t" + str(c), self.discards)

        if printHands:
            statusLines.append("")
            statusLines.append("\tHands:")
            for i, hand in enumerate(self.hands):
                statusLines += "\t\tPlayer {}: {}".format(i, ", ".join(map(str, hand)))

        resultLine = "Result: {} (Score: {})".format(self.result, self.getScore())
        if not self.remainingTurns:
            resultLine += " {} turns remaining".format(self.remainingTurns)
        statusLines.append(resultLine)

        return "\n".join(statusLines)


'''
g = Game()
print (g)
print ()
print ("----------------------")

g.hint(1, None, 1)
print (g)
print ()
print ("----------------------")

g.play(0)
print (g)
print ()
print ("----------------------")
#'''
