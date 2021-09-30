# -*- coding: utf-8 -*-
"""

@author: shouk
"""
def solveNQueens(n: int):
    '''return all valid solutions for n queen problem'''
    ans = []
    perms = []
    perm = [-1] * n
    s = {i:'.' * i + 'Q' + '.' * (n-i-1) for i in range(n)}
    def canPlace(y, x):
        for y2 in range(n):
            x2 = perm[y2]
            if x2 >= 0 and abs(y - y2) == abs(x - x2):
                return False
        return True
    
    def getPerms(n):
        if n == 0:
            ans.append('\n'.join([s[i] for i in perm]))
            return
        for i in range(len(perm)):
            if perm[i] == -1 and canPlace(i, n-1):
                perm[i] = n - 1
                getPerms(n - 1)
                perm[i] = - 1
    getPerms(n)
    for board in ans:
      print(board)
      print('')
    return ans

solveNQueens(4)
