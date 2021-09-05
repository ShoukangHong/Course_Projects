"""
A dynamic programming method to get the maximum diagonals that can be placed in the n*n table and print one example
This is just for curious, and I didn't spend time to make it readable...
"""
from collections import defaultdict as dd
import time

size = 10
canLine = [] #possible line combinations
listLine = {} #key: combination, val: change combination value to list
countLine = {} #key: combination, val: diagonal count for the line
nextLine = dd(list) # a list of all possible next line combinations
refTable = {0:"   ", 1:" \\ ", 2:" / "}
lineImage = [[] for l in range(size)]

def solve():
    init()
    ans = 0
    bestSeq = {i:[] for i in range(3**size)}
    dp = [[0 for _ in range(3**size)] for _ in range(size + 1)]
    for l in range(size):
        tmp = {i:[] for i in range(3**size)}
        for i in canLine:
            for j in nextLine[i]:
                if (dp[l][i] + countLine[j] > dp[l + 1][j]):
                    dp[l + 1][j] = dp[l][i] + countLine[j]
                    tmp[j] = bestSeq[i] + [j]
                if (dp[l + 1][j] > ans):
                    ans = dp[l + 1][j]
                    best = j
        bestSeq = tmp
        
    print(size*"---" + "--")
    for l in bestSeq[best]:
        print("|" + "".join([refTable[symb] for symb in listLine[l]]) + "|")
    print(size*"---" + "--")
        
    return ans

def checkLine(t):
    iList = []
    cnt = 0
    for k in range(size):
        cur = t % 3
        if cur > 0:
            cnt += 1
        t //= 3
        if k > 0 and cur + iList[k - 1] == 3:
            return False, [], 0
        iList.append(cur)
    return True, iList, cnt

def canNext(i, j):
    iList = listLine[i]
    jList = listLine[j]
    for k in range(size):
        if k > 0 and jList[k] == 1 and iList[k - 1] == 1:
            return False
        if jList[k] + iList[k] == 3:
            return False
        if k < size - 1 and jList[k] == 2 and iList[k + 1] == 2:
            return False
    return True

def init():
    for i in range(3**size):
        ok, l, cnt = checkLine(i)
        if ok:
            canLine.append(i)
            listLine[i] = l
            countLine[i] = cnt
    for i in canLine:
        for j in canLine:
            if canNext(i, j):
                nextLine[i].append(j)

if __name__ == '__main__':
    print("start", time.time())
    print(solve())
    print("finish", time.time())
