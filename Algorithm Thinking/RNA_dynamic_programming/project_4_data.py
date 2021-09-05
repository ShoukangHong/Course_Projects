# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 22:25:32 2021
@author: shouk
"""
import urllib3
http = urllib3.PoolManager()

FLY_PROTEIN_PATH = 'alg_FruitflyEyelessProtein.txt'
HUMAN_PROTEIN_PATH = 'alg_HumanEyelessProtein.txt'
PROTEIN_SCORE_PATH = 'alg_PAM50.txt'
CONSENSUS_PATH = 'alg_ConsensusPAXDomain.txt'
WORD_PATH = 'http://storage.googleapis.com/codeskulptor-assets/assets_scrabble_words3.txt'

def load_seq(flie_path):
    file = open(flie_path, 'r', encoding = 'UTF-8')
    seq = file.read()
    seq = seq.rstrip()
    return seq

def load_scoring_file():
    scoring_file = open(PROTEIN_SCORE_PATH, 'r', encoding = 'UTF-8')
    scoring_dict = {}
    ykeys = scoring_file.readline()
    ykeychars = ykeys.split()
    for line in scoring_file.readlines():
        vals = line.split()
        xkey = vals.pop(0)
        scoring_dict[xkey] = {}
        for ykey, val in zip(ykeychars, vals):
            scoring_dict[xkey][ykey] = int(val)
    return scoring_dict

def load_words():
    word_file = http.request('GET', WORD_PATH)
    word_text = word_file.data.decode('UTF-8')
    word_list = word_text.split('\n')
    print("Loaded a dictionary with", len(word_list), "words")
    return word_list

# =============================================================================
# print(load_seq(FLY_PROTEIN_PATH))
# print(load_seq(HUMAN_PROTEIN_PATH))
# print(load_seq(CONSENSUS_PATH))
# print(load_scoring_file())
# print(load_words()[:20])
# =============================================================================
