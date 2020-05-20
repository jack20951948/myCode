
def is_distinct( list ):
    #Check to see if the items in the list are distinct
    used = []
    for i in list:
        if i == 0:
            continue
        elif i in used:
            return False
        else:
            used.append(i)
    return True


def is_valid( brd ):
    #Check all the rows and columns
    for i in range(3):
        row = [brd[i][0],brd[i][1],brd[i][2]]
        if not is_distinct(row):
            return False
        col = [brd[0][i],brd[1][i],brd[2][i]]
        if not is_distinct(col):
            return False
    return True

def solve( brd , empties = 9):
    '''
      Solves a mini-Sudoku
      brd is the board
      empty is the number of empty cells
    '''

    if empties == 0:
        #Base case
        return is_valid( brd )
    for row,col in [[i,j] for i in [0,1,2] for j in [0,1,2]]:
        #Run through every element
        if brd[row][col] != 0:
            #If its not empty jump
            continue
        else:
            for test in [1,2,3]:
                brd[row][col] = test
                if is_valid(brd) and solve(brd,empties-1):
                    return True
                else:
                    #BackTrack
                    brd[row][col] = 0
    return False

Board = [ [ 0 , 0 , 0 ],
          [ 1 , 2 , 0 ],
          [ 0 , 0 , 1 ] ]
solve( Board , 9 - 3 )


for row in Board:#Prints a solution
    print (row)