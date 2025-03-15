import pygame
from constants import *

def draw_board(screen, board):
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            pygame.draw.rect(screen, BLUE, (col * SQUARE_SIZE, (row + 1) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            color = BLACK if board[row][col] == 0 else (RED if board[row][col] == 2 else YELLOW)
            pygame.draw.circle(screen, color, (col * SQUARE_SIZE + SQUARE_SIZE // 2, (row + 1) * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)
    pygame.display.flip()