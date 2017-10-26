#!/usr/bin/env python3

import random

import game
import naive_agent


seed = random.random()
game = game.Game(seed)
players = [
    naive_agent.NaiveAgent(game),
    naive_agent.NaiveAgent(game)
]
