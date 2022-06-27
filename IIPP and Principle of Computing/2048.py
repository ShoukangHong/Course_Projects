"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}


def merge(line):
    '''merge grids'''
    idx = 0
    result = list(line)
    while idx < len(result) - 1:
        result.append(0)
        result.remove(0)
        idx += 1
    idx = 0
    while idx < len(result) - 1:
        if result[idx] and result[idx] == result[idx + 1]:
            result.pop(idx + 1)
            result[idx] *= 2
            result.append(0)
        idx += 1
    return result

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        self._width = grid_width
        self._height = grid_height
        self.reset()
        self._dict = {}
        self._dict[DOWN] = [[self._height - 1, idx] for idx in range(self._width)]
        self._dict[UP] = [[0, idx] for idx in range(self._width)]
        self._dict[LEFT] = [[idy, 0] for idy in range(self._height)]
        self._dict[RIGHT] = [[idy, self._width - 1] for idy in range(self._height)]
        
    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[0 for dummy_idx in range(self._width)]
                     for dummy_idy in range(self._height)]
        self.new_tile()
        self.new_tile()
        
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # replace with your code
        return str(self._grid)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self._width
    
    def traverse_grid(self, start_cell, direction, num_steps):
        """
        Function that iterates through the cells in a grid
        in a linear direction

        Both start_cell is a tuple(row, col) denoting the
        starting cell

        direction is a tuple that contains difference between
        consecutive cells in the traversal
        """
        result = []
        for step in range(num_steps):
            row = start_cell[0] + step * direction[0]
            col = start_cell[1] + step * direction[1]
            result.append(self._grid[row][col])
        return result
    
    def update_line(self, start_cell, direction, num_steps, line):
        """
        Function that update grids
        """
        for step in range(num_steps):
            row = start_cell[0] + step * direction[0]
            col = start_cell[1] + step * direction[1]
            self._grid[row][col] = line[step]

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        identical = True
        num_steps = self._width * self._height // len(self._dict[direction])
        for start_cell in self._dict[direction]:
            line = self.traverse_grid(start_cell, OFFSETS[direction], num_steps)
            result = merge(line)
            if not (line == result):
                identical = False
            self.update_line(start_cell, OFFSETS[direction], num_steps, result)
        if not identical:
            self.new_tile()
            
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        empty_list = [[idy, idx] for idx in range(self._width)
                     for idy in range(self._height) if self._grid[idy][idx] == 0]
        random.shuffle(empty_list)
        if len(empty_list) > 0:
            pos = empty_list.pop()
            if random.random() > 0.9:
                self._grid[pos[0]][pos[1]] = 4
            else:
                self._grid[pos[0]][pos[1]] = 2

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        # replace with your code
        return self._grid[row][col]

poc_2048_gui.run_gui(TwentyFortyEight(4, 6))
