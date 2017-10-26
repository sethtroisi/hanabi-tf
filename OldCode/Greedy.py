import random
import math
import time

from collections import defaultdict


ROUNDS = 60000


# Total number of hands
#fact = math.factorial
#color_perms = (fact(3) * fact(2) ** 3) ** 5
#start_perm = fact(5) ** 2
#color_reassign = fact(5)
#print (fact(50) / color_perms / color_reassign / start_perm)


COLORS = ["B", "G", "R", "W", "Y"]
VALUE_DIST = [1, 1, 1, 2, 2, 3, 3, 4, 4, 5]
VALUE_COUNT = [VALUE_DIST.count(v) for v in range(max(VALUE_DIST)+1)]
MAX_SCORE = len(COLORS) * max(VALUE_DIST)


def hand_string(hand):
    return ", ".join(c + str(n) for c,n in hand)


def reduce_hand(hand):
    color_map = {}

    reduced_hand = []
    for c, v in hand:
        if c not in color_map:
            color_map[c] = COLORS[len(color_map)]           
        mapped_color = color_map[c]
        reduced_hand.append( (mapped_color, v) )

    return tuple(reduced_hand)


failure = defaultdict(int)
def greedy_v4(deck):
    player_one = deck[:5]
    player_two = deck[5:10]

    # It's awkward but because we pop, we need to reverse this list
    draw = list(reversed(deck[10:]))

    board_state = {color : 0 for color in COLORS}
    remaining = {color : VALUE_COUNT[:] for color in COLORS}

    color_order = {color : [] for color in COLORS}
    for color, value in deck:
        color_order[color].append(value)

    # TODO account for having some cards already in hand (ie out of order)

    # A simple suit is one where a 1,2,3,4 appear in that order
    # The rules for that suit become simple:
    #   1. if you can play it, play it.
    #   2. if it's a five save it
    #   3. discard it

    # 60%+ of the time one or two simple suits exist
    # 15% of the time none exists
    #simple_suits = set()
    #for color in COLORS:
    #    played = 0
    #    for value in color_order[color]:
    #        if value == played + 1:
    #            played += 1
    #    if played >= 4:
    #        simple_suits.add(color)

    hints = 8
    fuses = 2 # the number you can use without ending the game

    player_turn = 0
    last_turn = -1

    live_discards = 0
    forced_discards = 0

    stall_priority = 0

#    print ("P1: {}".format(player_one))
#    print ("P2: {}".format(player_two))
#    print ("deck: {}".format(deck))

    while True:
        hand = player_one if player_turn == 0 else player_two
        partner_hand = player_two if player_turn == 0 else player_one

        #hand_count_playable = sum((board_state[color] == value - 1) for color, value in hand)
        partner_has_playable = any((board_state[color] == value - 1) for color, value in partner_hand)

        #hand_count_saving = sum((remaining[color][value] == 1 and board_state[color] != value - 1) for color, value in hand)
        #partner_count_saving = sum((remaining[color][value] == 1 and board_state[color] != value - 1) for color, value in hand)

        # plays newest card that can be played
        play_choice = (100, None)
        for i, card in enumerate(hand):
            color, value = card
            # Any playable card
            if board_state[color] == value - 1:
                # Prefer to play lower cards first
                play_option = (40 + value, i)
                play_choice = min(play_option, play_choice)

                # Check if hand contains follow card
                if (color, value + 1) in hand:
                    play_option = (30 + value, i)
                    play_choice = min(play_option, play_choice)

                # Check if 5 and hints are needed
                if value == 5 and hints <= 2:
                    play_option = (20, i)
                    play_choice = min(play_option, play_choice)                    

                # Prefer that partner can follow
                if (color, value + 1) in partner_hand:
                    play_option = (10 + value, i)
                    play_choice = min(play_option, play_choice)
                    break
    
        play_index = play_choice[1]
        if play_index != None:
#            # Try to avoid forced discard
            color, value = card = hand[play_index]
            assert board_state[color] == value - 1
            board_state[color] += 1
            if value == 5 and hints < 8:
                hints += 1

            hand.pop(play_index)
