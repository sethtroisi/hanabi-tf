import random

from game import Game

# TODO getState(): string
# TODO loadState(string)
# investigate jsonpickle
# TODO get/set Note(player, turn)

class Table:
    PLAYERS = 2
    
    def __init__(self, agents):
        self.seed = random.random()
        self.players = agents
        self.game = Game(self.seed)


    #### ACTIONS ####
    def start(self):
        # TODO main loop
        pass

    def getResult(self):
        return (self.game.getScore(), self.game.getState())