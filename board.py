"""
import numpy as np
from PIL import ImageGrab
import pyautogui
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


# YOU MAY NEED TO CHANGE THESE VALUES BASED ON YOUR SCREEN SIZE
LEFT = 927
TOP = 200
RIGHT = 753
BOTTOM = 600

EMPTY = 0
RED = 1
BLUE = 2


class Board:
    def __init__(self, driver):
        self.driver = driver
    """
from selenium.common import TimeoutException

"""
def _init_(self) -> None:
  self.board = [[EMPTY for i in range(7)] for j in range(6)]

def print_grid(self, grid):
  for i in range(0, len(grid)):
      for j in range(0, len(grid[i])):
          if grid[i][j] == EMPTY:
              print("*", end=" \t")
          elif grid[i][j] == RED:
              print("R", end=" \t")
          elif grid[i][j] == BLUE:
              print("B", end=" \t")
      print("\n")

def _convert_grid_to_color(self, grid):
  for i in range(0, len(grid)):
      for j in range(0, len(grid[i])):
          if grid[i][j] == (255, 255, 255):
              grid[i][j] = EMPTY
          elif grid[i][j][0] > 200:
              grid[i][j] = RED
          elif grid[i][j][0] > 50:
              grid[i][j] = BLUE
  return grid

def _get_grid_cordinates(self):
  startCord = (50, 55)
  cordArr = []
  for i in range(0, 7):
      for j in range(0, 6):
          x = startCord[0] + i * 115
          y = startCord[1] + j * 112
          cordArr.append((x, y))
  return cordArr

def _transpose_grid(self, grid):
  return [[grid[j][i] for j in range(len(grid))] for i in range(len(grid[0]))]

def _capture_image(self):
  image = ImageGrab.grab()
  cropedImage = image.crop((LEFT, TOP, RIGHT, BOTTOM))
  return cropedImage

def _convert_image_to_grid(self, image):
  pixels = [[] for i in range(7)]
  i = 0
  for index, cord in enumerate(self._get_grid_cordinates()):
      pixel = image.getpixel(cord)
      if index % 6 == 0 and index != 0:
          i += 1
      pixels[i].append(pixel)
  return pixels

def _get_grid(self):
  cropedImage = self._capture_image()
  pixels = self._convert_image_to_grid(cropedImage)
  cropedImage.show()
  grid = self._transpose_grid(pixels)
  return grid

def _check_if_game_end(self, grid):
  for i in range(0, len(grid)):
      for j in range(0, len(grid[i])):
          if grid[i][j] == EMPTY and self.board[i][j] != EMPTY:
              return True
  return False

def get_game_grid(self):
  game_grid = self._get_grid()
  new_grid = self._convert_grid_to_color(game_grid)
  is_game_end = self._check_if_game_end(new_grid)
  self.board = new_grid
  return (self.board, is_game_end)

def select_column(self, column):
  pyautogui.click(
      self._get_grid_cordinates()[column][1] + LEFT,
      self._get_grid_cordinates()[column][0] + TOP,
  )
"""
"""
    def is_valid_move(self, col):
        return self.board[0][col] == 0

    def make_move(self, column):
        # Make a move in the web-based game by clicking on the specified column
        column_element = self.driver.find_element(By.CSS_SELECTOR, f'[data-col="{column}"]')
        action = ActionChains(self.driver)
        action.move_to_element(column_element).click().perform()

    def get_game_board(self):
        # Get the current game board from the web page
        board_elements = self.driver.find_elements('css selector', '.game-square')
        board = np.zeros((6, 7), dtype=int)
        for i, element in enumerate(board_elements):
            class_name = element.get_attribute('class')
            if 'player-red' in class_name:
                board[i // 7, i % 7] = 1
            elif 'player-yellow' in class_name:
                board[i // 7, i % 7] = 2
        return board

    def print_board(self):
        for row in self.board:
            print("\t".join(str(cell) for cell in row))
            print("\n")


def is_terminal_node(board):
    # Check for a win condition
    # Check rows for a win
    for row in range(6):
        for col in range(4):
            if board[row][col] != 0 and board[row][col] == board[row][col + 1] == board[row][col + 2] == board[row][
                col + 3]:
                return True
    # Check columns for a win
    for col in range(7):
        for row in range(3):
            if board[row][col] != 0 and board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][
                col]:
                return True
    # Check diagonals (top-left to bottom-right) for a win
    for row in range(3):
        for col in range(4):
            if board[row][col] != 0 and board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == \
                    board[row + 3][col + 3]:
                return True
    # Check diagonals (top-right to bottom-left) for a win
    for row in range(3):
        for col in range(3, 7):
            if board[row][col] != 0 and board[row][col] == board[row + 1][col - 1] == board[row + 2][col - 2] == \
                    board[row + 3][col - 3]:
                return True

    # Check for a draw condition
    if np.count_nonzero(board) == 42:
        return True

    # Return False if the game is not over
    return False
"""
"""
import numpy as np

class Board:
    def __init__(self):
        self.board = np.zeros((6, 7), dtype=int)

    def is_valid_move(self, col):
        return self.board[0][col] == 0

    def make_move(self, column, player):
        self.board[column][np.where(self.board[column] == 0)[0][-1]] = player

    def get_game_board(self):
        return self.board

    def print_board(self):
        for row in self.board:
            print("\t".join(str(cell) for cell in row))
            print("\n")
"""
from telnetlib import EC

import numpy as np
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class Board:
    def __init__(self, driver):
        self.driver = driver

    def is_valid_move(self, col):
        return self.get_game_board()[0][col] == 0

    def make_move(self, column):
        try:
            wait = WebDriverWait(self.driver, 10)
            column_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f'[data-col="{column}"]')))
            action = ActionChains(self.driver)
            action.move_to_element(column_element).click().perform()
        except TimeoutException:
            print(f"TimeoutException: Failed to locate the column element for column {column}.")

    def get_game_board(self):
        # Get the current game board from the web page
        board_elements = self.driver.find_elements(By.CSS_SELECTOR, '.game-square')
        board = np.zeros((6, 7), dtype=int)
        for i, element in enumerate(board_elements):
            class_name = element.get_attribute('class')
            if 'player-red' in class_name:
                board[i // 7, i % 7] = 1
            elif 'player-yellow' in class_name:
                board[i // 7, i % 7] = 2
        return board

    def print_board(self):
        board = self.get_game_board()
        for row in board:
            print("\t".join(str(cell) for cell in row))
            print("\n")
