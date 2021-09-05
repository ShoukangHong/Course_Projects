# -*- coding: utf-8 -*-
'''compute the graph resilence of undirected graph'''
from collections import deque
import random
#import matplotlib.pyplot as plt
# =============================================================================
# EX_GRAPH0 = {0:set([1]), 1:set([0]), 2:set()}
# EX_GRAPH1 = {0:set([1,2,3]), 1:set([2, 3]), 2:set([0, 1]),
#              3:set([0, 1]), 4:set([5, 7]), 5:set([4, 6]),
#              6:set([5, 7]), 7: set([6, 8]), 8:set([7])}
# =============================================================================
def make_ER_graph(num, prob):
    graph = {x:set() for x in range(num)}
    for node in graph:
        for idx in range(num):
            if random.random() <= prob and idx != node:
                graph[node].add(idx)
                graph[idx].add(node)
    return graph
#print(make_ER_graph(10, 0.2))

def make_UPA_graph(node_num, edge_num):
    graph = {x:set() for x in range(node_num)}
    total_deg = [x for x in range(node_num)]
    for node in range(edge_num, node_num):
        edges = set()
        for idx in range(edge_num):
            edges.add(random.choice(total_deg))
        edges = edges.difference(graph[node])
        for edge in edges:
            if edge != node:
                total_deg.append(node)
                total_deg.append(edge)
                graph[node].add(edge)
                graph[edge].add(node)
    return graph

def distribution(graph):
    dist = {}
    for node in graph:
        length = len(graph[node])
        if length in dist:
            dist[length] += 1
        else:
            dist[length] = 1
    return dist

# =============================================================================
# def plot_dist(dist):
#     
#     lists = sorted(dist.items())
#     key, val = zip(*lists)
#     total = sum(val)
#     print(total)
#     plt.plot(key, [v/total for v in val],'o')
#     plt.yscale("log")
#     plt.xscale("log")
#     plt.xlabel("cited number", fontsize='large')
#     plt.ylabel('distribution', fontsize='large')
#     plt.title('DPA graph')
#     savepath = 'C:/Users/shouk/py/projects/'
#     savename = 'graph_test'
#     saveformat = '.png'
#     resolution = 300
#     plt.axis([1, None, None, None])
#     #plt.savefig(savepath + savename + saveformat, dpi=resolution, bbox_inches="tight")   
# =============================================================================
# =============================================================================
# g = make_UPA_graph(27000, 13)  
# print(sorted(distribution(g).items()))
# plot_dist(distribution(g))
# =============================================================================
def bfs_visited(graph, start_node):
    '''sb'''
    que = deque([graph[start_node]])
    visited = set([start_node])
    while que:
        nodes = que.pop()
        for node in nodes:
            if not node in visited:
                que.appendleft(graph[node])
                visited.add(node)
    return visited

def cc_visited(graph):
    '''sb'''
    rgraph =set(graph)
    groups = []
    while rgraph:
        start_node = random.choice(list(rgraph))
        group = bfs_visited(graph, start_node)
        groups.append(group)
        rgraph = rgraph.difference(group)
    return groups

def largest_cc_size(graph):
    '''sb'''
    groups = cc_visited(graph)
    if not graph:
        return 0
    return max([len(group) for group in groups])

def compute_resilience(graph, attack_order):
    '''sb'''
    new_graph = dict(graph)
    ans = [largest_cc_size(new_graph)]
    print(ans)
    for node in attack_order:
        new_graph.pop(node)
        for rnode in new_graph:
            if node in new_graph[rnode]:
                new_graph[rnode].remove(node)
        ans.append(largest_cc_size(new_graph))
    return ans
            
# =============================================================================
# print(bfs_visited(EX_GRAPH1, 8))
# print(cc_visited(EX_GRAPH1))
# print(largest_cc_size(EX_GRAPH0))
# print(compute_resilience(EX_GRAPH1, [1,2,3,4,5,6,7,8,0]))
# =============================================================================
            
            

