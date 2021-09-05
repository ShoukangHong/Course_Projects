# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 22:59:04 2021
@author: shouk
"""
import project_4_data as data
import alignment_method as mtd
from matplotlib import pyplot as plt
import math
import os
from timeit import default_timer as timer

FLY_SEQ = data.load_seq('alg_FruitflyEyelessProtein.txt')
HUMAN_SEQ = data.load_seq('alg_HumanEyelessProtein.txt')
CONSENSUS_SEQ = data.load_seq('alg_ConsensusPAXDomain.txt')
WORD_LIST = data.load_words()

SCORE_TABLE = data.load_scoring_file()

def distribution_format(savename):
    plt.xlabel("score", fontsize='large')
    plt.ylabel('frequency', fontsize='large')
    plt.title('random-human score distribution')
    savepath = 'C:/Users/shouk/py/projects/RNA-dynamic-programming/'
    saveformat = '.png'
    resolution = 300
    plt.axis([None, None, 0, None])
    plt.legend(loc = "upper left")
    if os.path.isfile(savepath + savename + saveformat):
        print('file exist!')
        return
    plt.savefig(savepath + savename + saveformat, dpi=resolution, bbox_inches="tight")

# question 8
slow_begin = timer()
print(mtd.check_spelling('humble', 1, WORD_LIST))
print(mtd.check_spelling('firefly', 2, WORD_LIST))
print(timer() - slow_begin)

# =============================================================================
# local_score, fly_local, human_local = mtd.compute_alignment(FLY_SEQ, HUMAN_SEQ, SCORE_TABLE, False)
# # score = 875
# fly_local = mtd.remove_dash(fly_local)
# human_local = mtd.remove_dash(human_local)
# 
# fly_ans_result = mtd.compute_alignment(fly_local, CONSENSUS_SEQ, SCORE_TABLE, True)
# human_ans_result = mtd.compute_alignment(human_local, CONSENSUS_SEQ, SCORE_TABLE, True)
# =============================================================================

# =============================================================================
# #answer for question 1, 2 and 3
# print(fly_ans_result)
# print(human_ans_result)
# print(mtd.overlap_percent(fly_ans_result[1], fly_ans_result[2]))
# print(mtd.overlap_percent(human_ans_result[1], human_ans_result[2]))
# =============================================================================

# =============================================================================
# #distribution figure  
# distribution = mtd.generate_null_distribution(FLY_SEQ, HUMAN_SEQ, SCORE_TABLE, 1000)
# score_list = []
# freq_list = []
# for score, freq in distribution.items():
#     score_list.append(score)
#     freq_list.append(freq)
# plt.bar(score_list, freq_list)
# distribution_format('human-random distribution')
# print(score_list, freq_list)
# =============================================================================
