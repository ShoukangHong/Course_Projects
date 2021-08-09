"""
Visualizer for county-based cancer data - Data is collated from two sources

Overall lifetime cancer risk from air toxics
http://www.epa.gov/ttn/atw/nata2005/tables.html
T
Geographic county locations are computed from and relative to this image
http://commons.wikimedia.org/wiki/File:USA_Counties_with_FIPS_and_names.svg
"""

import math
from cluster_class import Cluster
import cluster_method as mtd
import cluster_class as alg_cluster

# Constants
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 634

# Assets
DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
MAP_URL = DIRECTORY + "data_clustering/USA_Counties.png"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
DATA_111 = 'C:/Users/shouk/py/projects/clusters/unifiedCancerData_111.csv'

def risk_color(risk):
    """
    Compute color associated with risk
    """
    magnitude = int(720 * (-math.log(risk, 10) - 4.3))
    magnitude = max(min(magnitude, 255), 0)
    color = "hsl(" + str(magnitude) + ",100%,50%)"
    return color

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


data_set = load_data(DATA_111)
cluster_list = []
for data in data_set[:5]:
    cluster_list.append(Cluster(set([data[0]]),data[1], data[2],data[3], data[4]))
#print(cluster_list)
test_list = [Cluster(set([1,5,6]),0,0,1,1),
             Cluster(set([2]),0,4,1,1),
             Cluster(set([3, 7]),4,0,1,1),
             Cluster(set([4]),4,2,1,1),
    ]
# =============================================================================
# print(mtd.closest_pair_strip([Cluster(set([1]), -4.0, 0.0, 1, 0),
#                               Cluster(set([2]), 0.0, -1.0, 1, 0),
#                               Cluster(set([3]), 0.0, 1.0, 1, 0),
#                               Cluster(set([4]), 4.0, 0.0, 1, 0)], 0.0, 4.123106))
# =============================================================================
#print(mtd.slow_closest_pair(test_list))
# =============================================================================
# print()
# print(mtd.hierarchical_clustering(test_list, 3))
# print()
print(mtd.kmeans_clustering(cluster_list[:10], 3, 2))
# =============================================================================
print()
TEST_CASE= [alg_cluster.Cluster(set(['00']), 0.0, 0.0, 1, 0.1), 
             alg_cluster.Cluster(set(['10']), 1.0, 0.0, 2, 0.1), 
             alg_cluster.Cluster(set(['11']), 1.0, 1.0, 3, 0.1), 
             alg_cluster.Cluster(set(['01']), 0.0, 1.0, 4, 0.1), 
             alg_cluster.Cluster(set(['1010']), 10.0, 10.0, 5, 0.1), 
             alg_cluster.Cluster(set(['1011']), 10.0, 11.0, 6, 0.1), 
             alg_cluster.Cluster(set(['1111']), 11.0, 11.0, 7, 0.1), 
             alg_cluster.Cluster(set(['1110']), 11.0, 10.0, 8, 0.1)]
print(mtd.kmeans_clustering(TEST_CASE, 4, 2))

    
    