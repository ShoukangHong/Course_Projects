# -*- coding: utf-8 -*-
"""
Created on Thu May 27 09:44:20 2021
@author: shouk
"""
import random

EX_GRAPH0 = {0:set([1, 2]), 1:set(), 2:set()}
EX_GRAPH1 = {0:set([4, 1, 5]), 
             1:set([2, 6]),
             2:set([3]),
             3:set([0]),
             4:set([1]),
             5:set([2]),
             6:set([])}
EX_GRAPH2 = {0:set([4, 1, 5]),
             1:set([2, 6]),
             2:set([7, 3]),
             3:set([7]),
             4:set([1]),
             5:set([2]),
             6:set([]),
             7:set([3]),
             8:set([1, 2]),
             9:set([0, 3, 4, 5, 6, 7])
    }

def make_complete_graph(num):
    '''make graph with all possible edges'''
    result = {}
    if num <= 0:
        return result
    for idx in range(num):
        result[idx] = set(range(num))
        result[idx].remove(idx)
    return result

def make_rand_graph(num, prob):
    '''make graph with all possible edges'''
    result = {}
    if num <= 0:
        return result
    for idx in range(num):
        result[idx] = set([x for x in range(num) if prob > random.random()])
        if idx in result[idx]:
            result[idx].remove(idx)
    return result

def compute_in_degrees(digraph):
    '''compute in degrees of each node'''
    result = {}
    for node, degrees in digraph.items():
        result[node] = 0
    for node, degrees in digraph.items():
        for degree in degrees:
            result[degree] += 1
    return result

def in_degree_distribution(digraph):
    '''compute in degree distribution of a graph'''
    counts = compute_in_degrees(digraph)
    result = {}
    for node in counts:
        if counts[node] in result:
            result[counts[node]] += 1
        else:
            result[counts[node]] = 1
    return result