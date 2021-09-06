# -*- coding: utf-8 -*-
"""
A Backtracking and pruning algorithm to print all possible solutions for the diagonal puzzle
@author: shouk
"""
import time

def diagonalsSolution(size, goal):
    '''given the size of board and goal of diagnal number, print all valid results'''
    refTable = {0:"   ", 1:" \\ ", -1:" / "}
    gridMap = {n:0 for n in range(size*size)}
    total = 0
    
    def printBoard():
        board = [[""] * size for n in range(size)]
        string = size*"---" + "--" + "\n"
        for i in gridMap:
            board[i//size][i%size] = refTable[gridMap[i]]
        for row in board:
            string += "|" + "".join(row) + "|" + "\n"
        print(string + size*"---" + "--")
     
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
            
    def backTrack(cur = 0):
        nonlocal total
        for n in range(cur, size*size):
            for symb in [1, -1]:
                if n <= (size*size + total - goal) and isValid(n, symb):
                    gridMap[n] = symb
                    total += 1
                    if total == goal:
                        printBoard()
                    else:
                        backTrack(n + 1)
                    gridMap[n] = 0
                    total -= 1
    backTrack()

if __name__ == '__main__':
    start = time.time()
    diagonalsSolution(5,16)
    print("finished in", str(time.time() - start)[:5], "seconds")
