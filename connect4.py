import numpy as np
import pygame
import sys
import math

# Constants
NUM_ROWS, NUM_COLS, WINNING_COUNT = 6, 7, 4
SQUARE_SIZE = 100
SCREEN_WIDTH, SCREEN_HEIGHT = NUM_COLS * SQUARE_SIZE, (NUM_ROWS + 1) * SQUARE_SIZE

# Colors
BLUE, BLACK, RED, YELLOW, WHITE = (0, 0, 255), (0, 0, 0), (255, 0, 0), (255, 255, 0), (255, 255, 255)

# Initialize pygame
pygame.init()
font = pygame.font.SysFont(None, 75)


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


def draw_board(screen, board):
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            pygame.draw.rect(screen, BLUE, (col * SQUARE_SIZE, (row + 1) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            color = BLACK if board[row][col] == 0 else (RED if board[row][col] == 1 else YELLOW)
            pygame.draw.circle(screen, color,(col * SQUARE_SIZE + SQUARE_SIZE // 2, (row + 1) * SQUARE_SIZE + SQUARE_SIZE // 2),SQUARE_SIZE // 2 - 5)
    pygame.display.flip()


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    board = create_board()
    turn, winner = 1, None
    draw_board(screen, board)

    while winner is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                screen.fill(BLACK, (0, 0, SCREEN_WIDTH, SQUARE_SIZE))
                col = event.pos[0] // SQUARE_SIZE
                x_pos = max(SQUARE_SIZE // 2, min(event.pos[0], SCREEN_WIDTH - SQUARE_SIZE // 2))
                pygame.draw.circle(screen, RED if turn == 1 else YELLOW, (x_pos, SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)
                pygame.display.flip()

            if event.type == pygame.MOUSEBUTTONDOWN:
                col = event.pos[0] // SQUARE_SIZE
                if is_valid_move(board, col):
                    row = drop_piece(board, col, turn)
                    draw_board(screen, board)
                    if check_winner(board, row, col, turn):
                        winner = turn
                    x_pos = max(SQUARE_SIZE // 2, min(event.pos[0], SCREEN_WIDTH - SQUARE_SIZE // 2))
                    turn = 3 - turn
                    pygame.draw.circle(screen, RED if turn == 1 else YELLOW, (x_pos, SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)
                    pygame.display.flip()
    screen.fill(BLACK, (0, 0, SCREEN_WIDTH, SQUARE_SIZE))
    text = font.render(f"Player {winner} wins!", True, WHITE)
    screen.blit(text, (40, 10))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
