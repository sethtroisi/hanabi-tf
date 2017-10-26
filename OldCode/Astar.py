import random
import math
import time
import functools
import heapq

from collections import defaultdict, Counter


ROUNDS = 100

COLORS = ["B", "G", "R", "W", "Y"]
COLOR_INDEX = { color : i for i, color in enumerate(COLORS)}
VALUE_DIST = [1, 1, 1, 2, 2, 3, 3, 4, 4, 5]
MAX_CARD = max(VALUE_DIST)
VALUE_COUNT = [VALUE_DIST.count(v) for v in range(MAX_CARD + 1)]
MAX_SCORE = len(COLORS) * max(VALUE_DIST)

DEAD_CARD = ("B", 0)


def handString(hand):
    return ", ".join(c + str(n) for c,n in hand)


def st(a):
    return tuple(sorted(a))


def getNewRemaining(r, color_index, value):
    return r[:color_index] + (r[color_index][:value] + (r[color_index][value] - 1,) + r[color_index][value + 1:],) + r[color_index+1:]
    


def getNextState(hand_a, hand_b, deck, board_state, remaining, hints, turn, last_turn_status):
    if len(hand_a) < 5:
            if len(deck) > 0:
                hand_a = hand_a + deck[-1:]
                deck = deck[:-1]

            # ALL BORING CARDS ARE MARKED AS THE SAME
            hand_a = st((color, value) if board_state[COLOR_INDEX[color]] < value else DEAD_CARD
                           for (color, value) in hand_a)

            hand_b = st((color, value) if board_state[COLOR_INDEX[color]] < value else DEAD_CARD
                           for (color, value) in hand_b)


            if len(deck) == 0:
                last_turn_status = max(last_turn_status, 0)

    if last_turn_status >= 0:
        last_turn_status += 1


    # turns + 1 breaks memoriszations
    return (hand_b, hand_a, deck, board_state, remaining, hints, turn, last_turn_status)


def getChildren(state):
    hand_a, hand_b, deck, board_state, remaining, hints, turn, last_turn_status = state
    assert len(hand_a) == 5 or last_turn_status >= 2

    if all(v == MAX_CARD for v in board_state):
        yield (MAX_SCORE,)
        return

    if last_turn_status == 3:
        yield (sum(board_state),)
        return

#    print (turn, [color + str(value) for color, value in zip(COLORS, board_state)],
#           "\t", hand_a, "\t\t", hand_b)

    # PLAY
    for i, (color, value) in enumerate(hand_a):
        color_index = COLOR_INDEX[color]
        if board_state[color_index] == value - 1:
            new_hand = hand_a[:i] + hand_a[i+1:]
            new_board_state = board_state[:color_index] + (value,) + board_state[color_index+1:]
            new_remaining = getNewRemaining(remaining, color_index, value)
            new_hints = hints + (value == 5)
            yield getNextState(new_hand, hand_b, deck, new_board_state, new_remaining, new_hints, turn, last_turn_status)

    # Discard
    #'''
    free_discard = None
    for i, (color, value) in enumerate(hand_a):
        if board_state[COLOR_INDEX[color]] >= value:
            free_discard = i
            break
    else:
        hand_count = Counter(hand_a)
        card, count = hand_count.most_common(1)[0]
        if count > 1:
            free_discard = hand_a.index(card)

    # TODO: consider not recursing if it ruins the game
    consider_discarding = (free_discard,) if free_discard != None else range(len(hand_a))
    for discard_index in consider_discarding:
        new_hand = hand_a[:discard_index] + hand_a[discard_index+1:]
        new_remaining = getNewRemaining(remaining, color_index, value)
        yield getNextState(new_hand, hand_b, deck, board_state, new_remaining, hints+1, turn, last_turn_status)
    #'''

    # Hint
    #'''
    if hints > 0:
        yield getNextState(hand_a, hand_b, deck, board_state, remaining, hints-1, turn, last_turn_status)
    #'''

def initialState(deck):
    player_one = deck[-5:]
    player_two = deck[-10:-5]
    draw = deck[:-10]

    board_state = [0 for color in COLORS]
    remaining = [tuple(VALUE_COUNT) for color in COLORS]
    hints = 8

    turn = 0
    last_turn = -1

    return st(player_one), st(player_two), tuple(draw), tuple(board_state), tuple(remaining), hints, turn, last_turn

# Always OVER states the possible score
def metric(state):
    hand_a, hand_b, deck, board_state, remaining, hints, turn, last_turn_status = state

    # Current Score
    g = sum(board_state)

    # Max amount that can be added
    h1 = len(deck) + 2

    # Number of alive cards remaining
    h2 = 0
    # Count of alive cards
    h3 = 0
    for b_state, r_state in zip(board_state, remaining):
        for v in range(b_state + 1, 6):
            if r_state[v] == 0:
                break
            h2 += 1
            h3 += r_state[v]

    # We evaluate highest metric states so prioritise having played more cards
    return g + min(h1, h2) + 1 / (h3 + 2)


def aStar(deck):
    iState = initialState(deck)
    startState = (-metric(iState), iState)

    seen = set([iState])
    openStates = [startState]
    parent = {iState : None}

    bestScore = 0
    bestState = None

    iteration = 0
    while bestScore < (MAX_SCORE-1) and len(openStates) > 0:
        iteration += 1
        score, state = heapq.heappop(openStates)
        if -score <= bestScore:
            return bestScore

        if iteration % 10000 == 0:
            print ("\t", bestScore, len(openStates), len(seen), "\t", score, sum(state[3]))

        for child in getChildren(state):
            if child not in seen:
                if len(child) == 1:
                    childScore = child[0]
                    if childScore > bestScore:
                        bestScore = childScore
                        bestState = state
                    continue
                
                seen.add(child)
                heapq.heappush(openStates, (-metric(child), child))
                parent[child] = state

    '''
    trail = bestState
    while trail != None:
        hand_a, hand_b, deck, board_state, hints, turn, last_turn_status = trail
        print ("{},  {} cards, {} hints\t\t{}\t{}\t\ttop: {}".format(
            handString(zip(COLORS, board_state)),
            len(deck), hints, handString(hand_a), handString(hand_b),
            None if len(deck) == 0 else deck[-1]))
        trail = parent[trail]
    #'''

    return bestScore


T0 = time.time()

sorted_deck = []
for color in COLORS:
    for value in VALUE_DIST:
        sorted_deck.append( (color, value) )


random.seed(10)

r_decks = []
for i in  range(ROUNDS):
    r_deck = sorted_deck[:]
    random.shuffle(r_deck)
    r_decks.append(tuple(r_deck))

#print ("bestScore:", aStar(r_decks[0]))

T1 = time.time()
print ("Generated {} random decks ({:.0f} seconds)".format(len(r_decks), T1 - T0))

dists = defaultdict(list)
for r_i, r_deck in enumerate(r_decks):
    score = aStar(r_deck)
    print (r_i, score)
    dists[score].append(r_i)

T2 = time.time()

avg = 0
for score in range(0, MAX_SCORE+1):
    count = len(dists[score])
    avg += score * count

    if count > 0:
#        if score < 20:
#            print ("\n".join(str(r_decks[r_i]) for r_i in dists[score]))
        print (score, "\t", count)

avg /= len(r_decks)

print ("avg score:", avg)
print ("win rate ({}): {}".format(MAX_SCORE, len(dists[MAX_SCORE]) / len(r_decks)))
print ("\t{:.2f} seconds ({:.5f} games / second)".format(T2 - T1, len(r_decks) / (T2 - T1)))

#'''


