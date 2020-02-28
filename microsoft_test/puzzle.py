import os
import numpy as np

def getInput():
    try:
        ls = list(map(int, input().replace(".", "0").replace("*", "1")))
    except:
        print("input error!")
        os._exit(0)
    if len(ls) != 3:
        print("input error!")
        os._exit(0)
    return ls
def checkWin():
    if ((puzzleA + puzzleB) == np.ones(3 * 3).reshape(3, 3)).all():
        print("YES")
        os._exit(0)
    else:
        pass

puzzleA = np.zeros(3 * 3).reshape(3, 3)
puzzleB = np.zeros(3 * 3).reshape(3, 3)

puzzleA[0, ::] = getInput()
puzzleA[1, ::] = getInput()
puzzleA[2, ::] = getInput()
if input() != "":
    print("input error!")
    os._exit(0)
puzzleB[0, ::] = getInput()
puzzleB[1, ::] = getInput()
puzzleB[2, ::] = getInput()

for i in range(4):
    puzzleA = np.rot90(puzzleA, -1)
    while (puzzleA[::, 0] == np.array([0, 0, 0])).all():
        puzzleA = np.roll(puzzleA, -1, axis = 1)
    while (puzzleA[0, ::] == np.array([0, 0, 0])).all():
        puzzleA = np.roll(puzzleA, -1, axis = 0)
    while (puzzleA[2, ::] == np.array([0, 0, 0])).all():
        checkWin()
        tmp_A = puzzleA
        while (puzzleA[::, 2] == np.array([0, 0, 0])).all():
            puzzleA = np.roll(puzzleA, 1, axis = 1)
            checkWin()
        puzzleA = np.roll(tmp_A, 1, axis = 0)
        checkWin()
print("NO")