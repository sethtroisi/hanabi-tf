class Agent:
    def __init__(self, name="Agent"):
        self.name = name
        self.game = None


    def setGame(self, game):
        self.game = game


    def getPlay(self, slot):
        pass


    def otherPlayerMove(self, action):
        pass


    def __str__(self):
        return "{}=...".format(
            self.name,
        )
