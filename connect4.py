import numpy as np

#Constants
NUM_ROWS = 6
NUM_COLS = 7
WINNING_COUNT = 4
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

def play():
    board = new_game()
    turn = 1
    end_game = False
    while not end_game:
        print(board)
        if turn == 1:
            col = int(input("Player 1, enter a column: "))
            if is_valid_move(board, col):
                board = drop_piece(board, col, 1)
                if game_over(board, 1):
                    print(board)
                    print("Player 1 wins!")
                    end_game = True

                turn = 2
            else:
                print("Invalid move, try again.")
        else :
            col = int(input("Player 2, enter a column: "))
            if is_valid_move(board, col):
                board = drop_piece(board, col, 2)
                if game_over(board, 2):
                    print(board)
                    print("Player 2 wins!")
                    end_game = True
                turn = 1
            else:
                print("Invalid move, try again.")

def main():
    play()

main()