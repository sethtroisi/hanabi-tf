#!/usr/bin/env python3

import random

import Game
import NaiveAgent


seed = random.random()
game = Game.Game(seed)
players = [
    NaiveAgent.NaiveAgent(game),
    NaiveAgent.NaiveAgent(game)
]
