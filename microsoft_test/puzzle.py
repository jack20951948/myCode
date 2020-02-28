import os
import copy

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
    if (list_add(puzzleX, puzzleY) == [[1, 1, 1], [1, 1, 1], [1, 1, 1]]):
        print("YES")
        os._exit(0)
    else:
        pass

def list_add(a,b):
    retun_ls = []
    ls = list(zip(a,b))
    for i in ls:
        i = list(i)
        c = list(map(lambda x :x[0]+x[1] ,zip(i[0],i[1])))
        retun_ls.append(c)
    return retun_ls

def rotate(matrix):
    return list(map(list,list(zip(*matrix))[::-1]))

def move_up(input_list):
    b = input_list.pop(0)
    input_list.append(b)
    return input_list

def move_down(input_list):
    b = input_list.pop(2)
    input_list.insert(0, b)
    return input_list

def move_left(input_list):
    retun_ls = []
    for i in input_list:
        b = i.pop(0)
        i.append(b)
        retun_ls.append(i)
    return retun_ls

def move_right(input_list):
    retun_ls = []
    for i in input_list:
        b = i.pop(2)
        i.insert(0, b)
        retun_ls.append(i)
    return retun_ls

puzzleA = [0, 0, 0]
puzzleB = [0, 0, 0]

puzzleA[0] = getInput()
puzzleA[1] = getInput()
puzzleA[2] = getInput()
if input() != "":
    print("input error!")
    os._exit(0)
puzzleB[0] = getInput()
puzzleB[1] = getInput()
puzzleB[2] = getInput()

if sum(map(sum, puzzleA)) < sum(map(sum, puzzleB)):
    puzzleX = puzzleA
    puzzleY = puzzleB
else:
    puzzleX = puzzleB
    puzzleY = puzzleA

for i in range(4):
    puzzleX = rotate(puzzleX)
    while puzzleX[0][0] == 0 and puzzleX[1][0] == 0 and puzzleX[2][0] == 0:
        puzzleX = move_left(puzzleX)
    while puzzleX[0] == [0, 0, 0]:
        puzzleX = move_up(puzzleX)
    if (puzzleX[0][1] == 0 and puzzleX[1][1] == 0 and puzzleX[2][1] == 0) or (puzzleX[1] == [0, 0, 0]) or (puzzleX[1][1] == 1 and puzzleX[0][1] == 0 and puzzleX[1][0] == 0):
        print("NO")
        os._exit(0)
    while puzzleX[2] == [0, 0, 0]:
        checkWin()
        tmp_A = copy.deepcopy(puzzleX)
        while puzzleX[0][2] == 0 and puzzleX[1][2] == 0 and puzzleX[2][2] == 0:
            puzzleX = move_right(puzzleX)
            checkWin()
        puzzleX = move_down(tmp_A)
        checkWin()
    while puzzleX[0][2] == 0 and puzzleX[1][2] == 0 and puzzleX[2][2] == 0:
        checkWin()
        puzzleX = move_right(puzzleX)
        checkWin()
    checkWin()
print("NO")