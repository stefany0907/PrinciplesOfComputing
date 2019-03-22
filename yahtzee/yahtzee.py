"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
#import codeskulptor
#codeskulptor.set_timeout(20)


def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: sorted tuple representing a full Yahtzee hand

    Returns an integer score
    """
    dice_val, score_lst = [], []
    for dice in hand:
        dice_val.append(dice)
        dice_max = max(dice_val)
    for item in range(1, (dice_max + 1)):
        score_num = 0
        for dice in hand:
            if item == dice:
                score_num += item
        score_lst.append(score_num)
    return max(score_lst)


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: a sorted tuple representing dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    score_val = 0
    outcomes = set([])
    for dummy in range(num_die_sides):
        outcomes.add(dummy + 1)
    out_hand = gen_all_sequences(outcomes, num_free_dice)
    # print "next out_hand=", out_hand
    for element in out_hand:
        hand = tuple(list(held_dice) + list(element))
        # print "hand=", hand, "score=", score(hand)
        score_val += score(hand)
        # print "expected value=", float(score_val) / len(out_hand)
    # print
    return float(score_val) / len(out_hand)


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: sorted tuple representing a full Yahtzee hand

    Returns a set of sorted tuples, where each tuple is dice to hold
    """
    hold_lst = [[]]
    hold_set = set([()])
    for item in list(hand):
        hold_lst += [x + [item] for x in hold_lst]
    # print sorted(hold_lst)
    for idx in hold_lst:
        hold_set.add(tuple(idx))
        # print hold_set
    # print set(sorted(hold_set))

    return set(sorted(hold_set))


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: sorted tuple representing a full Yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    held_dice = gen_all_holds(hand)
    exp_value = 0
    exp_value_lst = []
    exp_dict = {}
    for item in held_dice:
        num_free_dice = len(hand) - len(item)
        # print "held_item=", item, "num_free_dice=", num_free_dice
        exp_value = expected_value(item, num_die_sides, num_free_dice)
        exp_value_lst.append(exp_value)
        exp_dict[(item)] = (exp_value)

    for key in exp_dict.keys():
        if exp_dict[key] == max(exp_value_lst):
            return (max(exp_value_lst), key)
    # return (0.0, ())


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 2
    hand = (1, 1)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score


run_example()

# import poc_holds_testsuite
# poc_holds_testsuite.run_suite(gen_all_holds)
#
# score = 0
# for i in range(1,7):
#    for j in range(1,7):
#        if  i == j:
#            score += 2 * i
#        else:
#            score += max(i,j)
# print float(score) / 36
#




