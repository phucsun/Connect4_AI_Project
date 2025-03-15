import numpy as np
from constants import *

def create_board():
    return np.zeros((NUM_ROWS, NUM_COLS), dtype=int)

def is_valid_move(board, col):
    return 0 <= col < NUM_COLS and board[0][col] == 0

def drop_piece(board, col, player):
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == 0:
            board[row][col] = player
            return row

def check_winner(board, row, col, player):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        for i in (-1, 1):
            r, c = row, col
            while True:
                r += i * dr
                c += i * dc
                if not (0 <= r < NUM_ROWS and 0 <= c < NUM_COLS):
                    break
                if board[r, c] != player:
                    break
                count += 1
                if count >= WINNING_COUNT:
                    return True
    return False

def get_valid_moves(board):
    return [col for col in range(NUM_COLS) if is_valid_move(board, col)]

def is_game_tied(board):
    return len(get_valid_moves(board)) == 0