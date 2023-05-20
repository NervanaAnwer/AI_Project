
import math
import numpy as np
import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

WINDOW_LENGTH = 4
# ChromeDriver path
chrome_driver_path = 'D:\\New folder (2)\\chromedriver_win32'  # Replace with the actual path

# Create a Service object
service = Service(executable_path=chrome_driver_path)

# Create a WebDriver instance using the Service object
driver = webdriver.Chrome(service=service)

# Open the web-based Connect 4 game
driver.get('http://kevinshannon.com/connect4/')

# Wait for the game board to be visible and interactive
# Create a WebDriverWait object with the desired timeout
wait = WebDriverWait(driver, 5)  # Timeout set to 5 seconds

# Wait until the element with ID 'game' is visible
game_board_element = wait.until(EC.visibility_of_element_located((By.ID, 'game')))

# Constants
ROW_COUNT = 6
COLUMN_COUNT = 7

# AI constants
AI_PIECE_1 = 1
AI_PIECE_2 = 2
HUMAN_PLAYER = 3

def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True

def evaluate_window(window, piece):
    score = 0
    opponent_piece = 1 if piece == 2 else 2

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opponent_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score
    
    
    
def score_position(board, piece):
    score = 0

    ## Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    ## Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score positive sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def is_terminal_node(board):
    return winning_move(board, AI_PIECE_1) or winning_move(board, AI_PIECE_2) or len(get_valid_locations(board)) == 0

def Alpha_Beta_Pruning(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE_2):
                return (None, 100000000000000)
            elif winning_move(board, AI_PIECE_1):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, AI_PIECE_2))

    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE_2)
            #new_score = minimax(b_copy, depth - 1, False)[1]
            new_score = Alpha_Beta_Pruning(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE_1)
            # new_score = minimax(b_copy, depth - 1, False)[1]
            new_score = Alpha_Beta_Pruning(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def minimax(board, depth, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE_2):
                return (None, 100000000000000)
            elif winning_move(board, AI_PIECE_1):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, AI_PIECE_2))

    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE_2)
            new_score = minimax(b_copy, depth - 1, False)[1]
            if new_score > value:
                value = new_score
                column = col
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE_1)
            new_score = minimax(b_copy, depth - 1, True)[1]
            if new_score < value:
                value = new_score
                column = col
        return column, value


def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col

def play_connect4():
    board = create_board()
    game_over = False
    turn = AI_PIECE_1

    while not game_over:
        if turn == AI_PIECE_1:
            # AI player 1's move
            col, _ = Alpha_Beta_Pruning(board, 5, -math.inf, math.inf, True)
            #col, _ = minimax(board, 5, True)
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE_1)
                if winning_move(board, AI_PIECE_1):
                    print("AI player 1 wins!!")
                    game_over = True
                print_board(board)
                # Perform the move on the web page
                perform_move_on_webpage(col)
                turn = AI_PIECE_2


        elif turn == AI_PIECE_2:
            # AI player 2's move
            col, _ = Alpha_Beta_Pruning(board, 5, -math.inf, math.inf, True)
            #col, _ = minimax(board, 5, True)
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE_2)
                if winning_move(board, AI_PIECE_2):
                    print("AI player 2 wins!!")
                    game_over = True
                print_board(board)
                # Perform the move on the web page
                perform_move_on_webpage(col)
                turn = AI_PIECE_1


def perform_move_on_webpage(col):
    # Calculate the x and y offsets based on the column
 try:
    x_offset = 153.6 + col * 102.1
    y_offset = 125.667

    game_board_element = driver.find_element(By.ID, 'game')  # Use the 'driver' object to find the element
    # Click on the column to make the move
    #print(f"x_offset: {x_offset}, y_offset: {y_offset}")  # Debug statement to check the offsets
    print(f"Performing move at column: {col}")
    print(f"X Offset: {x_offset}, Y Offset: {y_offset}")
    ActionChains(driver).move_to_element_with_offset(game_board_element, x_offset, y_offset).click().perform()
    # Pause for a short while to allow the move to be registered
    time.sleep(2)
 except Exception as e:
      print(f"Error performing move on webpage: {e}")
# Start the game
play_connect4()