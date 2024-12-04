import pygame, sys
from constants import *
from sudoku_generator import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")
number_font = pygame.font.Font(None, NUMBER_FONT)
sketch_font = pygame.font.Font(None, SKETCH_FONT)

board = SudokuGenerator(9, 30)
board.fill_diagonal()
board.fill_remaining(0, 0)
board.remove_cells()
updated = board.get_board()
saved = board.get_board()
sketched = [[0] * 9 for _ in range(9)]  # Sketched array is reset to an empty grid

selected_cell = None
game_over = False
wins = 0


def draw_grid():
    for row in range(1, 9):
        pygame.draw.line(screen, LINE_COLOR, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), 1)
        pygame.draw.line(screen, LINE_COLOR, (row * SQUARE_SIZE, 0), (row * SQUARE_SIZE, HEIGHT - 60), 1)


def draw_numbers():
    # Draw numbers from the updated array (locked numbers)
    for row in range(9):
        for col in range(9):
            number = updated[row][col]
            if number != 0:  # Draw non-empty cells
                number_surf = number_font.render(str(number), True, LINE_COLOR)
                number_rect = number_surf.get_rect(
                    center=(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2))
                screen.blit(number_surf, number_rect)

    # Draw numbers from the sketched array (temporary numbers)
    for row in range(9):
        for col in range(9):
            number = sketched[row][col]
            if number != 0:  # Draw non-empty cells
                number_surf = sketch_font.render(str(number), True, SKETCH_COLOR)
                number_rect = number_surf.get_rect(
                    topleft=(col * SQUARE_SIZE + 5, row * SQUARE_SIZE + 5))  # Position at the top-left corner
                screen.blit(number_surf, number_rect)


def sketch(row, col, number):
    # Update the position to place the number in the top-left of the cell
    number_surf = sketch_font.render(str(number), True, SKETCH_COLOR)
    number_rect = number_surf.get_rect(
        topleft=(col * SQUARE_SIZE + 5, row * SQUARE_SIZE + 5))  # Adjust the +5 for a little padding from the corner
    screen.blit(number_surf, number_rect)
    sketched[row][col] = number


def clear_cell(row, col):
    sketched[row][col] = 0  # Only remove the sketch from sketched array


def enter_number(row, col):
    if sketched[row][col] != 0:  # Only update if the cell has a sketch
        updated[row][col] = sketched[row][col]  # Lock the number into the board
        sketched[row][col] = 0  # Remove sketch after confirming


screen.fill(BG_COLOR)
draw_grid()
draw_numbers()

keyDict = {}

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

        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7,
                             pygame.K_8, pygame.K_9]:
                number = event.key - pygame.K_1 + 1  # Get number from key press
                if selected_cell:
                    row, col = selected_cell
                    if saved[row][col] == 0:  # Only allow sketching in empty cells
                        sketch(row, col, number)

            if event.key == pygame.K_BACKSPACE:
                if selected_cell:
                    row, col = selected_cell
                    if saved[row][col] == 0:  # Only clear if the cell is empty
                        clear_cell(row, col)

            if event.key == pygame.K_RETURN:  # Press Enter to confirm the number
                if selected_cell:
                    row, col = selected_cell
                    if saved[row][col] == 0:  # Only confirm in empty cells
                        enter_number(row, col)

    screen.fill(BG_COLOR)  # Clear the screen before redrawing everything
    draw_grid()
    draw_numbers()

    for row in range(9):
        for col in range(9):
            pygame.draw.rect(screen, (0, 0, 0), (col * 60, row * 60, SQUARE_SIZE, SQUARE_SIZE), 1)
            if selected_cell == (row, col):
                pygame.draw.rect(screen, (255, 0, 0), (col * 60, row * 60, SQUARE_SIZE, SQUARE_SIZE), 1)

    pygame.display.update()
