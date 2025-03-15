import pygame
import sys
from constants import *
from board import is_valid_move, drop_piece, check_winner
from minimax import minimax
from display import draw_board

def handle_events(event, screen, board, turn):
    winner = None

    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    if event.type == pygame.MOUSEMOTION:
        screen.fill(BLACK, (0, 0, SCREEN_WIDTH, SQUARE_SIZE))
        x_pos = max(SQUARE_SIZE // 2, min(event.pos[0], SCREEN_WIDTH - SQUARE_SIZE // 2))
        pygame.draw.circle(screen, YELLOW, (x_pos, SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)
        pygame.display.flip()

    # Người chơi đi
    if turn == PLAYER_TURN and event.type == pygame.MOUSEBUTTONDOWN:
        col = event.pos[0] // SQUARE_SIZE
        if is_valid_move(board, col):
            row = drop_piece(board, col, PLAYER_TURN)
            draw_board(screen, board)
            if check_winner(board, row, col, PLAYER_TURN):
                winner = PLAYER_TURN
            return board, AI_TURN, winner  # Chuyển lượt sang AI

    # AI đi
    if turn == AI_TURN:
        col, _ = minimax(board, depth=4, turn=AI_TURN)
        if is_valid_move(board, col):
            row = drop_piece(board, col, AI_TURN)
            draw_board(screen, board)
            if check_winner(board, row, col, AI_TURN):
                winner = AI_TURN
            return board, PLAYER_TURN, winner

    return board, turn, winner