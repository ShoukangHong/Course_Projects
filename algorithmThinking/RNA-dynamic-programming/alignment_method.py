# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 23:14:39 2021
@author: shouk
"""
import random
import string

def remove_dash(seq):
    result = ''
    for char in seq:
        if char != '-':
            result += char
    return result

def overlap_percent(seq_y, seq_x):
    length = len(seq_y)
    num = 0
    for idx in range(length):
        if seq_y[idx] == seq_x[idx]:
            num += 1
    return 100 * num / length

def build_scoring_matrix(char_set, diag_score, off_diag_score, dash_score):
    '''build scoring matrix'''    
    matrix = {char:{'-':dash_score} for char in char_set}
    for char in matrix:
        for char_2 in char_set:
            if char == char_2:
                matrix[char][char_2] = diag_score
            else:
                matrix[char][char_2] = off_diag_score
    matrix['-'] = {char:dash_score for char in char_set}
    matrix['-']['-'] = dash_score
    return matrix

def init_matrix(width, height, score_table, flag):
    '''initiate an alignment matrix'''
    matrix = [[0 for num in range(0, width)] for num in range(0, height)]
    dash_score = max([val for dummy_key, val in score_table['-'].items()])
    if not flag:
        return matrix
    for num in range(1, width):
        matrix[0][num] = matrix[0][num - 1] + dash_score
    for num in range(1, height):
        matrix[num][0] = matrix[num - 1][0] + dash_score
    return matrix

def align_max(str_y, str_x, idy, idx, score_table, align_matrix):
    '''calculate the max val for the given grid'''
    if idy == 0:
        val_y_dash = align_matrix[idy][idx - 1] + score_table['-'][str_x[idx - 1]]
        return (float('-inf'), float('-inf'), val_y_dash)
    if idx == 0:
        val_x_dash = align_matrix[idy - 1][idx] + score_table[str_y[idy - 1]]['-']
        return (float('-inf'), val_x_dash, float('-inf'))
    val_match = align_matrix[idy - 1][idx - 1] + score_table[str_x[idx - 1]][str_y[idy - 1]]
    val_x_dash = align_matrix[idy - 1][idx] + score_table[str_y[idy - 1]]['-']
    val_y_dash = align_matrix[idy][idx - 1] + score_table['-'][str_x[idx - 1]]
    return (val_match, val_x_dash, val_y_dash)
    
def compute_alignment_matrix(str_y, str_x, score_table, flag):
    'compute an alignment matrix by dynamic porgramming'
    align_matrix = init_matrix(len(str_x) + 1, len(str_y) + 1, score_table, flag)
    for idy in range(1, len(str_y) + 1):
        for idx in range(1, len(str_x) + 1):
            align_matrix[idy][idx] = max(align_max(str_y, str_x, idy, idx, score_table, align_matrix))
            if not flag:
                align_matrix[idy][idx] = max(align_matrix[idy][idx], 0)
    #print(align_matrix)
    return align_matrix

def compute_global_alignment(seq_y, seq_x, score_table, align_matrix):
    '''compute global alignment'''
    width = len(seq_x)
    height = len(seq_y)
    pos_x, pos_y = width, height
    str_x, str_y = '', ''
    score = align_matrix[height][width]
    while pos_x != 0 or pos_y != 0:
        both, x_dash, y_dash = align_max(seq_y, seq_x, pos_y, pos_x, score_table, align_matrix)
        best = max(both, x_dash, y_dash)
        if best == both:
            str_x = seq_x[pos_x - 1] + str_x
            str_y = seq_y[pos_y - 1] + str_y
            pos_x -= 1
            pos_y -= 1
        elif best == x_dash:
            str_x = '-' + str_x
            str_y = seq_y[pos_y - 1] + str_y
            pos_y -= 1
        else:
            str_x = seq_x[pos_x - 1] + str_x
            str_y = '-' + str_y
            pos_x -= 1
    return (score, str_y, str_x)

def compute_local_alignment(seq_y, seq_x, score_table, align_matrix):
    '''compute local alignment'''
    best_x, best_y, best = 0, 0, 0
    for pos_y in range(len(seq_y) + 1):
        for pos_x in range(len(seq_x) + 1):
            if align_matrix[pos_y][pos_x] > best:
                best = align_matrix[pos_y][pos_x]
                best_x, best_y = pos_x, pos_y
    score = best
    pos_x, pos_y = best_x, best_y
    str_x, str_y = '', ''
    while align_matrix[pos_y][pos_x] > 0:
        both, x_dash, y_dash = align_max(seq_y, seq_x, pos_y, pos_x, score_table, align_matrix)
        score = max(both, x_dash, y_dash)
        if score == both:
            str_x = seq_x[pos_x - 1] + str_x
            str_y = seq_y[pos_y - 1] + str_y
            pos_x -= 1
            pos_y -= 1
        elif score == x_dash:
            str_x = '-' + str_x
            str_y = seq_y[pos_y - 1] + str_y
            pos_y -= 1
        else:
            str_x = seq_x[pos_x - 1] + str_x
            str_y = '-' + str_y
            pos_x -= 1
    return (best, str_y, str_x)
        
def compute_alignment(seq_y, seq_x, score_table, global_align = False):
    align_matrix = compute_alignment_matrix(seq_y, seq_x, score_table, global_align)
    if global_align:
        return compute_global_alignment(seq_y, seq_x, score_table, align_matrix)
    else:
        return compute_local_alignment(seq_y, seq_x, score_table, align_matrix)

def generate_null_distribution(seq_y, seq_x, score_table, num_trials):
    distri= {}
    rand_y = [char for char in seq_y]
    for num in range(num_trials):
        random.shuffle(rand_y)
        rand_seq_y = ''.join(rand_y)
        scores = compute_alignment_matrix(rand_seq_y, seq_x, score_table, False)
        score = max([max(line) for line in scores])
        if score in distri:
            distri[score] += 1
        else:
            distri[score] = 1
        print(num)
    for score in distri:
        distri[score] /= num_trials
    return distri

def check_spelling(check_word, target_dist, word_list):
    len_check_word = len(check_word)
    possible_word = []
    score_table = build_scoring_matrix(set([char for char in string.ascii_lowercase]), 2, 1, 0)
    for word in word_list:
        if abs(len(word) - len_check_word) <= target_dist:
            dist = len(word) + len_check_word - compute_alignment(check_word, word, score_table, True)[0]
            if dist <= target_dist:
                possible_word.append(word)
    return possible_word

#generate_null_distribution('abcdefg', 0, 0, 0)
# =============================================================================
# seq_y = 'aaac'
# seq_x = 'bbbaababbcb'
# score_table = build_scoring_matrix(set(['a', 'b', 'c', 'd']), 10, 4, -2)
# align_matrix = compute_alignment_matrix(seq_y, seq_x, score_table, True)
# align_matrix2 = compute_alignment_matrix(seq_y, seq_x, score_table, False)
# print(align_matrix)
# result = compute_global_alignment(seq_y, seq_x, score_table, align_matrix)
# result2 = compute_local_alignment(seq_y, seq_x, score_table, align_matrix2)
# print(result)
# print(result2)
# =============================================================================
#print(build_scoring_matrix(set(['a', 'b', 'c']), 10, 5, -5))

