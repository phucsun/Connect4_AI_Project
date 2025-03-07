import numpy as np
import pygame
import sys
import math

# Constants
NUM_ROWS = 6
NUM_COLS = 7
WINNING_COUNT = 4
size_of_square = 100
SCREEN_HEIGHT = (NUM_ROWS + 1) * size_of_square
SCREEN_WIDTH = NUM_COLS * size_of_square
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# Initialize pygame
pygame.init()
font = pygame.font.SysFont("None", 75)


def new_game():
    return np.zeros((NUM_ROWS, NUM_COLS), dtype=int)


def is_valid_move(board, col):
    return 0 <= col < NUM_COLS and board[0][col] == 0


def drop_piece(board, col, player):
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == 0:
            board[row][col] = player
            break
    return board


def game_over(board, player):
    # Check horizontal, vertical, diagonal, and anti-diagonal wins
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if np.all(board[row, col:col + 4] == player):
                return True
    for col in range(NUM_COLS):
        for row in range(NUM_ROWS - 3):
            if np.all(board[row:row + 4, col] == player):
                return True
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if all(board[row + i, col + i] == player for i in range(WINNING_COUNT)):
                return True
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if all(board[row - i, col + i] == player for i in range(WINNING_COUNT)):
                return True
    return False


def draw_board(screen, board):
    screen.fill((0, 0, 0))
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            pygame.draw.rect(screen, (0, 0, 255),(col * size_of_square, row * size_of_square + size_of_square, size_of_square,size_of_square))
            color = (0, 0, 0)
            if board[row][col] == 1:
                color = (255, 0, 0)
            elif board[row][col] == 2:
                color = (255, 255, 0)
            pygame.draw.circle(screen, color,(col * size_of_square + size_of_square / 2,row * size_of_square + size_of_square + size_of_square / 2),size_of_square / 2 - 5)
    pygame.display.update()


def play():
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    board = new_game()
    turn = 1
    game_running = True
    draw_board(screen, board)

    while game_running:
        # clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                screen.fill((0, 0, 0), (0, 0, SCREEN_WIDTH, size_of_square))
                posX = event.pos[0]
                col = int(math.floor(posX / size_of_square))
                color = (255, 0, 0) if turn == 1 else (255, 255, 0)
                pygame.draw.circle(screen, color, (col * size_of_square + size_of_square / 2, size_of_square / 2),size_of_square / 2 - 5)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                screen.fill((0, 0, 0), (0, 0, SCREEN_WIDTH, size_of_square))
                posX = event.pos[0]
                col = int(math.floor(posX / size_of_square))

                if is_valid_move(board, col):
                    board = drop_piece(board, col, turn)
                    draw_board(screen, board)

                    if game_over(board, turn):
                        text = font.render(f"Player {turn} wins!", True, (255, 255, 255))
                        screen.blit(text, (40, 10))
                        pygame.display.update()
                        pygame.time.wait(3000)
                        game_running = False

                    turn = 3 - turn

    pygame.quit()


if __name__ == "__main__":
    play()
