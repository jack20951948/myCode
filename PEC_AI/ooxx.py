def checkWinScore(B):
    o_win = 'o_win'
    x_win = 'x_win'
    even = 'even'
    for i in B + list(map(list, zip(*B))) + [[B[0][0], B[1][1], B[2][2]], [B[0][2], B[1][1], B[2][0]]]:
        if i == ['o', 'o', 'o']:
            return 1
        elif i == ['x', 'x', 'x']:
            return -1
    if checkVoid(B) != 0:
        return -2
    return 0

def placeValue(now_board, value):
    step = 1
    for row_index, row in enumerate(now_board):
        for col_index, col in enumerate(row):
            if value == step:
                if col == 0:
                    now_board[row_index][col_index] = 'o'
                else:
                    print('Wrong place!')
                return now_board 
            step += 1
                    
def checkVoid(board):
    count = 0
    for row in board:
        for col in row:
            if col == 0:
                count += 1
    return count

def main():
    Board = [['x', 0, 0],
             ['x', 0, 'o'],
             ['o', 'o', 'x']]
    print(checkWinScore(Board))
    Game = [[0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]]

    human = 'o'
    ai = 'x'

    win_player = {
        1:'O_win', -1:'X_win', 0:'Even', -2:'Countinue',
    }

    while checkVoid(Game) != 0 and not(checkWinScore(Game) == 1) and not(checkWinScore(Game) == -1) :
        playerInput = int(input('Your turn:'))
        Game = placeValue(Game, playerInput)
        print(Game[0])
        print(Game[1])
        print(Game[2])
        print(win_player[checkWinScore(Game)])
        
    
main()