"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

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
    hand: full yahtzee hand
    Returns an integer score 
    """
    new_map = {}
    for num in hand:
        if num in new_map:
            new_map[num] += num
        else:
            new_map[num] = num
    return max([new_map[num] for num in new_map])

def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.
    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled
    Returns a floating point expected value
    """
    sum_score = 0
    count = 0
    # print held_dice, num_die_sides, num_free_dice
    dice_set = gen_all_sequences(range(1, num_die_sides + 1), num_free_dice)
    for perm in dice_set:
        tmp = list(held_dice) + list(perm)
        count += 1
        sum_score += score(tmp)
    # print sum_score * 1.0 / count
    return sum_score * 1.0 / count
    
def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    result = set([])
    sorted_hand = list(hand)
    sorted_hand.sort()
    for dice_num in range(len(hand) + 1):
        tmp_list = gen_all_sequences(range(len(hand)), dice_num)
        for perm in tmp_list:
            tmp_perm = list(perm)
            tmp_perm.sort()
            converted = [sorted_hand[idx] for idx in tmp_perm]
            #print converted
            if len(set(tmp_perm)) == len(tmp_perm):
                result.add(tuple(converted))
    # print result, len(result)
    return result



def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    all_holds = gen_all_holds(hand)
    best_score = 0
    for hold in all_holds:
        exp_value = expected_value(hold, num_die_sides, len(hand) - len(hold))
        if exp_value > best_score:
            best_hold = hold
            best_score = exp_value
    return (best_score, best_hold)


#def run_example():
#    """
#    Compute the dice to hold and expected score for an example hand
#    """
#    num_die_sides = 3
#    hand = (1,3)
#    hand_score, hold = strategy(hand, num_die_sides)
#    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
#    
#    
#run_example()
#gen_all_holds((1,2,2))
# expected_value((6,), 6, 2)
#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                       
    
    
    



