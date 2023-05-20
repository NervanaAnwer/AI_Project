
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
    