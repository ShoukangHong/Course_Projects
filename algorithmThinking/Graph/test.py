# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
filename =  'C:/STUDY/research data/All-in-one/EIS-accurate-heater-PEO/not accurate/'
filename += 'Li-Li_polished_PEO_EO-LiTFSI_20-1_0_05mm_600000MW_50celcius_Sh_01132021_C06.txt'
text = open(filename, 'r')
idx_freq = 0
idx_re = 1
idx_im = 2
doc = text.readlines()
print(doc[0])

for line in doc:
    print(line)