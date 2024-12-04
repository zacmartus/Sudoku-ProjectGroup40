import pygame
import sys
from sudoku_generator import SudokuGenerator


class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.sketched_value = 0  # Default sketched value is 0
        self.selected = False
        self.locked = value != 0  # Cells with a non-zero value are locked and cannot be changed

    def set_cell_value(self, value):
        if not self.locked:  # Prevent changing locked values
            self.value = value
            self.locked = True
            self.sketched_value = 0  # Clear the sketched value after confirming

    def set_sketched_value(self, value):
        if not self.locked:  # Only allow sketching in unlocked cells
            self.sketched_value = value

    def clear_sketched_value(self):
        self.sketched_value = 0  # Clear the sketched value when necessary

    def draw(self):
        x = self.col * 60
        y = self.row * 60
        # Highlight the selected cell with a red border
        if self.selected:
            pygame.draw.rect(self.screen, (255, 0, 0), (x, y, 60, 60), 3)
        else:
            pygame.draw.rect(self.screen, (0, 0, 0), (x, y, 60, 60), 1)

        # Draw the locked value (fixed numbers)
        if self.value != 0:
            font = pygame.font.Font(None, 36)
            text = font.render(str(self.value), True, (0, 0, 0))
            text_rect = text.get_rect(center=(x + 30, y + 30))  # Center the text in the cell
            self.screen.blit(text, text_rect)

        # Draw the sketched value (half the size of normal number, top-left corner)
        if self.sketched_value != 0:
            font = pygame.font.Font(None, 18)  # Smaller font size for the sketch
            text = font.render(str(self.sketched_value), True, (128, 128, 128))  # Gray color for sketches
            text_rect = text.get_rect(topleft=(x + 5, y + 5))  # Top-left corner
            self.screen.blit(text, text_rect)


