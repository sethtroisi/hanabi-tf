import random
import math

from collections import defaultdict


ROUNDS = 50000


# Total number of hands
#fact = math.factorial
#color_perms = (fact(3) * fact(2) ** 3) ** 5
#start_perm = fact(5) ** 2
#color_reassign = fact(5)
#print (fact(50) / color_perms / color_reassign / start_perm)


COLORS = ["B", "G", "R", "W", "Y"]

def handString(hand):
    return ", ".join(c + str(n) for c,n in hand)


def greedy_brute(deck):
    player_one = deck[:5]
    player_two = deck[5:10]

    draw = deck[10:]

    board_state = {color : 0 for color in COLORS}
    hints = 8
    fuses = 2 # the number you can use without ending the game

    player_turn = 0
    last_turn = -1

#    print ("P1: {}".format(player_one))
#    print ("P2: {}".format(player_two))
#    print ("deck: {}".format(deck))

    while True:
        hand = player_one if player_turn == 0 else player_two

        # plays a card if possible
        play_index = None
        for i, card in enumerate(hand):
            color, value = card
            if board_state[color] == value - 1:
                # play
                play_index = i
                break

        if play_index != None:
            color, value = card = hand[play_index]
            assert board_state[color] == value - 1
            board_state[color] += 1

#            print ("Player {} plays {}".format(player_turn, card))

            hand.pop(play_index)
        else:
            # discard first card
            discard_index = 0
            card = hand.pop(discard_index)
#            print ("Player {} discards {}".format(player_turn, card))


        if len(draw) > 0:
            if len(hand) < 5:
                hand.append(draw.pop())
        else:
            last_turn += 1
            if last_turn == 2:
                break

        player_turn = 1 - player_turn


#        print ("P1: {}  \tP2: {}, rem: {}\nplayed: {}\n".format(
#            handString(player_one),
#            handString(player_two),
#            len(deck),
#            "  ".join([c + str(board_state[c]) for c in COLORS])))

    return sum(board_state.values())



def greedy_v2(deck):
    player_one = deck[:5]
    player_two = deck[5:10]

    draw = deck[10:]

    board_state = {color : 0 for color in COLORS}
    remaining = {color : [0,3,2,2,2,1] for color in COLORS}
    hints = 8
    fuses = 2 # the number you can use without ending the game

    player_turn = 0
    last_turn = -1

#    print ("P1: {}".format(player_one))
#    print ("P2: {}".format(player_two))
#    print ("deck: {}".format(deck))

    while True:
        hand = player_one if player_turn == 0 else player_two
        partner_hand = player_two if player_turn == 0 else player_one

        # plays newest card that can be played
        play_choice = (100, None)
        for i, card in enumerate(hand):
            color, value = card
            # Any playable card
            if board_state[color] == value - 1:
                # Prefer to play lower cards first
                play_option = (2 + value, i)
                play_choice = min(play_option, play_choice)

                # Can be followed by play by partner
                if (color, value + 1) in partner_hand:
                    play_option = (1, i)
                    play_choice = min(play_option, play_choice)
    
        play_index = play_choice[1]
        if play_index != None:
            color, value = card = hand[play_index]
            assert board_state[color] == value - 1
            board_state[color] += 1

#            print ("Player {} plays {}".format(player_turn, card))

            hand.pop(play_index)
        else:
            discard_choice = (100, None)
            for i, card in enumerate(hand):
                color, value = card

                # discard a already played card 
                if board_state[color] >= value:
                    discard_option = (0, i)
                    discard_choice = min(discard_option, discard_choice)

                # discard a card in partners hand
                if card in partner_hand:
                    discard_option = (1, i)
                    discard_choice = min(discard_option, discard_choice)                    

                # discard a card that won't end the line
                if remaining[color][value] > 1:
                    discard_option = (2, i)
                    discard_choice = min(discard_option, discard_choice)                    

            discard_priority = discard_choice[0]
            if discard_priority > 2 and hints > 0:
                # Not an already played or available card
                # give a hint if possible
                hints -= 1
#                print ("Player {} hints".format(player_turn))

            else:
                # discard oldest card in hand
                discard_index = discard_choice[1]
                if discard_index == None:
                    discard_index = len(hand) - 1

                color, value = card = hand.pop(discard_index)
                remaining[color][value] -= 1
#                print ("Player {} discards {}".format(player_turn, card))

        if len(draw) > 0:
            if len(hand) < 5:
                hand.append(draw.pop())
        else:
            last_turn += 1
            if last_turn == 2:
                break

        player_turn = 1 - player_turn

#        print ("P1: {}  \tP2: {}, rem: {}, lt:{} \nplayed: {}\n".format(
#            handString(player_one),
#            handString(player_two),
#            len(draw), last_turn,
#            "  ".join([c + str(board_state[c]) for c in COLORS])))

    return sum(board_state.values())



