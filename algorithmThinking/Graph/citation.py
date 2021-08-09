# -*- coding: utf-8 -*-
"""
Created on Thu May 27 11:24:42 2021

@author: shouk
"""

import Graph2 as graph
import urllib3
import requests
import matplotlib.pyplot as plt
import json

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"
http = urllib3.PoolManager()

def plot_dist(dist):
    
    lists = sorted(dist.items())
    key, val = zip(*lists)
    total = sum(val)
    print(total)
    plt.plot(key, [v/total for v in val],'o')
    plt.yscale("log")
    plt.xscale("log")
    plt.xlabel("cited number", fontsize='large')
    plt.ylabel('distribution', fontsize='large')
    plt.title('DPA graph')
    savepath = 'C:/Users/shouk/py/projects/'
    savename = 'graph_test'
    saveformat = '.png'
    resolution = 300
    plt.axis([1, None, None, None])
    plt.savefig(savepath + savename + saveformat, dpi=resolution, bbox_inches="tight")   

def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    http = urllib3.PoolManager()
    graph_file = http.request('GET', CITATION_URL)
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

citation_graph = load_graph(CITATION_URL)
graph_rand = graph.make_rand_graph(1000, 0.1)
dist = graph.in_degree_distribution(citation_graph)    
plot_dist(dist)