import pygame, sys
from constants import *
from sudoku_generator import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")
number_font = pygame.font.Font(None, 60)

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
    number_surf = number_font.render('1', True, LINE_COLOR)
    number_rect = number_surf.get_rect(center=(270, 270))
    screen.blit(number_surf, number_rect)


screen.fill(BG_COLOR)
draw_grid()
draw_numbers()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()