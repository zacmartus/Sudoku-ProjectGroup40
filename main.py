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

selected_cell = None
game_over = False
wins = 0

def draw_grid():
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
    #Render and display the numbers from the Sudoku board
    for row in range(9):
        for col in range(9):
            number = updated[row][col]
            if number != 0:  #draw non-empty cells
                number_surf = number_font.render(str(number), True, LINE_COLOR)
                number_rect = number_surf.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2))
                screen.blit(number_surf, number_rect)


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
            selected_cell = (row, col)

    for row in range(9):
        for col in range(9):
            pygame.draw.rect(screen, (0, 0, 0), (col * 60, row * 60, SQUARE_SIZE, SQUARE_SIZE), 1)
            if selected_cell == (row, col):
                pygame.draw.rect(screen, (255, 0, 0), (col * 60, row * 60, SQUARE_SIZE, SQUARE_SIZE), 1)



    pygame.display.update()
