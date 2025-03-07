import numpy as np
import pygame
import sys
#Constants
NUM_ROWS = 6
NUM_COLS = 7
WINNING_COUNT = 4
size_of_square = 100
SCREEN_HEIGHT = (NUM_ROWS+1) * size_of_square
SCREEN_WIDTH = NUM_COLS * size_of_square
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
def game_over(board, player):
    # Check for horizontal win
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if np.all(board[row, col:col + 4] == player):
                return True

    # Check for vertical win
    for col in range(NUM_COLS):
        for row in range(NUM_ROWS - 3):
            if np.all(board[row:row + 4, col] == player):
                return True

    # Check for diagonal win
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if all(board[row + i, col + i] == player for i in range(WINNING_COUNT)):
                return True

    # Check for anti-diagonal win
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if all(board[row - i, col + i] == player for i in range(WINNING_COUNT)):
                return True

    return False  # Nếu không tìm thấy chuỗi thắng nào
def new_game():
    return np.zeros((NUM_ROWS, NUM_COLS), dtype=int)

def is_valid_move(board, col):
    return 0 <= col <= 6 and board[0][col] == 0
def drop_piece(board, col, player):
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == 0:
            board[row][col] = player
            break
    return board
def draw_board(screen, board):
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            pygame.draw.rect(screen, (0, 0, 255), (col * size_of_square, row * size_of_square + size_of_square, size_of_square, size_of_square))
            pygame.draw.circle(screen, (0, 0, 0), (col * size_of_square + size_of_square // 2, row * size_of_square + size_of_square + size_of_square // 2), size_of_square // 2 - 5)
            if board[row][col] == 1:
                pygame.draw.circle(screen, (255, 0, 0), (col * size_of_square + size_of_square // 2, row * size_of_square + size_of_square + size_of_square // 2), size_of_square // 2 - 5)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, (255, 255, 0), (col * size_of_square + size_of_square // 2, row * size_of_square + size_of_square + size_of_square // 2), size_of_square // 2 - 5)
    pygame.display.update()

def play():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    board = new_game()
    turn = 1
    draw_board(screen, board)
    end_game = False
    while not end_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        # print(board)
        # if turn == 1:
        #     col = int(input("Player 1, enter a column: "))
        #     if is_valid_move(board, col):
        #         board = drop_piece(board, col, 1)
        #         if game_over(board, 1):
        #             print(board)
        #             print("Player 1 wins!")
        #             end_game = True
        #
        #         turn = 2
        #     else:
        #         print("Invalid move, try again.")
        # else :
        #     col = int(input("Player 2, enter a column: "))
        #     if is_valid_move(board, col):
        #         board = drop_piece(board, col, 2)
        #         if game_over(board, 2):
        #             print(board)
        #             print("Player 2 wins!")
        #             end_game = True
        #         turn = 1
        #     else:
        #         print("Invalid move, try again.")

def main():
    play()

main()