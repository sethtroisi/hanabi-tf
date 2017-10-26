#!/usr/bin/env python3

import random_agent

from table import Table

players = [
    random_agent.RandomAgent(),
    random_agent.RandomAgent()
]

table = Table(players)

table.start()