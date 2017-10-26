import random
import math
import time
import functools

from collections import defaultdict, Counter


ROUNDS = 100


# Total number of hands
#fact = math.factorial
#color_perms = (fact(3) * fact(2) ** 3) ** 5
#start_perm = fact(5) ** 2
#color_reassign = fact(5)
#print (fact(50) / color_perms / color_reassign / start_perm)

COLORS = ["B", "G", ] #"R", "W", "Y"]
COLOR_INDEX = { color : i for i, color in enumerate(COLORS)}
VALUE_DIST = [1, 1, 1, 2, 2, 3, 3, 4, 4, 5]
MAX_CARD = max(VALUE_DIST)
VALUE_COUNT = [VALUE_DIST.count(v) for v in range(MAX_CARD + 1)]
MAX_SCORE = len(COLORS) * max(VALUE_DIST)

def handString(hand):
    return ", ".join(c + str(n) for c,n in hand)


def st(a):
    return tuple(sorted(a))


def searchRecurseHelper(hand_a, hand_b, deck, board_state, hints, last_turn_status):
    if len(hand_a) < 5:
        if len(deck) > 0:
            hand_a = st(hand_a + deck[-1:])
            deck = deck[:-1]
        else:
            last_turn_status = max(last_turn_status, 0)

    if last_turn_status >= 0:
        last_turn_status += 1

    return searchRecurse(hand_b, hand_a, deck, board_state, hints, last_turn_status)
        

@functools.lru_cache(maxsize = None)
def searchRecurse(hand_a, hand_b, deck, board_state, hints, last_turn_status):
    if all(v == MAX_CARD for v in board_state):
        return (MAX_SCORE, "Played everthing")

    if last_turn_status == 3:
        return (sum(board_state), "End")

    # three actions are Discard, Play, Hint
    best = (0, None)

    # PLAY
    for i, (color, value) in enumerate(hand_a):
        color_index = COLOR_INDEX[color]
        if board_state[color_index] == value-1:
            new_hand = hand_a[:i] + hand_a[i+1:]
            new_board_state = board_state[:color_index] + (value,) + board_state[color_index+1:]
            new_hints = hints + (value == 5)
            best = max(best, searchRecurseHelper(new_hand, hand_a, deck, new_board_state, new_hints, last_turn_status))
            if best == MAX_SCORE:
                return best[0], [best[1], "Play {}".format((color,value))]

    # Hint
    if hints > 0:
        best = max(best, searchRecurseHelper(hand_a, hand_b, deck, board_state, hints-1, last_turn_status))
        if best == MAX_SCORE:
                return best[0], [best[1], "Hint"]

    # Discard
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
        best = max(best, searchRecurseHelper(new_hand, hand_b, deck, board_state, hints+1, last_turn_status))
        if best == MAX_SCORE:
            return best[0], [best[1], "Discard {}".format(hand_a[discard_index])]

#    if best[0] >= MAX_SCORE - 1:
#        print (len(hand_a), len(hand_b), len(deck), last_turn_status, best)

    if searchRecurse.cache_info().misses % 25000 == 0:
        print (searchRecurse.cache_info())

    return best


def search(deck):
    player_one = deck[-5:]
    player_two = deck[-10:-5]

    draw = deck[:-10]

    print (player_one)
    print (player_two)
    print ()
    print (deck)
    print ()

    board_state = [0 for color in COLORS]
    hints = 8

    player_turn = 0
    last_turn = -1

    searchRecurse.cache_clear()
    result = searchRecurseHelper(st(player_one), st(player_two), tuple(deck), tuple(board_state), hints, last_turn)
    print (result)
    return result[0]


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

T1 = time.time()
print ("Generated {} random decks ({:.0f} seconds)".format(len(r_decks), T1 - T0))


dists = defaultdict(list)
for r_i, r_deck in enumerate(r_decks):
    score = search(r_deck)

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


