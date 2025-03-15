import pygame
import sys
from constants import *
from board import create_board
from display import draw_board
from handle_event import handle_events

def main():
    pygame.init()
    font = pygame.font.SysFont(None, 75)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    board = create_board()
    turn, winner = PLAYER_TURN, None
    draw_board(screen, board)

    while True:
        for event in pygame.event.get():
            board, turn, winner = handle_events(event, screen, board, turn)

        if winner is not None:
            screen.fill(BLACK, (0, 0, SCREEN_WIDTH, SQUARE_SIZE))
            mess = "Player wins!" if winner == PLAYER_TURN else "AI wins!"
            text = font.render(mess, True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 3, 10))
            pygame.display.flip()

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.quit()
                        sys.exit()

if __name__ == "__main__":
    main()
