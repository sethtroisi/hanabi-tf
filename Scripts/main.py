#!/usr/bin/env python3

import naive_agent

from table import Table

players = [
    naive_agent.NaiveAgent(),
    naive_agent.NaiveAgent()
]

table = Table(players)

table.start()