def greedy_v3(deck):
    player_one = deck[:5]
    player_two = deck[5:10]

    draw = deck[10:]

    board_state = {color : 0 for color in COLORS}
    remaining = {color : [0,3,2,2,2,1] for color in COLORS}

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
    simple_suits = set()
    for color in COLORS:
        played = 0
        for value in color_order[color]:
            if value == played + 1:
                played += 1
        if played >= 4:
            simple_suits.add(color)

    hints = 8
    fuses = 2 # the number you can use without ending the game

    player_turn = 0
    last_turn = -1

#    print ("P1: {}".format(player_one))
#    print ("P2: {}".format(player_two))
#    print ("deck: {}".format(deck))

    while True:
        hand = player_one if player_turn == 0 else player_two
        partner_hand = player_two if player_turn == 0 else player_one

        # plays newest card that can be played
        play_choice = (100, None)
        for i, card in enumerate(hand):
            color, value = card
            # Any playable card
            if board_state[color] == value - 1:
                # Prefer to play lower cards first
                play_option = (2 + value, i)
                play_choice = min(play_option, play_choice)

                # Check if hand contains follow card
                if (color, value + 1) in hand:
                    play_option = (2, i)
                    play_choice = min(play_option, play_choice)

                # Prefer that partner can follow
                if (color, value + 1) in partner_hand:
                    play_option = (1, i)
                    play_choice = min(play_option, play_choice)
    
        play_index = play_choice[1]
        if play_index != None:
            color, value = card = hand[play_index]
            assert board_state[color] == value - 1
            board_state[color] += 1
            if value == 5:
                hints += 1

            hand.pop(play_index)
#            print ("Player {} plays {}".format(player_turn, card))

        else:
            discard_choice = (100, None)
            for i, card in enumerate(hand):
                color, value = card

                # discard the highest card in hand
                # helps maximise score; doesn't help get 25
                discard_option = (100 - value, i)
                discard_choice = min(discard_option, discard_choice)

                # discard a already played card 
                if board_state[color] >= value:
                    discard_option = (0, i)
                    discard_choice = min(discard_option, discard_choice)

                # discard a duplicate
                if hand.count(card) > 1:
                    discard_option = (2, i)
                    discard_choice = min(discard_option, discard_choice)

                # discard a card in partners hand
                if card in partner_hand:
                    discard_option = (2, i)
                    discard_choice = min(discard_option, discard_choice)                    

                # discard a card that won't end the line
                if remaining[color][value] > 1:
                    discard_option = (3, i)
                    discard_choice = min(discard_option, discard_choice)                    

            discard_priority = discard_choice[0]
            if discard_priority > 20 and hints > 0:
                # Not an already played or available card
                # give a hint if possible
                hints -= 1
#                print ("Player {} hints".format(player_turn))

            else:
                discard_index = discard_choice[1]
                color, value = card = hand.pop(discard_index)
                remaining[color][value] -= 1
                hints += 1
#                print ("Player {} discards {}".format(player_turn, card))

        if len(draw) > 0:
            if len(hand) < 5:
                hand.append(draw.pop())
        else:
            last_turn += 1
            if last_turn == 2:
                break

        player_turn = 1 - player_turn

#        print ("P1: {}  \tP2: {}, rem: {}, lt:{} \nplayed: {}\n".format(
#            handString(player_one),
#            handString(player_two),
#            len(draw), last_turn,
#            "  ".join([c + str(board_state[c]) for c in COLORS])))

    return sum(board_state.values())


sorted_deck = []
for color in COLORS:
    for value in [1, 1, 1, 2, 2, 3, 3, 4, 4, 5]:
        sorted_deck.append( (color, value) )


random.seed(10)

r_decks = []
for i in  range(ROUNDS):
    r_deck = sorted_deck[:]
    random.shuffle(r_deck)
    r_decks.append(r_deck)

print ("Generated {} random decks".format(len(r_decks)))


#'''
dists = defaultdict(lambda : defaultdict(int))
for r_i, r_deck in enumerate(r_decks):
    score_brute = greedy_brute(r_deck)
    score_brute_v2 = greedy_v2(r_deck)
    score_brute_v3 = greedy_v3(r_deck)

    dists["brute"][score_brute] += 1
    dists["brute_v2"][score_brute_v2] += 1
    dists["brute_v3"][score_brute_v3] += 1


avg = defaultdict(float)
for score in range(0, 30+1):
    total_count = 0
    for key in sorted(dists.keys()):
        count = dists[key][score]
        avg[key] += score * count

        if count > 0:
            print (score, "\t", key, " ", count)


for k in avg.keys():
    avg[k] /= len(r_decks)

print ("avg score:",
       ", ".join(map(lambda e: "{}: {}".format(e[0], e[1]), sorted(avg.items()))))
#'''
