import random
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

#Turn
EMPTY = 0 #Test
PLAYER_TURN = 1
AI_TURN = 2

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
            color = BLACK if board[row][col] == 0 else (RED if board[row][col] == 2 else YELLOW)
            pygame.draw.circle(screen, color,(col * SQUARE_SIZE + SQUARE_SIZE // 2, (row + 1) * SQUARE_SIZE + SQUARE_SIZE // 2),SQUARE_SIZE // 2 - 5)
    pygame.display.flip()

def get_valid_move(board):
    valid_moves = []
    for col in range(NUM_COLS):
        if is_valid_move(board, col):
            valid_moves.append(col)
    return valid_moves

def is_terminal(board, row, col, player):
    return check_winner(board, row, col, player)
def is_game_tied(board):
    return len(get_valid_move(board)) == 0
def evaluate_window(window, piece):
	score = 0
	opp_piece = PLAYER_TURN
	if piece == PLAYER_TURN:
		opp_piece = AI_TURN

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4

	return score
def evaluate(board, piece):
    score = 0
    ## Score center column
    center_array = [int(i) for i in list(board[:, NUM_COLS // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    ## Score Horizontal
    for r in range(NUM_ROWS):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(NUM_COLS - 3):
            window = row_array[c:c + WINNING_COUNT]
            score += evaluate_window(window, piece)

    ## Score Vertical
    for c in range(NUM_COLS):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(NUM_ROWS - 3):
            window = col_array[r:r + WINNING_COUNT]
            score += evaluate_window(window, piece)

    ## Score posiive sloped diagonal
    for r in range(NUM_ROWS - 3):
        for c in range(NUM_COLS - 3):
            window = [board[r + i][c + i] for i in range(WINNING_COUNT)]
            score += evaluate_window(window, piece)

    for r in range(NUM_ROWS - 3):
        for c in range(NUM_COLS - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINNING_COUNT)]
            score += evaluate_window(window, piece)

    return score

#MINIMAX ALGORITHM
def minimax(board, row = 0, col = 0, depth = 4, turn = AI_TURN):
    valid_moves = get_valid_move(board)
    if is_terminal(board, row, col, turn) or depth == 0 or is_game_tied(board):
        if is_terminal(board, row, col, turn):
            if turn == AI_TURN:
                return None, math.inf
            else:
                return None, -math.inf
        elif is_game_tied(board):
            return None, 0
        else:
            return None, evaluate(board, turn)
    if turn == AI_TURN:
        evalu = -math.inf
        column = valid_moves[0]
        for col in valid_moves:
            board_tmp = np.copy(board)
            row = drop_piece(board_tmp, col, AI_TURN)
            score = minimax(board_tmp, row, col, depth - 1, PLAYER_TURN)[1]
            if score > evalu:
                evalu = score
                column = col
        return column, evalu
    else: #Player turn
        evalu = math.inf
        column = valid_moves[0]
        for col in valid_moves:
            board_tmp = np.copy(board)
            row = drop_piece(board_tmp, col, PLAYER_TURN)
            score = minimax(board_tmp, row, col, depth - 1, AI_TURN)[1]
            if score < evalu:
                evalu = score
                column = col
        return column, evalu




def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    board = create_board()
    turn, winner = PLAYER_TURN, None
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
                pygame.draw.circle(screen, RED if turn == 2 else YELLOW, (x_pos, SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)
                pygame.display.flip()
            if turn == PLAYER_TURN:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    col = event.pos[0] // SQUARE_SIZE
                    if is_valid_move(board, col):
                        row = drop_piece(board, col, turn)
                        draw_board(screen, board)
                        if check_winner(board, row, col, turn):
                            winner = turn
                        x_pos = max(SQUARE_SIZE // 2, min(event.pos[0], SCREEN_WIDTH - SQUARE_SIZE // 2))
                        turn = AI_TURN
                        pygame.draw.circle(screen, YELLOW, (x_pos, SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)
                        pygame.display.flip()
            else: #AI Turn
                col, _ = minimax(board, AI_TURN)
                if is_valid_move(board, col):
                    row = drop_piece(board, col, turn)
                    draw_board(screen, board)
                    if check_winner(board, row, col, turn):
                        winner = turn
                    x_pos = max(SQUARE_SIZE // 2, min(event.pos[0], SCREEN_WIDTH - SQUARE_SIZE // 2))
                    turn = PLAYER_TURN
                    pygame.draw.circle(screen, RED, (x_pos, SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)
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
