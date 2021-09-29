# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 16:18:56 2021
@author: shouk
"""

def stableMatching(n, menPreferences, womenPreferences):
    # Initially, all n men are unmarried
    unmarriedMen = list(range(n))
    # None of the men has a spouse yet, we denote this by the value None
    manSpouse = [None] * n                      
    # None of the women has a spouse yet, we denote this by the value None
    womanSpouse = [None] * n                      
    # Each man made 0 proposals, which means that 
    # his next proposal will be to the woman number 0 in his list
    nextManChoice = [0] * n                       
    
    # While there exists at least one unmarried man:
    while unmarriedMen:
        # Pick an arbitrary unmarried man
        he = unmarriedMen[0]                      
        # Store his ranking in this variable for convenience
        hisPreferences = menPreferences[he]       
        # Find a woman to propose to
        she = hisPreferences[nextManChoice[he]] 
        # Store her ranking in this variable for convenience
        herPreferences = womenPreferences[she]
        # Find the present husband of the selected woman (it might be None)
        currentHusband = womanSpouse[she]    
        
        # Now "he" proposes to "she". 
        # Decide whether "she" accepts, and update the following fields
        # 1. manSpouse
        # 2. womanSpouse
        # 3. unmarriedMen
        # 4. nextManChoice
        
        if currentHusband == None:
            womanSpouse[she] = he
            manSpouse[he] = she
            unmarriedMen.pop(0)
        elif herPreferences.index(currentHusband) > herPreferences.index(he):
            manSpouse[currentHusband] = None
            unmarriedMen.append(currentHusband)
            womanSpouse[she] = he
            manSpouse[he] = she
            unmarriedMen.pop(0)
        hisPreferences.pop(0)
            
    return manSpouse

menPreferences = [[0, 1, 3, 2], [0, 2, 3, 1], [1, 0, 2, 3], [0, 3, 1, 2]] 
womenPreferences = [[3, 1, 2, 0], [3, 1, 0, 2], [0, 3, 1, 2], [1, 0, 3, 2]]

assert(stableMatching(1, [ [0] ], [ [0] ]) == [0])
assert(stableMatching(2, [ [0,1], [1,0] ], [ [0,1], [1,0] ]) == [0, 1])
assert (stableMatching(4, menPreferences, womenPreferences) == [1,2,3,0])