"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
            
    def __str__(self):
        """
        Return multi-line string represenation for grid
        """
        ans = 'human:' + str(self._human_list)
        ans += '\n' + 'zombie:' + str(self._zombie_list) + '\n'
        for row in range(self._grid_height):
            ans += str(self._cells[row])
            ans += "\n"
        return ans
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        self._cells = [[EMPTY for dummy_col in range(self._grid_width)] 
                       for dummy_row in range(self._grid_height)]
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append([row, col])
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        return [tuple(pos) for pos in self._zombie_list]

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append([row, col])
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        return [tuple(pos) for pos in self._human_list]
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        max_dist = self._grid_width * self._grid_height
        result = [[max_dist for dummy_x in range(self._grid_width)]
                   for dummy_y in range(self._grid_height)]
        count = 0
        if entity_type == HUMAN:
            edges = self.humans()
        else:
            edges = self.zombies()
        while len(edges) > 0:
            tmp = []
            while len(edges) > 0:
                grid = edges.pop(0)
                if self._cells[grid[0]][grid[1]] == FULL:
                    result[grid[0]][grid[1]] = max_dist
                elif result[grid[0]][grid[1]] == max_dist:
                    result[grid[0]][grid[1]] = count
                    tmp.extend(self.four_neighbors(grid[0], grid[1]))
            edges = tmp
            count += 1
        #for row in result:
        #    print str(row)
        return result
    
    def move_humans(self, dist_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        for idx, human in enumerate(self._human_list):
            valid_moves = self.eight_neighbors(human[0], human[1])
            print valid_moves
            best = human
            for grid in valid_moves:
                if self._cells[grid[0]][grid[1]] == FULL:
                    continue
                if dist_field[grid[0]][grid[1]] > dist_field[best[0]][best[1]]:
                    best = grid
            self._human_list[idx] = best
        #print self._human_list
        
    def move_zombies(self, dist_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        for idx, zombie in enumerate(self._zombie_list):
            valid_moves = self.four_neighbors(zombie[0], zombie[1])
            print valid_moves
            best = zombie
            for grid in valid_moves:
                if self._cells[grid[0]][grid[1]] == FULL:
                    continue
                if dist_field[grid[0]][grid[1]] < dist_field[best[0]][best[1]]:
                    best = grid
            self._zombie_list[idx] = best
        #print self._zombie_list

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Apocalypse(20, 5))
