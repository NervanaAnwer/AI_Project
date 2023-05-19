
import numpy as np
import random
from board import Board

# Define the players
ai = 1


# Define the evaluation function for the board
def evaluate(board):
    # Check rows for winning positions
    for i in range(6):
        row = list(board[i, :])
        for j in range(4):
            window = row[j:j+4]
            if window.count(ai) == 4:
                return 100
    # Check columns for winning positions
    for i in range(7):
        col = list(board[:, i])
        for j in range(3):
            window = col[j:j+4]
            if window.count(ai) == 4:
                return 100
    # Check diagonals for winning positions
    for i in range(3):
        for j in range(4):
            window = [board[i+k][j+k] for k in range(4)]
            if window.count(ai) == 4:
                return 100
    for i in range(3):
        for j in range(4):
            window = [board[i+3-k][j+k] for k in range(4)]
            if window.count(ai) == 4:
                return 100
    # If there are no winning positions, return 0
    return 0
