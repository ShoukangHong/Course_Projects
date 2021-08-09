# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 10:06:06 2021
@author: shouk
"""
import math
from cluster_class import Cluster
import cluster_method as mtd
import cluster_class as alg_cluster
from timeit import default_timer as timer
import os
from matplotlib import pyplot as plt

DIRECTORY = "C:/Users/shouk/py/projects/clusters/"
MAP_URL = 'C:/Users/shouk/py/projects/clusters/Counties.png'
DATA_111 = 'C:/Users/shouk/py/projects/clusters/unifiedCancerData_111.csv'
DATA_3108 = 'C:/Users/shouk/py/projects/clusters/unifiedCancerData_3108.csv'
DATA_290 = 'C:/Users/shouk/py/projects/clusters/unifiedCancerData_290.csv'
DATA_896 = 'C:/Users/shouk/py/projects/clusters/unifiedCancerData_896.csv'

# Define colors for clusters.  Display a max of 16 clusters.
COLORS = ['Aqua', 'Yellow', 'Blue', 'Fuchsia', 'Black', 'Green', 'Lime', 'Maroon', 'Navy', 'Olive', 'Orange', 'Purple', 'Red', 'Brown', 'Teal']
# Helper functions
def circle_area(pop):
    """
    Compute area of circle proportional to population
    """
    return math.pi * pop / (200.0 ** 2)

def plot_clusters(data_table, cluster_list, draw_centers = False):
    """
    Create a plot of clusters of counties
    """

    fips_to_line = {}
    for line_idx in range(len(data_table)):
        fips_to_line[data_table[line_idx][0]] = line_idx
     
    # Load map image
    map_file = open(MAP_URL)
    map_img = plt.imread(MAP_URL)

    # Scale plot to get size similar to CodeSkulptor version
    ypixels, xpixels, bands = map_img.shape
    DPI = 60.0                  # adjust this constant to resize your plot
    xinch = xpixels / DPI
    yinch = ypixels / DPI
    plt.figure(figsize=(xinch,yinch))
    implot = plt.imshow(map_img)
   
    # draw the counties colored by cluster on the map
    if not draw_centers:
        for cluster_idx in range(len(cluster_list)):
            cluster = cluster_list[cluster_idx]
            cluster_color = COLORS[cluster_idx % len(COLORS)]
            for fips_code in cluster.fips_codes():
                line = data_table[fips_to_line[fips_code]]
                plt.scatter(x = [line[1]], y = [line[2]], s =  circle_area(line[3]), lw = 1,
                            facecolors = cluster_color, edgecolors = cluster_color)

    # add cluster centers and lines from center to counties            
    else:
        for cluster_idx in range(len(cluster_list)):
            cluster = cluster_list[cluster_idx]
            cluster_color = COLORS[cluster_idx % len(COLORS)]
            for fips_code in cluster.fips_codes():
                line = data_table[fips_to_line[fips_code]]
                plt.scatter(x = [line[1]], y = [line[2]], s =  circle_area(line[3]), lw = 1,
                            facecolors = cluster_color, edgecolors = cluster_color, zorder = 1)
        for cluster_idx in range(len(cluster_list)):
            cluster = cluster_list[cluster_idx]
            cluster_color = COLORS[cluster_idx % len(COLORS)]
            cluster_center = (cluster.horiz_center(), cluster.vert_center())
            for fips_code in cluster.fips_codes():
                line = data_table[fips_to_line[fips_code]]
                plt.plot( [cluster_center[0], line[1]],[cluster_center[1], line[2]], cluster_color, lw=1, zorder = 2)
        for cluster_idx in range(len(cluster_list)):
            cluster = cluster_list[cluster_idx]
            cluster_color = COLORS[cluster_idx % len(COLORS)]
            cluster_center = (cluster.horiz_center(), cluster.vert_center())
            cluster_pop = cluster.total_population()
            plt.scatter(x = [cluster_center[0]], y = [cluster_center[1]], s =  circle_area(cluster_pop), lw = 2,
                        facecolors = "none", edgecolors = "black", zorder = 3)

    plt.show()

def circle_radius(pop):
    """
    Compute radius of circle whose area is proportional to population
    """
    return math.sqrt(pop) / 200
        
def load_data(file):
    """
    Load cancer risk data from .csv file
    """    
    data_file = open(file, 'r', encoding = 'UTF-8')
    data = data_file.read()
    data_lines = data.split('\n')
    print("Loaded", len(data_lines), "data points")
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])] for tokens in data_tokens]

def plot_format(savename):
    plt.xlabel("cluster size", fontsize='large')
    plt.ylabel('running time / s', fontsize='large')
    plt.title('running time of fast and slow pairing')
    savepath = 'C:/Users/shouk/py/projects/clusters/'
    saveformat = '.png'
    resolution = 300
    plt.axis([0, None, 0, None])
    plt.legend(loc = "upper left")
    if os.path.isfile(savepath + savename + saveformat):
        print('file exist!')
        return
    plt.savefig(savepath + savename + saveformat, dpi=resolution, bbox_inches="tight")

def plot_format_error(savename, num):
    plt.xlabel("cluster number", fontsize='large')
    plt.ylabel('distortion x 10^11', fontsize='large')
    plt.title('distortion of 2 methods--' + str(num))
    savepath = 'C:/Users/shouk/py/projects/clusters/'
    saveformat = '.png'
    resolution = 300
    plt.axis([6, 20, 0, None])
    plt.legend(loc = "upper right")
    if os.path.isfile(savepath + savename + saveformat):
        print('file exist!')
        return
    plt.savefig(savepath + savename + saveformat, dpi=resolution, bbox_inches="tight")

def plot_pair_time(start, end):
    
    slow_list = []
    fast_list = []
    for idx in range(start, end):
        rand1 = mtd.gen_random_clusters(idx)
        slow_begin = timer()
        mtd.slow_closest_pair(rand1)
        slow_list.append(timer() - slow_begin)
        fast_begin = timer()
        mtd.fast_closest_pair(rand1)
        fast_list.append(timer() - fast_begin)
    plt.plot(range(start, end), slow_list, '-', label = 'slow closest pair')
    plt.plot(range(start, end), fast_list, '-', label = 'fast closest pair')
    
def plot_hieratical(doc, num):
    data = load_data(doc)
    info = {line[0]:(line[1], line[2], line[3], line[4]) for line in data}
    cluster_list = []
    for line in data:
        cluster_list.append(Cluster(set([line[0]]),line[1],line[2],line[3],line[4]))
    cluster_list = mtd.hierarchical_clustering(cluster_list, num)
    plot_clusters(data, cluster_list, draw_centers = True)
    print(compute_distortion(info, cluster_list))

def plot_kmean(doc, num, iterate_time):
    data = load_data(doc)
    info = {line[0]:(line[1], line[2], line[3], line[4]) for line in data}
    cluster_list = []
    for line in data:
        cluster_list.append(Cluster(set([line[0]]),line[1],line[2],line[3],line[4]))
    cluster_list = mtd.kmeans_clustering(cluster_list, num, iterate_time)
    plot_clusters(data, cluster_list, draw_centers = True)
    #print(compute_distortion(info, cluster_list))
#plot_111()
# =============================================================================
# plot_pair_time(2, 201)
# plot_format('running time')
# =============================================================================
def compute_distortion(info, clusters):
    distor = 0
    for cluster in clusters:
        for county in cluster.fips_codes():
            distor += ((info[county][0] - cluster.horiz_center()) ** 2 + (info[county][1] - cluster.vert_center()) ** 2) * info[county][2]
    return distor

def plot_error(start, end):
    factor = 10 ** 11
    for doc in [DATA_896]:
        data = load_data(doc)
        info = {line[0]:(line[1], line[2], line[3], line[4]) for line in data}
        clusters = []
        for line in data:
            clusters.append(Cluster(set([line[0]]),line[1],line[2],line[3],line[4]))
            
        clusters_hierar = mtd.hierarchical_clustering(clusters, end)
        clusters_kmean = mtd.kmeans_clustering(clusters, end, 6)
        error_hierar, error_kmean = [compute_distortion(info, clusters_hierar)/factor], [compute_distortion(info, clusters_kmean)/factor]
        for num in range(end - 1, start - 1, -1):
            clusters_hierar = mtd.hierarchical_clustering(clusters_hierar, num)
            clusters_kmean = mtd.kmeans_clustering(clusters, num, 6)
            error_hierar.append(compute_distortion(info, clusters_hierar)/factor)
            error_kmean.append(compute_distortion(info, clusters_kmean)/factor)
        #print([range(end, start - 1, -1)], len(range(end, start - 1, -1)))
        #print(error_hierar, len(error_hierar))
        plt.plot(range(end, start - 1, -1), error_hierar, '-', label = 'hierarchical ' + str(len(data)))
        plt.plot(range(end, start - 1, -1), error_kmean, '-', label = 'kmeans ' + str(len(data)))
        print(error_hierar)
        print(error_kmean)
        #print('a')
        plot_format_error('error of methods', len(data))
        
plot_error(6, 20)

#plot_hieratical(DATA_111, 9)
#plot_kmean(DATA_111, 9, 5)