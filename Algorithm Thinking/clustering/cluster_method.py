# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 17:58:32 2021

@author: shouk
"""
import math
import random
from cluster_class import Cluster
def slow_closest_pair(clusters):
    '''sb'''
    length = len(clusters)
    min_dist = float('inf')
    result = None
    for idx in range(length):
        for idy in range(idx + 1, length):
            dist = clusters[idx].distance(clusters[idy])
            if dist <= min_dist:
                min_dist = dist
                result = (min_dist, idx, idy)
    return result

def closest_pair_strip(clusters, mid, wid):#: y, wid: half width
    '''sb'''
    new_clusters = list(filter(lambda cluster: abs(cluster.horiz_center() - mid) < wid , clusters))
    new_clusters.sort(key = lambda cluster: cluster.vert_center())
    #print(new_clusters)
    length = len(new_clusters)
    result = (float('inf'), -1, -1)
    for idx in range(length - 1):
        for idy in range(idx + 1, min(idx + 4, length)):
            dist = new_clusters[idx].distance(new_clusters[idy])
            #print(dist, idx, idy)
            if dist <= result[0]:
                result = (dist, clusters.index(new_clusters[idx]), clusters.index(new_clusters[idy]))
    if result[1] < result[2]:
        return result
    else:
        return (result[0], result[2], result[1])

def fast_closest_pair(clusters):
    '''sb'''
    length = len(clusters)
    if length <= 3:
        return slow_closest_pair(clusters)
    else:
        half = length // 2
        l_clusters, r_clusters = clusters[:half], clusters[half:]
        l_pair = fast_closest_pair(l_clusters)
        r_pair = fast_closest_pair(r_clusters)
        if l_pair[0] < r_pair[0]:
            result = l_pair
        else:
            result = (r_pair[0], r_pair[1] + half, r_pair[2] + half)
        mid = 0.5 * (clusters[half - 1].horiz_center() + clusters[half].horiz_center())
        new_result = closest_pair_strip(clusters, mid, result[0])
        if new_result[0] < result[0]:
            result = new_result
        return result
        
def hierarchical_clustering(o_cluster, num):
    '''sb'''
    clusters = [cluster.copy() for cluster in o_cluster]
    clusters.sort(key = lambda cluster: cluster.horiz_center())
    #print(clusters)
    while len(clusters) > num:
        merges = fast_closest_pair(clusters)
        c_2 = clusters.pop(merges[2])
        clusters[merges[1]].merge_clusters(c_2)
    return clusters

def kmeans_clustering(o_cluster, num, loop_time):
    '''sb'''
    count = 0
    clusters = [cluster.copy() for cluster in o_cluster]
    clusters.sort(key = lambda cluster: -cluster.total_population())
    centers = [(clusters[idx].horiz_center(), clusters[idx].vert_center()) for idx in range(num)]
    #print(centers)
    while count < loop_time:
        count += 1
        new_clusters = [None] * num
        for cluster in clusters:
            min_dist = float('inf')
            for idx in range(num):
                vert_dist = cluster.vert_center() - centers[idx][1]
                horiz_dist = cluster.horiz_center() - centers[idx][0]
                dist = math.sqrt(vert_dist ** 2 + horiz_dist ** 2)
                if dist < min_dist:
                    min_id = idx
                    min_dist = dist
                    #print(min_id)
            if new_clusters[min_id]:
                new_clusters[min_id] = new_clusters[min_id].merge_clusters(cluster)
            else:
                new_clusters[min_id] = cluster.copy()
            #print(clusters)
        #clusters.sort(key = lambda cluster: -len(cluster.fips_codes()))
        for idx in range(num):
            centers[idx] = (new_clusters[idx].horiz_center(), new_clusters[idx].vert_center())
    return new_clusters
        
def gen_random_clusters(num):
    clusters = []
    for idx in range(num):
        clusters.append(Cluster(set([idx]), 2 * random.random() - 1, 2 * random.random() - 1, 1, 1))
    return clusters
        
        