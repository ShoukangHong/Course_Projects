"""
A dynamic programming method to get the maximum diagonals that can be placed in the n*n table and print one example
This is just for curious, and I didn't spend time to make it readable...
"""
import networkx as nx
from itertools import chain, combinations

def cycle_length(g, cycle):
    '''given a cycle and graph, retern cycle length'''
    assert len(cycle) == g.number_of_nodes()
    return sum([g[cycle[i]][cycle[i + 1]]['weight'] for i in range(-1, len(cycle) - 1)])

def all_permutations(g):
    '''brute-force approach'''
    n = g.number_of_nodes()

    # Iterate through all permutations of n vertices
    return min([sum([g[p[i]][p[i + 1]]['weight'] for i in range(-1, len(p) - 1)]) for p in permutations(range(n))])

def nearest_neighbors(g):
    '''greedy approach'''
    current_node = 0
    path = [current_node]
    n = g.number_of_nodes()

    # We'll repeat the same routine (n-1) times
    for _ in range(n - 1):
        next_node = None
        # The distance to the closest vertex. Initialized with infinity.
        min_edge = float("inf")
        for v in g.nodes():
          if not v == current_node and min_edge > g[current_node][v]['weight'] and not v in path:
            min_edge = g[current_node][v]['weight']
            next_node = v
            # Write your code here: decide if v is a better candidate than next_node.
            # If it is, then update the values of next_node and min_edge

        assert next_node is not None
        path.append(next_node)
        current_node = next_node

    weight = sum(g[path[i]][path[i + 1]]['weight'] for i in range(g.number_of_nodes() - 1))
    weight += g[path[-1]][path[0]]['weight']
    return weight

def powerset(s):
    '''This function returns all the subsets of the given set s in the increasing order of their sizes'''
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def dynamic_programming(g):
    '''This function finds an optimal Hamiltonian cycle using the dynamic programming approach.'''
    n = g.number_of_nodes()

    # The variable power now contains a tuple for each subset of the set {1, ..., n-1}.
    power = powerset(range(1, n))
    for i in range(1, n):
        # Syntactic note: In Python, we define a tuple of length 1 that contains the element i as (i,) *with comma*.
        T[(i,), i] = g[0][i]['weight']

    # For every subset s of [1,...,n-1]
    for s in power:
        # We have already initialized the elements of T indexed by sets of size 1, so we skip them.
        if len(s) > 1:
            # For every vertex i from s which we consider as the ending vertex of a path going through vertices from s.
            for i in s:
                # Define the tuple which contains all elements from s without *the last vertex* i.
                t = tuple([x for x in s if x != i])
                # Now we compute the optimal value of a cycle which visits all vertices from s and ends at the vertex i.
                T[s, i] = min([T[t, j] + g[j][i]['weight'] for j in t])
                # WRITE YOUR CODE HERE
    return min(T[tuple(range(1, n)), i] + g[i][0]['weight'] for i in range(1, n))

import networkx as nx

def approximation(g):
    ''' minimum spanning tree + DFS, which outputs a solution which is a 2-approximation of the optimal weight.'''
    n = g.number_of_nodes()
    mst = nx.minimum_spanning_tree(g)
    path = list(nx.dfs_preorder_nodes(mst, 0))
    # You might want to use the function "nx.minimum_spanning_tree(g)"
    # which returns a Minimum Spanning Tree of the graph g

    # You also might want to use the command "list(nx.dfs_preorder_nodes(graph, 0))"
    # which gives a list of vertices of the given graph in depth-first preorder.

    return sum([g[path[i - 1]][path[i]]['weight'] for i in range(n)])

