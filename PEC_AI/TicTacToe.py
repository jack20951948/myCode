from math import inf as infinity
import platform
import time
from os import system

# set HUMAN as -1, COMPUTER as +1 to represent the player's choice on board
HUMAN = -1
COMP = +1
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

# evalute score, if computer wins return +1, if human wins return -1, if draw return 0
def evaluate(state):
    if wins(state, COMP):
        score = +1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0
    return score

# return true if the player is in the win states (8 conditions)
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

# return if the game is finished
def game_over(state):
    return wins(state, HUMAN) or wins(state, COMP)

# list the empty cells
def empty_cells(state):
    cells = []
    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])
    return cells

# if the move is valid (if the chosen cell is empty)
def valid_move(x, y):
    if [x, y] in empty_cells(board):
        return True
    else:
        return False

# set the move on board
def set_move(x, y, player):
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False

# find the best move for the computer, and will return a list with [the best row, best column, best score]
def minimax(state, depth, player):
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    # if there is no empty cell or the game is finished, then return final result (win or draw or lose)
    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    # consider every empty cells and find the best move
    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        # find the best score after set this move
        score = minimax(state, depth - 1, -player)
        # recover this move
        state[x][y] = 0
        # record the coordinate of this move
        score[0], score[1] = x, y
        # find the move that will win or draw
        if player == COMP:
            # if the score is better than the current best score, replace the best move ([row, column, score])
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value
    return best

# clear the console
def clean():
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')

# plot the board
def render(state, c_choice, h_choice):
    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }
    print('\n' + '---------------')
    for row in state:
        for cell in row:
            symbol = chars[cell]
            print('| {} |'.format(symbol), end='')
        print('\n' + '---------------')

# call minmax function to find the best move
def ai_turn(c_choice, h_choice):
    # set depth to the number of remaining empty cells
    depth = len(empty_cells(board))
    # if there is no empty cell or the game is finished, then return nothing to end this turn
    if depth == 0 or game_over(board):
        return

    clean()
    print(f'Computer turn [{c_choice}]')
    render(board, c_choice, h_choice)

    # find the best move
    move = minimax(board, depth, COMP)
    x, y = move[0], move[1]

    # set move on the board
    set_move(x, y, COMP)

# Human's turn and choose a valid move
def human_turn(c_choice, h_choice):
    # set depth to the number of remaining empty cells
    depth = len(empty_cells(board))
    # if there is no empty cell or the game is finished, then return nothing to end this turn
    if depth == 0 or game_over(board):
        return

    # initialize move to -1 as default
    move = -1
    # Dictionary of valid moves
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    clean()
    print('Human turn [{}]'.format(h_choice))
    # show board
    render(board, c_choice, h_choice)

    # detect user's input if the move is between 1-9 (cell's number)
    while move < 1 or move > 9:
        try:
            move = int(input('Use numpad (1..9): '))
            # find the corresponding coordinate
            coord = moves[move]
            # set move on the board if the coordinate is empty (valid), else return false
            can_move = set_move(coord[0], coord[1], HUMAN)
            if not can_move:
                print('Bad move')
                move = -1
        # if the input is out of range (1-9)
        except (KeyError, ValueError):
            print('Bad choice')

def main():
    """
    Main function that calls all functions
    """
    h_choice = 'X'  # X or O
    c_choice = 'O'  # X or O

    # Main loop of this game
    # if there are empty cells and the game is not finished
    while len(empty_cells(board)) > 0 and not game_over(board):
        human_turn(c_choice, h_choice)
        ai_turn(c_choice, h_choice)

    clean()
    # Game over message
    if wins(board, HUMAN):
        print(f'Human turn [{h_choice}]')
        render(board, c_choice, h_choice)
        print('YOU WIN!')
    elif wins(board, COMP):
        print(f'Computer turn [{c_choice}]')
        render(board, c_choice, h_choice)
        print('YOU LOSE!')
    else:
        render(board, c_choice, h_choice)
        print('DRAW!')

if __name__ == '__main__':
    main()