#            print ("Player {} plays {}".format(player_turn, card))

        elif hints < 8:
            discard_choice = (1000, None)
            for i, card in enumerate(hand):
                color, value = card

                # discard the highest card in hand
                # helps maximise score; doesn't help get 25
                discard_option = (110 - value, i)
                discard_choice = min(discard_option, discard_choice)

                # discard a already played card 
                if board_state[color] >= value:
                    discard_option = (0, i)
                    discard_choice = min(discard_option, discard_choice)
                    break

                # discard a duplicate
                if hand.count(card) > 1:
                    discard_option = (0, i)
                    discard_choice = min(discard_option, discard_choice)
                    break

                # discard a card in partners hand
                if card in partner_hand:
                    discard_option = (20 + value, i)
                    discard_choice = min(discard_option, discard_choice)                    

                # discard a card (prefer higher or soon in the deck) that won't end the line
                elif remaining[color][value] > 1:
                    middle_cards = value - board_state[color]
                    distance_from_end = len(draw) - draw.index(card)

                    priority = 30 + \
                               1 * (4 - middle_cards) + \
                               4 * (5 - value) + \
                               1 * distance_from_end

                    assert priority >= 30
                    discard_option = (priority, i)
                    discard_choice = min(discard_option, discard_choice)                    

            discard_priority = discard_choice[0]
            if discard_priority >= max(30, stall_priority + 1) and hints > 0:
                # Prefer not to do live discards
                # give a hint if possible
                hints -= 1
                stall_priority = discard_priority

            elif stall_priority == 0 and partner_has_playable > 0 and hints > 1:
                # Stall and let partner play again
                hints -= 1
                stall_priority = discard_priority

            else:
                discard_index = discard_choice[1]
                color, value = card = hand.pop(discard_index)
                remaining[color][value] -= 1
                hints += 1

                if discard_priority > 100:
                    forced_discards += 1
                elif discard_priority > 30:
                    live_discards += 1
#                print ("Player {} discards {}".format(player_turn, card))
        else:
            assert hints == 8, hints
            hints -= 1
            stall_priority = 0
            
        stall_priority = 0 if len(hand) < 5 else stall_priority

        if len(draw) > 0:
            if len(hand) < 5:
                hand.append(draw.pop())

        if len(draw) == 0:
            last_turn += 1
            if last_turn == 2:
                break

        player_turn = 1 - player_turn

#        print ("P1: {}  \tP2: {}, rem: {}, lt:{} \nplayed: {}\n".format(
#            hand_string(player_one),
#            hand_string(player_two),
#            len(draw), last_turn,
#            "  ".join([c + str(board_state[c]) for c in COLORS])))

    score = sum(board_state.values())

    if score < MAX_SCORE:
        failure["forced_discards: {}".format(forced_discards)] += 1

        if forced_discards == 0:
            failure["live_dscards: {}".format(live_discards)] += 1

    # TODO count how many are identical:
    #   Any card not played can be swapped with any other not played card?
    #   Colors can be permuted in 5! = 120 ways
    return score


if __name__ == "__main__":

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
        r_decks.append(r_deck)

    T1 = time.time()
    print ("Generated {} random decks ({:.0f} seconds)".format(len(r_decks), T1 - T0))


    LAST_EXAMINE = 5
    last_x = [[defaultdict(int) for x in range(LAST_EXAMINE + 1)] for i in range(MAX_SCORE + 1)]
    dists = defaultdict(list)
    for r_i, r_deck in enumerate(r_decks):
        score = greedy_v4(r_deck)

        dists[score].append(r_i)

        if score < MAX_SCORE:
            for x in range(1, LAST_EXAMINE+1):
                last_x[score][x][reduce_hand(r_deck[-x:])] += 1
                # TODO instead look up position of last X matching cards

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


    total_failures = 0
    print ()
    for score, last_x_failures in enumerate(last_x):
        for x, failures_map in enumerate(last_x_failures):
            if sum(failures_map.values()) < 10:
                continue
            print (score, x, "\t", sum(failures_map.values()))
            for last in sorted(failures_map, key=failures_map.get, reverse=True):
                count = failures_map[last]
                if count < 6:
                    break
                print ("\t", count, last)
