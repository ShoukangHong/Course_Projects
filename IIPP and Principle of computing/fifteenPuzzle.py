"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

def dist(y_1, x_1, y_2, x_2):
    '''get dist'''
    return abs(y_1 - y_2) + abs(x_1 - x_2)

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]
        self._map ={1:lambda row, col, number: [[[idy > row or (idy == row and idx > col) or number == self._grid[idy][idx],''] 
                      for idx in range(self._width)]
                      for idy in range(self._height)],
                    2:lambda row, col, number:[[[idy > row or number == self._grid[idy][idx],'']
                      for idx in range(self._width)]
                      for idy in range(self._height)],        
                    3:lambda row, col, number:[[[idy > row or idx > col or number == self._grid[idy][idx],'']
                      for idx in range(self._width)]
                      for idy in range(self._height)]}

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    #help functions
    def get_pos(self, number):
        '''get supposed pos of number'''
        for idy in range(self._height):
            for idx in range(self._width):
                if self._grid[idy][idx] == number:
                    return [idy, idx]
                
    def get_val(self, row, col):
        '''get supposed value'''
        return col + self._width * row
                
    def next_grid(self, target_row, target_col):
        '''get next grid'''
        if target_col > 0:
            return [target_row, target_col - 1]
        else:
            return [target_row - 1, self._width - 1]
    
    def four_grids(self, grids, idy, idx):
        '''get four grids'''
        d_x = [0, 0, 1, -1]
        d_y = [1, -1, 0, 0]
        direct = ['d', 'u', 'r', 'l']
        result = []
        for num in range(4):
            pos_y, pos_x = idy + d_y[num], idx + d_x[num]
            if (0 <= pos_y < self._height and 0 <= pos_x < self._width) and grids[pos_y][pos_x][0] == False:
                grids[pos_y][pos_x][0] = True
                grids[pos_y][pos_x][1] += grids[idy][idx][1] + direct[num]
                result.append([pos_y, pos_x])
        return result
    
    def loop_route(self, row, col, target_yx, number = -1, mode = 1):
        '''core route method'''
        grids = self._map[mode](row, col, number)
        edges = []
        #for grid in grids:
        #    print grid
        if number == -1:
            start, end = [row, col], target_yx
        else:
            start, end = target_yx, [row, col]
        edge = start
        #print str(self)
        #print start, end
        while edge != end:
            edges += self.four_grids(grids, edge[0], edge[1])
            edge = edges.pop(0)
        move = grids[edge[0]][edge[1]][1]
        #print move
        if dist(row, col, target_yx[0], target_yx[1]) <= 1 or number != -1:
            self.update_puzzle(move)
            return move
        number = self._grid[target_yx[0]][target_yx[1]]
        #print number
        self.update_puzzle(move)
        return move + self.loop_route(row, col, target_yx, number, mode)
        
    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        if self._grid[target_row][target_col] != 0:
            return False
        for idx in range(target_col + 1, self._width):
            if self._grid[target_row][idx] != idx + self._width * target_row:
                return False
        for idy in range(target_row + 1, self._height):
            for idx in range(self._width):
                if self._grid[idy][idx] != idx + self._width * idy:
                    return False
        return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, target_col)
        result = ''
        val = self.get_val(target_row, target_col)
        target = self.get_pos(val)
        while dist(target_row, target_col, target[0], target[1]) >= 1:
            result += self.loop_route(target_row, target_col,target)
            target = self.get_pos(self.get_val(target_row, target_col))
            #result + self.solve_interior_tile(target_row, target_col)
        next_grid = self.next_grid(target_row, target_col)
        pos_0 = self.get_pos(0)
        return result + self.loop_route(next_grid[0], next_grid[1], pos_0, val)

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        result = 'ur'
        self.update_puzzle(result)
        val = self.get_val(target_row, 0)
        target = self.get_pos(val)
        if target != [target_row, 0]:
            while dist(target[0], target[1], target_row - 1, 1) >= 1:
                #print str(self)
                #print target, target_row - 1, 1
                result += self.loop_route(target_row - 1, 1, target, mode = 2)
                target = self.get_pos(self.get_val(target_row, 0))
            next_grid = [target_row - 1, 0]
            pos_0 = self.get_pos(0)
            #print str(self)
            result += self.loop_route(next_grid[0], next_grid[1], pos_0, val, mode = 2) + 'ruldrdlurdluurddlur'
            self.update_puzzle('ruldrdlurdluurddlur')
        while not self.lower_row_invariant(target_row - 1, self._width - 1):
            result += 'r'
            self.update_puzzle('r')
        return result

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        for idx in range(self._width):
            for idy in range(self._height):
                cur_val = self._grid[idy][idx]
                val = self.get_val(idy, idx)
                if idy >= 2 and cur_val != val:
                    return False
                elif idx > target_col and cur_val != val:
                    return False
                elif idx == target_col and idy == 1 and cur_val != val:
                    return False
                elif idx == target_col and idy == 0 and cur_val != 0:
                    return False
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        for idx in range(self._width):
            for idy in range(self._height):
                cur_val = self._grid[idy][idx]
                val = self.get_val(idy, idx)
                if idy >= 2 and cur_val != val:
                    return False
                elif idx > target_col and cur_val != val:
                    return False
                elif idx == target_col and idy == 1 and cur_val != 0:
                    return False
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        result = 'ld'
        self.update_puzzle(result)
        val = self.get_val(0, target_col)
        target = self.get_pos(val)
        if dist(target[0], target[1], 0, target_col) == 0:
            return result
        while dist(target[0], target[1], 1, target_col - 1) >= 1:
            result += self.loop_route(1, target_col - 1, target, mode = 3)
            target = self.get_pos(val)
        next_grid = [1, target_col - 2]
        pos_0 = self.get_pos(0)
        result += self.loop_route(next_grid[0], next_grid[1], pos_0, val) + 'urdlurrdluldrruld'
        self.update_puzzle('urdlurrdluldrruld')
        return result
    
    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle rdluand returns a move string
        """
        result = ''
        val = self.get_val(1, target_col)
        target = self.get_pos(val)
        while dist(target[0], target[1], 1, target_col) >= 1:
            result += self.loop_route(1, target_col, target, mode = 3)
            target = self.get_pos(val)
        next_grid = [1, target_col - 1]
        pos_0 = self.get_pos(0)
        result += self.loop_route(next_grid[0], next_grid[1], pos_0, val) + 'ur'
        self.update_puzzle('ur')
        return result

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        result = 'ul'
        self.update_puzzle(result)
        count = 0
        while not self.lower_row_invariant(0, 0) and count < 5:
            count += 1
            self.update_puzzle('drul')
            result += 'drul'
        return result

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        result = ''
        cur_row = self._height - 1
        cur_col = self._width - 1
        pos_0 = self.get_pos(0)
        result += self.loop_route(cur_row, cur_col, pos_0, 1000)
        while cur_row >= 2:
            assert self.lower_row_invariant(cur_row, cur_col)
            if cur_col != 0:
                result += self.solve_interior_tile(cur_row, cur_col)
            else:
                result += self.solve_col0_tile(cur_row)
            #print result
            target = self.next_grid(cur_row, cur_col)
            cur_row, cur_col = target[0], target[1]
            #print self
        while cur_col > 1:
            if cur_row == 1:
                assert self.row1_invariant(cur_col)
                result += self.solve_row1_tile(cur_col)
                cur_row -= 1
            else:
                assert self.row0_invariant(cur_col)
                result += self.solve_row0_tile(cur_col)
                cur_row += 1
                cur_col -= 1
            #print self
        result += self.solve_2x2()
        return result

# Start interactive simulation
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))

#test = Puzzle(4, 5)
#test._grid =  [[8, 2, 10, 9, 1], [7, 6, 5, 4, 3], [0, 11, 12, 13, 14], [15, 16, 17, 18, 19]]
#              [9, 8, 5, 10],
#              [7, 6, 12, 11],
#              [3, 0, 14, 15]]
#test._grid = [[2, 14, 0, 3],
#              [4, 5, 6, 7],
#              [8, 9, 10, 11],
#              [12, 13, 1, 15]]
#test.update_puzzle('ddrrruullld')
#print str(test)
##print test.row0_invariant(2)
##print test.row1_invariant(2)
##print test.solve_row0_tile(2)
##print str(test)
##print test.solve_2x2()
#print test.solve_puzzle()
#print str(test)
#print test.solve_interior_tile(3,1)
#print test.lower_row_invariant(0,0)
#print str(test)
#print test.solve_col0_tile(3)
#print str(test)