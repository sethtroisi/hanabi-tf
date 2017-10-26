class Agent:
    def __init__(self, game, name="None"):
        self.game = game
        self.name = name or "Agent"


    def getPlay(self, slot):
        pass


    def otherPlayerMove(self, action):
        pass


    def __str__(self):
        return "{}=...".format(
            self.name,
        )
