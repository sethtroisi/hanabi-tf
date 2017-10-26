import itertools
import random
import math
import time
from Greedy import greedy_v4, reduce_hand, hand_string

from collections import defaultdict, Counter


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
NUMBER_OF_CARDS = len(COLORS) * len(VALUE_DIST)

T0 = time.time()

def nCr(a, b):
    assert b <= a
    fact = math.factorial
    return fact(a) // fact(b) // fact(a - b)

def CountFractionWithEnding(ending):
    number_of_colors = len(set([c for c, v in ending]))
    color_combinations = nCr(4, number_of_colors)
    card_combinations = 1
    for (c, v), count in Counter(ending).items():
        card_combinations *= nCr(VALUE_COUNT[v], count)

    all_possibilities = math.factorial(NUMBER_OF_CARDS) // math.factorial(NUMBER_OF_CARDS - len(ending))
    return card_combinations * color_combinations / all_possibilities




sorted_deck = []
for color in COLORS:
    for value in VALUE_DIST:
        sorted_deck.append( (color, value) )


random.seed(10)

R_HANDS = 2000

bad_ending_fractions = 0
bad_endings = []
good_endings = [tuple()]
for ending_length in range(1, 6):
    new_good_endings = []
    for ending in good_endings:
        other_cards = sorted_deck[:]
        for card in ending:
            other_cards.remove(card)

        for new_end_card in set(other_cards):
            new_ending = (new_end_card,) + ending

            # Canonical is weird and needs to be done backwards
            # (as that's the direction they are built)

            if new_ending[::-1] != reduce_hand(new_ending[::-1]):
                # Not the canonical version of this hand
                continue

            other_cards_rem = other_cards[:]
            other_cards_rem.remove(new_end_card)
            for r_i in range(R_HANDS):
                if r_i == 0:
                    shuffled = other_cards_rem
                else:
                    shuffled = random.sample(other_cards_rem, len(other_cards_rem))
                r_deck = shuffled + list(new_ending)

                score = greedy_v4(r_deck)
                if score == MAX_SCORE:
                    new_good_endings.append(new_ending)
                    break
            else:
                bad_ending_fraction = CountFractionWithEnding(new_ending)
                bad_ending_fractions += bad_ending_fraction 
                bad_endings.append(new_ending)
                print ("\t{:<25}\t{:.9f}".format(hand_string(new_ending), bad_ending_fraction))


    good_endings = new_good_endings
    print (ending_length, len(good_endings))

T1 = time.time()
print ("Considered some endings ({:.0f} seconds)".format(T1 - T0))
print ("{:.5f}% are bad".format(bad_ending_fractions * 100))

# '''
