# -*- coding: utf-8 -*-
"""
Created on Sun Jun  6 10:50:50 2021
scores and frequency of 1000 rand vs fly
@author: shouk
"""
import math
SCORES = [53, 51, 49, 45, 44, 46, 47, 52, 42, 60, 63, 48, 55, 57, 79, 50, 65, 68, 69, 56, 77, 54, 58, 40, 43, 38, 62, 59, 64, 61, 71, 70, 41, 67, 85, 82, 83, 39, 66, 75, 72, 76, 74, 78, 73, 84, 91, 80, 88, 92]
FREQUENCIES = [0.058, 0.058, 0.067, 0.049, 0.051, 0.058, 0.055, 0.055, 0.024, 0.022, 0.015, 0.065, 0.042, 0.036, 0.003, 0.057, 0.014, 0.007, 0.005, 0.041, 0.001, 0.05, 0.029, 0.003, 0.029, 0.001, 0.013, 0.023, 0.013, 0.009, 0.006, 0.003, 0.008, 0.005, 0.001, 0.001, 0.001, 0.002, 0.006, 0.002, 0.002, 0.001, 0.001, 0.001, 0.001, 0.002, 0.001, 0.001, 0.001, 0.001]

DISTRIBUTION = {SCORES[num]:FREQUENCIES[num] for num in range(len(SCORES))}

def mean_score(distribution):
    mean = 0
    for score, freq in distribution.items():
        mean += score * freq
    return mean

def deviation(distribution):
    mean = mean_score(distribution)
    deviation_square = 0
    for score, freq in distribution.items():
       deviation_square += freq * (score - mean) ** 2
    return math.sqrt(deviation_square)
    
print(mean_score(DISTRIBUTION))
print(deviation(DISTRIBUTION))

# mean 52.291000000000004
# deviation 7.565072306329927