# -*- coding: utf-8 -*-
"""
Given several dices, if there exists a dice that win more often against all the other dices, pick the dice
if such dice doesn't exist, let opponent pick dice first, then pick the best dice against the opponent's dice.
@author: shouk
"""
def count_wins(dice1, dice2):
    assert len(dice1) == 6 and len(dice2) == 6
    dice1_wins, dice2_wins = 0, 0
    
    # write your code here
    for n1 in dice1:
        for n2 in dice2:
            if n1 > n2:
                dice1_wins += 1
            elif n2 > n1:
                dice2_wins += 1
    return (dice1_wins, dice2_wins)

def find_the_best_dice(dices):
    assert all(len(dice) == 6 for dice in dices)

    # write your code here
    # use your implementation of count_wins method if necessary
    idx = 0
    for dice1 in dices:
        count = 0
        for dice2 in dices:
            if dice1 == dice2:
                continue
            win1, win2 = count_wins(dice1, dice2)
            if win1 > win2:
                count += 1
        if count == len(dices) - 1:
            return idx
        idx += 1
    return -1

def compute_strategy(dices):
    assert all(len(dice) == 6 for dice in dices)

    strategy = dict()
    strategy["choose_first"] = True
    strategy["first_dice"] = 0
    if find_the_best_dice(dices) >=0:
        strategy["first_dice"] = find_the_best_dice(dices)
        return strategy
    strategy["choose_first"] = False
    for i in range(len(dices)):
        best = i
        mcount = 0
        for j in range(len(dices)):
            win1, win2 = count_wins(dices[i], dices[j])
            if win2 - win1 > mcount:
                best = j
                mcount = win2 - win1
        strategy[i] = best
    return strategy

compute_strategy([[1, 1, 4, 6, 7, 8], [2, 2, 2, 6, 7, 7], [3, 3, 3, 5, 5, 8]])
find_the_best_dice([[3, 3, 3, 3, 3, 3], [6, 6, 2, 2, 2,2], [4, 4, 4, 4, 0, 0], [5, 5, 5, 1, 1, 1]])
