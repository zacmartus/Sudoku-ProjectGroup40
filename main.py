import pygame, sys
from constants import *
from sudoku_generator import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")
number_font = pygame.font.Font(None, NUMBER_FONT)

board = SudokuGenerator(9, 30)
board.fill_diagonal()
board.fill_remaining(0, 0)
board.remove_cells()
updated = board.get_board()

game_over = False
wins = 0

def draw_grid():
    # draw horizontal lines
    for i in range(1, BOARD_ROWS):

        pygame.draw.line(
            screen,
            LINE_COLOR,
            (0, i * SQUARE_SIZE),
            (WIDTH, i * SQUARE_SIZE),
            LINE_WIDTH
        )

    #draw vertical lines
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (i * SQUARE_SIZE, 0),
            (i * SQUARE_SIZE, HEIGHT - 60),
            LINE_WIDTH
        )

    pygame.draw.line(screen,
                     LINE_COLOR,
                     (0, HEIGHT - 60),
                     (WIDTH, HEIGHT - 60),
                     3
                     )

    pygame.draw.line(screen,
                     LINE_COLOR,
                     (0, HEIGHT - 240),
                     (WIDTH, HEIGHT - 240),
                     3
                     )

    pygame.draw.line(screen,
                     LINE_COLOR,
                     (0, HEIGHT - 420),
                     (WIDTH, HEIGHT - 420),
                     3
                     )

    pygame.draw.line(screen,
                     LINE_COLOR,
                     (HEIGHT - 420, 0),
                     (HEIGHT - 420, WIDTH),
                     3
                     )

    pygame.draw.line(screen,
                     LINE_COLOR,
                     (HEIGHT - 240, 0),
                     (HEIGHT - 240, WIDTH),
                     3
                     )


def draw_numbers():
    number_surf1 = number_font.render('1', True, LINE_COLOR)
    number_surf2 = number_font.render('2', True, LINE_COLOR)
    number_surf3 = number_font.render('3', True, LINE_COLOR)
    number_surf4 = number_font.render('4', True, LINE_COLOR)
    number_surf5 = number_font.render('5', True, LINE_COLOR)
    number_surf6 = number_font.render('6', True, LINE_COLOR)
    number_surf7 = number_font.render('7', True, LINE_COLOR)
    number_surf8 = number_font.render('8', True, LINE_COLOR)
    number_surf9 = number_font.render('9', True, LINE_COLOR)

    number_rect = number_surf1.get_rect(center=(270, 270))

    for row in range(0, 9):
        for col in range(0, 9):
            if updated[row][col] == '1':
                number_rect = number_surf1.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2))
                screen.blit(number_surf1, number_rect)
            elif updated[row][col] == '2':
                number_rect = number_surf2.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2))
                screen.blit(number_surf2, number_rect)
            elif updated[row][col] == '3':
                number_rect = number_surf3.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2))
                screen.blit(number_surf3, number_rect)
            elif updated[row][col] == '4':
                number_rect = number_surf4.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2))
                screen.blit(number_surf4, number_rect)
            elif updated[row][col] == '5':
                number_rect = number_surf5.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2))
                screen.blit(number_surf5, number_rect)
            elif updated[row][col] == '6':
                number_rect = number_surf6.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2))
                screen.blit(number_surf6, number_rect)
            elif updated[row][col] == '7':
                number_rect = number_surf7.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2))
                screen.blit(number_surf7, number_rect)
            elif updated[row][col] == '8':
                number_rect = number_surf8.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2))
                screen.blit(number_surf8, number_rect)
            elif updated[row][col] == '9':
                number_rect = number_surf9.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2))
                screen.blit(number_surf9, number_rect)


screen.fill(BG_COLOR)
draw_grid()
draw_numbers()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            row = y // SQUARE_SIZE
            col = x // SQUARE_SIZE

    pygame.display.update()
