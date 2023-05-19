import numpy as np

EMPTY = 0
RED = 1
BLUE = 2


def evaluate(board):
    # Check rows for winning positions
    for i in range(6):
        row = list(board[i])
        for j in range(4):
            window = row[j:j + 4]
            if window.count(RED) == 4:
                return 100
    # Check columns for winning positions
    for i in range(7):
        col = list(board[:, i])
        for j in range(3):
            window = col[j:j + 4]
            if window.count(RED) == 4:
                return 100
    # Check diagonals for winning positions
    for i in range(3):
        for j in range(4):
            window = [board[i + k, j + k] for k in range(4)]
            if window.count(RED) == 4:
                return 100
    for i in range(3):
        for j in range(4):
            window = [board[i + 3 - k, j + k] for k in range(4)]
            if window.count(RED) == 4:
                return 100
    # If there are no winning positions, return 0
    return 0


def game_over(board):
    # Convert board to NumPy array if it is a list
    if isinstance(board, list):
        board = np.array(board, dtype=object)

    # Check rows for winning positions
    for i in range(6):
        row = board[i, :]
        for j in range(4):
            window = row[j:j + 4]
            if np.count_nonzero(window == RED) == 4:
                return True
    # Check columns for winning positions
    for i in range(7):
        col = board[:, i]
        for j in range(3):
            window = col[j:j + 4]
            if np.count_nonzero(window == RED) == 4:
                return True
    # Check diagonals for winning positions
    for i in range(3):
        for j in range(4):
            window = np.array([board[i + k, j + k] for k in range(4)])
            window = window.reshape(1, 4)

            if np.count_nonzero(window == RED) == 4:
                return True
    for i in range(3):
        for j in range(4):
            window = np.array([board[i + 3 - k, j + k] for k in range(4)])
            window = window.reshape(1, 4)

            if np.count_nonzero(window == RED) == 4:
                return True
    # Check if there are any empty squares
    if np.count_nonzero(board) == 42:
        return True
    # If none of the above conditions are met, the game is not over
    return False


def get_possible_moves(board):
    moves = []
    for i in range(7):
        if board[0][i] == EMPTY:
            for j in range(5, -1, -1):
                if board[j][i] == EMPTY:
                    moves.append((j, i))
                    break
    return moves


def make_move(board, move, player):
    board[move[0], move[1]] = player
    return board


def get_valid_moves(board):
    valid_moves = []
    for col in range(7):
        if board[0][col] == EMPTY:
            valid_moves.append(col)
    return valid_moves


def alpha_beta_pruning(board, depth, alpha, beta, maximizing_player):
    if game_over(board) or depth == 0:
        return evaluate(board), None
    if maximizing_player:
        value = -np.inf
        best_move = None
        for move in get_possible_moves(board):
            new_board = make_move(board.copy(), move, RED)
            new_score, _ = alpha_beta_pruning(new_board, depth - 1, alpha, beta, False)
            if new_score > value:
                value = new_score
                best_move = move
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value, best_move
    else:
        value = np.inf
        best_move = None
        for move in get_possible_moves(board):
            new_board = make_move(board.copy(), move, BLUE)
            new_score, _ = alpha_beta_pruning(new_board, depth - 1, alpha, beta, True)
            if new_score < value:
                value = new_score
                best_move = move
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value, best_move



