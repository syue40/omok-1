import pygame

# Define colors of the board
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (250, 202, 8)


class Gomoku_board:
    def __init__(self):
        # Define the size of the board, grid size, backdrop size
        self.grid = []
        self.grid_size = 28
        self.backdrop_size = 16

        self.start_x = 30
        self.start_y = 60

        self.piece = 'black'
        self.piece = 'white'

        self.winner = None
        self.game_over = False

        # Define squares in the grid
        self.grid_count = 19
        for i in range(self.grid_count):
            self.grid.append(list("." * self.grid_count))

    def player_turns(self, event):
        # Define where each click lays an omok piece
        origin_x = 16
        origin_y = 46

        # Define size of each game piece
        size = ((self.grid_count - 1) * self.grid_size) + (self.backdrop_size * 3)
        position = event.pos

        if origin_x <= position[0] <= origin_x + size:
            if origin_y <= position[1] <= origin_y + size:
                if not self.game_over:
                    x = position[0] - origin_x
                    y = position[1] - origin_y

                    row = int(y // self.grid_size)
                    column = int(x // self.grid_size)
                    if self.set_piece(row, column):
                        self.check_win(row, column)
                    else:
                        return
                else:
                    return
            else:
                return
        else:
            return

    def set_piece(self, row, column):
        if self.grid[row][column] == '.':
            self.grid[row][column] = self.piece

            if self.piece == 'black':
                self.piece = 'white'
            else:
                self.piece = 'black'
            return True
        else:
            return False

    def check_win(self, row, column):
        up_count = self.get_count(row, column, -1, 0)
        down_count = self.get_count(row, column, 1, 0)

        right_count = self.get_count(row, column, 0, 1)
        left_count = self.get_count(row, column, 0, -1)

        down_left_diag = self.get_count(row, column, 1, -1)
        down_right_diag = self.get_count(row, column, 1, 1)

        up_left_diag = self.get_count(row, column, -1, -1)
        up_right_diag = self.get_count(row, column, -1, 1)

        # Check if win condition satisfied along x/y axis. If 5 in a row, declare winner.
        if (up_count + down_count == 4) or (right_count + left_count == 4) or \
                (down_right_diag + up_left_diag == 4) or (up_right_diag + down_left_diag == 4):
            self.winner = self.grid[row][column]
            self.game_over = True
        else:
            return

    def get_count(self, row, column, dir_row, dir_col):
        # Keeps count of how many pieces are in a row
        piece = self.grid[row][column]
        result = 0
        i = 1
        while True:
            new_row = row + (dir_row * i)
            new_column = column + (dir_col * i)
            if 0 <= new_row < self.grid_count:
                if 0 <= new_column < self.grid_count:
                    if self.grid[new_row][new_column] == piece:
                        result += 1
                    else:
                        break
                else:
                    break
            else:
                break
            i += 1
        return result

    def draw(self, screen):
        # Draws the backdrop for the board in yellow
        pygame.draw.rect(screen, YELLOW,
                         [self.start_x - self.backdrop_size, self.start_y - self.backdrop_size,
                          (self.grid_count - 1) * self.grid_size + self.backdrop_size * 2,
                          (self.grid_count - 1) * self.grid_size + self.backdrop_size * 2], 0)

        # Draws the black grid lines for rows
        for row in range(self.grid_count):
            y = self.start_y + row * self.grid_size
            pygame.draw.line(screen, BLACK, [self.start_x, y],
                             [self.start_x + self.grid_size * (self.grid_count - 1), y], 2)

        # Draw the black grid lines for column
        for column in range(self.grid_count):
            x = self.start_x + column * self.grid_size
            pygame.draw.line(screen, BLACK, [x, self.start_y],
                             [x, self.start_y + self.grid_size * (self.grid_count - 1)], 2)

        for row in range(self.grid_count):
            for column in range(self.grid_count):
                piece = self.grid[row][column]
                if piece != '.':
                    if piece == 'black':
                        color = BLACK
                    else:
                        color = WHITE

                    x = self.start_x + column * self.grid_size
                    y = self.start_y + row * self.grid_size

                    # Draws each game piece to size
                    pygame.draw.circle(screen, color, [x, y], self.grid_size // 2.5)


class Gomoku():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Gomoku")
        self.screen = pygame.display.set_mode((570, 600))
        self.font = pygame.font.SysFont('Tahoma', 24)
        self.going = True

        self.board = Gomoku_board()

    def update_gomoku(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.going = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.board.player_turns(event)

    def write_to_board(self):
        self.screen.fill(WHITE)
        self.screen.blit(self.font.render("Welcome to Gomoku!", True, BLACK), (20, 10))

        self.board.draw(self.screen)
        if self.board.game_over:
            self.screen.blit(
                self.font.render("{0} Wins!".format("Black" if self.board.winner == 'black' else "White"), True,
                                 BLACK), (420, 10))

        pygame.display.update()

    def main_loop(self):
        while self.going:
            self.update_gomoku()
            self.write_to_board()

        pygame.quit()


def main():
    Gomoku().main_loop()


if __name__ == '__main__':
    main()
