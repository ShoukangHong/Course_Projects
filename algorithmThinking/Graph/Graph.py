# -*- coding: utf-8 -*-
"""
Created on Thu May 27 09:44:20 2021
@author: shouk
"""

EX_GRAPH0 = {0:set([(0,1), (0, 2)]), 1:set([(0, 1)]), 2:set([(0, 2)])}
EX_GRAPH1 = {0:set([(0, 4), (0, 1), (0, 5), (3, 0)]), 
             1:set([(1, 2), (1, 6), (0, 1), (4, 1)]),
             2:set([(2, 3), (1, 2), (5, 2)]),
             3:set([(3, 0), (2, 3)]),
             4:set([(4, 1), (0, 4)]),
             5:set([(5, 2), (0, 5)]),
             6:set([(1, 6)])}
EX_GRAPH2 = {0:set([(9, 0), (0, 4), (0, 1), (0, 5)]),
             1:set([(0, 1), (4, 1), (1, 2), (1, 6), (8, 1)]),
             2:set([(1, 2), (5, 2), (8, 2), (2, 7), (2, 3)]),
             3:set([(2, 3), (3, 7), (7, 3), (8, 3)]),
             4:set([(0, 4), (9, 4), (4, 1)]),
             5:set([(0, 5), (5, 2), (9, 5)]),
             6:set([(1, 6), (9, 6)]),
             7:set([(2, 7), (3, 7), (7, 3)]),
             8:set([(8, 1), (8, 2)]),
             9:set([(9, 0), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7)])
    }
def make_complete_graph(num):
    '''make graph with all possible edges'''
    result = {}
    if num <= 0:
        return result
    for idx in range(num):
        result[idx] = set()
        for idy in range(num):
            if idy != idx:
                result[idx].add((idy, idx))
                result[idx].add((idx, idy))
    return result

def compute_in_degrees(digraph):
    '''aaa'''
    result = {}
    for node, degrees in digraph.items():
        result[node] = 0
        for degree in degrees:
            if degree[0] != node:
                result[node] += 1
    return result
def in_degree_distribution(digraph):
    '''dist'''
    counts = compute_in_degrees(digraph)
    sum = 0
    result = {}
    for node, count in counts.items():
        sum += count
    for node, count in counts.items():
        result[node] = count / sum
    return result

# =============================================================================
# print(compute_in_degrees(EX_GRAPH2))
# print(in_degree_distribution(make_complete_graph(10)))
# =============================================================================
                