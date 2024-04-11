import random
from data import get_random_color
from shapes import xShape, circleShape

class Player:
    def __init__(self, window, name, color, sign):
        self.window = window
        self.name = name
        self.color = color
        self.sign = sign

    def shape(self, x, y, animation=False):
        if self.sign == 'x':
            return xShape(window=self.window,
                          x=x, y=y,
                          color=self.color,
                          size=70,
                          width=7,
                          center=True,
                          is_animation=animation)
        else:
            return circleShape(window=self.window,
                               x=x, y=y,
                               color=self.color,
                               size=43,
                               width=7,
                               is_animation=animation)

class PC(Player):
    def __init__(self, window, sign):
        super().__init__(window=window,
                         name='PC',
                         color=get_random_color(),  # Assigning a random color for the PC player
                         sign=sign)
        self.timer = False  # Flag to control timer for PC's move
        self.ready = False  # Flag to indicate PC's readiness to make a move

    def make_move(self, game_grid, grid_tracker, empty_cells):
        # Function to check if the next move results in winning for a specific player
        def check_next_move(grid, sign):
            for i in range(3):
                if all(grid[i][j] == sign for j in range(3)) or \
                        all(grid[j][i] == sign for j in range(3)):
                    return True
            if all(grid[i][i] == sign for i in range(3)) or \
                    all(grid[i][2 - i] == sign for i in range(3)):
                return True
            return False

        # Determining the opponent's sign
        enemy_sign = 'x' if self.sign != 'x' else 'o'

        # Trying to win the game or prevent the opponent from winning
        for cell in empty_cells:
            row, col = cell
            if check_next_move(grid_tracker, self.sign):
                # If the PC can win in the next move, make that move
                grid_block = game_grid[row][col]
                grid_block.set_sign(sign_obj=self.shape(x=grid_block.rect.x + grid_block.rect.width // 2,
                                                        y=grid_block.rect.y + grid_block.rect.height // 2,
                                                        animation=True),
                                    sign=self.sign)
                return
            else:
                grid_tracker[row][col] = ''  # Resetting the grid tracker

        # If winning is not possible, try to block the opponent's winning move
        for cell in empty_cells:
            row, col = cell
            grid_tracker[row][col] = enemy_sign
            if check_next_move(grid_tracker, enemy_sign):
                # If the opponent can win in the next move, block that move
                grid_block = game_grid[row][col]
                grid_block.set_sign(sign_obj=self.shape(x=grid_block.rect.x + grid_block.rect.width // 2,
                                                        y=grid_block.rect.y + grid_block.rect.height // 2,
                                                        animation=True),
                                    sign=self.sign)
                grid_tracker[row][col] = self.sign
                return
            else:
                grid_tracker[row][col] = ''  # Resetting the grid tracker

        # If no winning move or blocking move is available, choose a random empty cell
        row, col = random.choice(empty_cells)
        grid_block = game_grid[row][col]
        grid_block.set_sign(sign_obj=self.shape(x=grid_block.rect.x + grid_block.rect.width // 2,
                                                y=grid_block.rect.y + grid_block.rect.height // 2,
                                                animation=True),
                            sign=self.sign)
        grid_tracker[row][col] = self.sign
