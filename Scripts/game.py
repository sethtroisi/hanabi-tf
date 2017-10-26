import random

from card_deck import Card, Deck

# TODO getState(): string
# TODO loadState(string)
# investigate jsonpickle
# TODO get/set Note(player, turn)

class Game:
    STARTING_HINTS = 8
    STARTING_BLANKS = 4

    HAND_SIZE = 5
    
    def __init__(self, seed):
        # TODO support more players
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

        self.piles = dict((color,0) for color in Card.COLORS)
        self.discards = []

        self.hands = [[self.deck.draw() for card in range(self.HAND_SIZE)]
                          for player in range(self.players)]
 
        self.actions = []


    #### ACTIONS ####
    def play(self, slot):
        assert self.result == None
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
        assert self.result == None
        assert self.remainingTurns != 0
        
        card = self.__pop(slot)
        self.discards.append(card)
        self.hints = min(self.hints, Game.STARTING_HINTS)
        self.actions.append("Discarded {} from slot {} (now have {} hints)".format(
                                card, slot, self.hints))

        self.__draw()
        self.__advanceTurn()        

    def hint(self, otherPlayer, color, number):
        assert self.result == None
        assert self.remainingTurns != 0
        assert self.hints > 0

        assert (color == None) ^ (number == None)

        otherPlayerHand = self.hands[otherPlayer]
        slots = [i for i in range(Game.HAND_SIZE)
                             if otherPlayerHand[i].matches(color, number)]
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


    def __end(self, result):
        self.reult = self.maxScore()
        self.actions.append("Game Ended with score {}".format(self.getScore()))


    #### END ACTIONS ####
    def canHint(self):
        return self.hints > 0

    def getScore(self):
        return sum(self.piles.values())

    def maxScore(self):
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

    def status(self, printHands = False):
        statusLines = []
        statusLines.append("Game with {} players, turn {}, player {} to play"
            .format(self.players, self.turn, self.toPlay))

        statusLines.append("\t" + " ".join(map(lambda c: "{}: {}".format(c, self.piles[c]),
            Card.COLORS)))

        statusLines.append("\thints: {}, blanks: {}, cards left: {}".format(
            self.hints, self.blanksLeft, len(self.deck)))

        statusLines.append("")
        statusLines.append("\tActions:")
        statusLines += map(lambda a : "\t\t" + str(a), self.actions)

        statusLines.append("")
        statusLines.append("\tDiscards:")
        statusLines += map(lambda c : "\t\t" + str(c), self.discards)

        if printHands:
            statusLines.append("")
            statusLines.append("\tHands:")
            statusLines += map(lambda p: "\t\tPlayer {}: {}".format(
                                                p[0], ", ".join(map(str, p[1]))),
                                    enumerate(self.hands))


        resultLine = "Result: {} (Score: {})".format(self.result, self.getScore())
        if self.remainingTurns != None:
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