class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.selected_row = None
        self.selected_col = None
        self.cells = self.initialize_cells()

    def initialize_cells(self):
        removed_cells = {
            'easy': 30,
            'medium': 40,
            'hard': 50
        }[self.difficulty]
        generator = SudokuGenerator(9, removed_cells)
        generator.fill_values()
        generator.remove_cells()
        board = generator.get_board()
        return [[Cell(board[row][col], row, col, self.screen) for col in range(9)] for row in range(9)]

    def draw(self):
        self.screen.fill((255, 255, 255))
        for row in self.cells:
            for cell in row:
                cell.draw()
        # Draw the grid lines
        for i in range(10):
            line_width = 3 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, (0, 0, 0), (i * 60, 0), (i * 60, 540), line_width)
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * 60), (540, i * 60), line_width)

    def click(self, x, y):
        if 0 <= x < 540 and 0 <= y < 540:
            row = y // 60
            col = x // 60
            return (row, col)
        return None

    def select(self, row, col):
        if self.selected_row is not None and self.selected_col is not None:
            self.cells[self.selected_row][self.selected_col].selected = False
        self.selected_row = row
        self.selected_col = col
        self.cells[row][col].selected = True

    def clear(self):
        if self.selected_row is not None and self.selected_col is not None:
            cell = self.cells[self.selected_row][self.selected_col]
            if not cell.locked:  # Only clear if the cell is not locked
                cell.clear_sketched_value()

    def sketch(self, value):
        if self.selected_row is not None and self.selected_col is not None:
            self.cells[self.selected_row][self.selected_col].set_sketched_value(value)

    def place_number(self, value):
        if self.selected_row is not None and self.selected_col is not None:
            self.cells[self.selected_row][self.selected_col].set_cell_value(value)

    def reset_to_original(self):
        self.cells = self.initialize_cells()
        self.selected_row = None
        self.selected_col = None

    def is_full(self):
        return all(cell.value != 0 for row in self.cells for cell in row)

    def check_board(self):
        # Check rows
        for i in range(9):
            nums = set()
            for j in range(9):
                nums.add(self.cells[i][j].value)
            if len(nums) != 9:
                return False
        # Check columns
        for j in range(9):
            nums = set()
            for i in range(9):
                nums.add(self.cells[i][j].value)
            if len(nums) != 9:
                return False
        # Check boxes
        for box in range(9):
            nums = set()
            box_row = (box // 3) * 3
            box_col = (box % 3) * 3
            for i in range(3):
                for j in range(3):
                    nums.add(self.cells[box_row + i][box_col + j].value)
            if len(nums) != 9:
                return False
        return True


def main():
    pygame.init()
    pygame.font.init()
    WINDOW_SIZE = 540
    SCREEN = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 60))
    pygame.display.set_caption("Sudoku")
    game_state = "start"
    board = None
    game_over = False
    result_message = ""

    while True:
        if game_state == "start":
            SCREEN.fill((255, 255, 255))
            font = pygame.font.Font(None, 48)
            title = font.render("Welcome to Sudoku", True, (0, 0, 0))
            SCREEN.blit(title, (WINDOW_SIZE // 2 - title.get_width() // 2, 100))
            difficulties = ["EASY", "MEDIUM", "HARD"]
            buttons = []
            for i, diff in enumerate(difficulties):
                button = pygame.Rect(WINDOW_SIZE // 2 - 100, 250 + i * 80, 200, 50)
                pygame.draw.rect(SCREEN, (255, 165, 0), button)
                font = pygame.font.Font(None, 36)
                text = font.render(diff, True, (0, 0, 0))
                SCREEN.blit(text, (button.centerx - text.get_width() // 2, button.centery - text.get_height() // 2))
                buttons.append((button, diff.lower()))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for button, difficulty in buttons:
                        if button.collidepoint(mouse_pos):
                            board = Board(WINDOW_SIZE, WINDOW_SIZE, SCREEN, difficulty)
                            game_state = "playing"
        elif game_state == "playing":
            board.draw()
            # Draw buttons
            buttons = []
            labels = ["Reset", "Restart", "Exit"]
            for i, label in enumerate(labels):
                button = pygame.Rect(20 + i * 180, WINDOW_SIZE + 10, 160, 40)
                pygame.draw.rect(SCREEN, (255, 165, 0), button)
                font = pygame.font.Font(None, 36)
                text = font.render(label, True, (0, 0, 0))
                SCREEN.blit(text, (button.centerx - text.get_width() // 2, button.centery - text.get_height() // 2))
                buttons.append((button, label.lower()))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    clicked = board.click(mouse_pos[0], mouse_pos[1])
                    if clicked:
                        row, col = clicked
                        board.select(row, col)
                    for button, action in buttons:
                        if button.collidepoint(mouse_pos):
                            if action == "reset":
                                board.reset_to_original()
                                game_over = False
                                result_message = ""
                            elif action == "restart":
                                game_state = "start"
                            elif action == "exit":
                                pygame.quit()
                                sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                                     pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                        value = int(event.unicode)
                        board.sketch(value)
                    elif event.key == pygame.K_RETURN:
                        # Confirm the sketched value as a locked value
                        if board.selected_row is not None and board.selected_col is not None:
                            cell = board.cells[board.selected_row][board.selected_col]
                            if cell.sketched_value != 0:
                                cell.set_cell_value(cell.sketched_value)
                    elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                        board.clear()
                        # Also clear the sketched value
                        if board.selected_row is not None and board.selected_col is not None:
                            cell = board.cells[board.selected_row][board.selected_col]
                            cell.clear_sketched_value()
                if board.is_full():
                    if board.check_board():
                        game_state = "won"
                    else:
                        game_state = "lost"

        elif game_state in ["won", "lost"]:
            pygame.time.delay(1000)
            overlay = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE + 60))
            overlay.fill((255, 255, 255))
            overlay.set_alpha(230)
            SCREEN.blit(overlay, (0, 0))
            font = pygame.font.Font(None, 48)
            if game_state == "won":
                text = font.render("Game Won!", True, (0, 0, 0))
            else:
                text = font.render("Game Over :(", True, (0, 0, 0))
            SCREEN.blit(text, (WINDOW_SIZE // 2 - text.get_width() // 2, WINDOW_SIZE // 2 - 50))
            button = pygame.Rect(WINDOW_SIZE // 2 - 60, WINDOW_SIZE // 2 + 20, 120, 40)
            pygame.draw.rect(SCREEN, (255, 165, 0), button)
            font = pygame.font.Font(None, 36)
            text = font.render("RESTART" if game_state == "lost" else "EXIT", True, (0, 0, 0))
            SCREEN.blit(text, (button.centerx - text.get_width() // 2, button.centery - text.get_height() // 2))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button.collidepoint(event.pos):
                        if game_state == "won":
                            pygame.quit()
                            sys.exit()
                        else:
                            game_state = "start"

        pygame.display.flip()


if __name__ == "__main__":
    main()
