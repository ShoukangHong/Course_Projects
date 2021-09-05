# -*- coding: utf-8 -*-
import graph_resilience as res
import random
import time
import math
import urllib3
import requests
import matplotlib.pyplot as plt

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)
    
def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)
    order = []    
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            if max_degree_node in new_graph[neighbor]:
                new_graph[neighbor].remove(max_degree_node)
        order.append(max_degree_node)
    return order

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"

def graph_edges(graph):
    return sum([len(graph[node]) for node in graph])
        
def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    http = urllib3.PoolManager()
    graph_file = http.request('GET', graph_url)
    graph_text = graph_file.data.decode('utf-8')
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print("Loaded graph with", len(graph_lines), "nodes")
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))
    return answer_graph

def update_degree_set(degree_set, nodes, new_graph):
    #print(degree_set)
    for no in nodes:
        length = len(new_graph[no])
        #print(length)
        degree_set[length].remove(no)
        degree_set[length - 1].add(no)
            
EX_GRAPH1 = {0:set([1,2,3]), 1:set([0, 2]), 2:set([0, 1]), 3: set([0])}
def targeted_attack(graph):
    result = []
    new_graph = dict(graph)
    degree_set = {x:set([]) for x in range(len(new_graph))}
    for node in new_graph:
        length = len(new_graph[node])
        degree_set[length].add(node)
    for degree in range(len(new_graph) - 1, -1, -1):
        #print(degree, degree_set)
        while degree_set[degree]:
            node = list(degree_set[degree])[0]
            nodes = new_graph[node]
            result.append(node)
            update_degree_set(degree_set, nodes, new_graph)
            delete_node(new_graph, node)
            degree_set[degree].remove(node)
    return result

def plot_format():
    plt.xlabel("attack number", fontsize='large')
    plt.ylabel('largest connect component', fontsize='large')
    plt.title('target attack')
    savepath = 'C:/Users/shouk/py/projects/'
    savename = 'graph_target'
    saveformat = '.png'
    resolution = 300
    plt.axis([0, None, 0, None])
    plt.legend(loc = "upper right")
    plt.savefig(savepath + savename + saveformat, dpi=resolution, bbox_inches="tight")
    
def plot_attack(nums, name):
    plt.plot(range(len(nums)), nums,'-', label = name)

def do_attack(graph, name):
    attacks = [node for node in graph]
    random.shuffle(attacks)
    nums = res.compute_resilience(graph, attacks)
    plot_attack(nums, name)
    
def do_fast_attack(graph, name):
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    attacks = targeted_attack(new_graph)
    nums = res.compute_resilience(graph, attacks)
    plot_attack(nums, name)

# =============================================================================
# time_list = []
# time_list2 = []
# for x in range(10, 1000, 10): 
#     UPA_graph = res.make_UPA_graph(x, 5)
#     start = time.time()
#     attacks = targeted_attack(UPA_graph)
#     end = time.time()
#     time_list.append(end - start)
#     start = time.time()
#     attacks = targeted_order(UPA_graph)
#     end = time.time()
#     time_list2.append(end - start)
# plt.plot(range(10, 1000, 10), time_list,'-', label = 'fast_targeted_time')
# plt.plot(range(10, 1000, 10), time_list,'-', label = 'fast_targeted_time')
# plot_format()  
# =============================================================================
rand_graph = res.make_ER_graph(1239, 0.002)
web_graph = load_graph(NETWORK_URL)
UPA_graph = res.make_UPA_graph(1239, 2)

do_fast_attack(UPA_graph, 'UPA, m = 2')
do_fast_attack(rand_graph, 'ER, p = 0.002')
do_fast_attack(web_graph, 'Network')
plot_format()
print(graph_edges(web_graph), graph_edges(rand_graph), graph_edges(UPA_graph))
