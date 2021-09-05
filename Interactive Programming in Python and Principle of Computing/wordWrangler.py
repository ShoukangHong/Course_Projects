"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.
    Returns a new sorted list with the same elements in list1, but
    with no duplicates.
    This function can be iterative.
    """
    if list1 == []:
        return list1
    result = [list1[0]]
    for word in list1:
        if word != result[len(result) - 1]:
            result.append(word)
    return result

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.
    Returns a new sorted list containing only elements that are in
    both list1 and list2.
    This function can be iterative.
    """
    idx, idy = 0, 0
    result = []
    while idx < len(list1) and idy < len(list2):
        if list1[idx] == list2[idy]:
            result.append(list1[idx])
            idx += 1
            idy += 1
        elif list1[idx] < list2[idy]:
            idx += 1
        else:
            idy += 1
    return result

def merge(list1, list2):
    """
    Merge two sorted lists.
    Returns a new sorted list containing those elements that are in
    either list1 or list2.
    This function can be iterative.
    """
    result = []
    idx, idy = 0, 0
    while idx < len(list1) or idy < len(list2):
        if idy >= len(list2):
            result.append(list1[idx])
            idx += 1
        elif idx >= len(list1) or list1[idx] >= list2[idy]:
            result.append(list2[idy])
            idy += 1
        else:
            result.append(list1[idx])
            idx += 1
    return result
                
def merge_sort(list1):
    """
    Sort the elements of list1.
    Return a new sorted list with the same elements as list1.
    This function should be recursive.
    """
    if len(list1) <= 1:
        return list1
    mid = len(list1) // 2
    part1 = merge_sort(list1[:mid])
    part2 = merge_sort(list1[mid:])
    return merge(part1, part2)

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.
    Returns a list of all strings that can be formed from the letters
    in word.
    This function should be recursive.
    """
    if len(word) == 0:
        return ['']
    sub_word = gen_all_strings(word[1:])
    insert = word[0]
    tmp = []
    for string in sub_word:
        for idx in range(len(string) + 1):
            tmp.append(string[:idx] + insert + string[idx:])
    return sub_word + tmp

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.
    Returns a list of strings.
    """
    url = codeskulptor.file2url(filename)
    dictionary = []
    for line in urllib2.urlopen(url).readlines():
        dictionary.append(line[:-1])
    return dictionary

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

run()
#sb = gen_all_strings('ab')
##print str(len(sb))
#for aa in sb:
#    print aa