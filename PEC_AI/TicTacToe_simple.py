board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]
human = 'X'
computer = 'O'

def evaluate(state):
    if wins(state, computer):
        score = +1
    elif wins(state, human):
        score = -1
    else:
        score = 0
    return score

def wins(state, player):
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False

def empty_cells(state):
    cells = []
    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])
    return cells

def minimax(brd, depth, player):
    if player == computer :
        best = [-1, -1, -2,+5]
    else:
        best = [-1, -1, +2,+5]

    if depth == 0 or wins(brd, human) or wins(brd, computer):
        score = evaluate(brd)
        return [-1, -1, score, 0]

    for cell in empty_cells(brd):
        x, y = cell[0], cell[1]
        brd[x][y] = player
        if player == human:
            score = minimax(brd, depth - 1, computer)
        else:
            score = minimax(brd, depth - 1, human)

        brd[x][y] = 0
        score[0], score[1] = x, y
        
        if player == computer:
            score[3] = score[3] + 1

            if score[2] == 1 and score[3] < best[3]:
                best = score
            elif score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value
    return best

def computer_turn(player):
    print("computer turn:")
    depth = len(empty_cells(board))
    if depth == 0 or wins(board, human) or wins(board, computer):
        return

    move = minimax(board, depth, computer)
    #print("computer move: ", move)
    board[move[0]][move[1]] = player

def human_turn(player):
    depth = len(empty_cells(board))
    if depth == 0 or wins(board, human) or wins(board, computer):
        return

    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }
    move = int(input('your turn:\nEnter (1 ~ 9): '))
    coord = moves[move]
    board[coord[0]][coord[1]] = player

def main():
    # Main loop of this game
    while len(empty_cells(board)) > 0 and not wins(board, human) and not wins(board, computer):
        human_turn(human)
        print(board[0])
        print(board[1])
        print(board[2])
        computer_turn(computer)
        print(board[0])
        print(board[1])
        print(board[2])
    # Game over message
    print("the end:")
    if wins(board, human):
        print('YOU WIN!')
    elif wins(board, computer):
        print('YOU LOSE!')
    else:
        print('DRAW!')

main()
