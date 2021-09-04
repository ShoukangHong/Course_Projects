# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 14:33:05 2021

@author: shouk
"""

def diagonalsSolution(size, goal):
    '''given the size and num of diagnals, print all valid results '''
    refTable = {0:" . ", 1:"\\ ", -1:"// "}
    gridMap = {n:0 for n in range(size*size)}
    total = 0
    
    def printBoard():
        board = [[""] * size for n in range(size)]
        for i in gridMap:
            board[i//size][i%size] = refTable[gridMap[i]]
        for row in board:
            print(row)
        print()
     
    def isValid(n, symb):
        if n%size != 0:
            if gridMap.get(n-1, 0) == -symb:
                return False
            if symb == 1 == gridMap.get(n - size - 1, 0):
                return False
        if gridMap.get(n - size, 0) == -symb:
            return False
        if (n + 1)%size != 0 and symb == -1 == gridMap.get(n-size + 1, 0):
            return False
        return True
            
    def backTrace(cur = 0):
        nonlocal total
        for n in range(cur, size*size):
            for symb in [1, -1]:
                if n <= (size*size + total - goal) and isValid(n, symb):
                    gridMap[n] = symb
                    total += 1
                    if total == goal:
                        printBoard()
                    else:
                        backTrace(n + 1)
                    gridMap[n] = 0
                    total -= 1
    backTrace()
                
diagonalsSolution(5,16)
