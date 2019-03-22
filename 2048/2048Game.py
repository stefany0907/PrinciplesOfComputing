#!/usr/bin/python

#http://www.codeskulptor.org/#user39_vIzXiKKY4B_19.py
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
    """
    Helper function that merges a single row or column in 2048
    """
    # replace with your code from the previous mini-project
    tmp_lst = [0 for dummy_element in range(len(line))]
    index = 0
    for line_element in line:
        if line_element != 0:
            tmp_lst[index] = line_element
            index += 1
    for tmp_element in range(len(tmp_lst) - 1):
        if tmp_lst[tmp_element + 1] == tmp_lst[tmp_element]:
            tmp_lst[tmp_element] = tmp_lst[tmp_element + 1] + tmp_lst[tmp_element]
            tmp_lst.pop(tmp_element + 1)
            tmp_lst.append(0)
    return tmp_lst


class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        self._height = grid_height
        self._width = grid_width
        self._grid = [[0 for dummy_col in range(self._width)] for dummy_row in range(self._height)]

        # generate a list of starting cells for each direction given dimension of the grid
        up_indice, down_indice, left_indice, right_indice = [], [], [], []
        for col in range(self._width):
            up_indice.append([0, col])
            down_indice.append([self._height - 1, col])
        for row in range(self._height):
            left_indice.append([row, 0])
            right_indice.append([row, self._width - 1])
            # print UP_indice, DOWN_indice, LEFT_indice, RIGHT_indice
        self._indice = {UP: up_indice,
                        DOWN: down_indice,
                        LEFT: left_indice,
                        RIGHT: right_indice}

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        zero_cells = [[0 for dummy_col in range(self._width)] for dummy_row in range(self._height)]
        self._grid = zero_cells[:]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # for debugging purpose
        return "height=" + str(self._height) + ", width=" + str(self._width)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # Get the height of the board.
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # Get the width of the board.
        return self._width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        old_grid = [[self.get_tile(each_row, each_col) for each_col in range(self._width)] for each_row in
                    range(self._height)]
        flag = True
        tmp_lst = []
        merge_lst = []
        if direction == UP or direction == DOWN:
            for element in self._indice[direction]:
                for step in range(self._height):
                    row_int = element[0] + step * OFFSETS[direction][0]
                    col_int = element[1] + step * OFFSETS[direction][1]
                    tmp_lst.append(self.get_tile(row_int, col_int))
                merge_lst = merge(tmp_lst)
                tmp_lst = []
                for step in range(self._height):
                    self.set_tile(element[0] + step * OFFSETS[direction][0], element[1] + step * OFFSETS[direction][1],
                                  merge_lst[step])
            self._grid = [[self.get_tile(each_row, each_col) for each_col in range(self._width)] for each_row in
                          range(self._height)]
            for _row in range(self._height):
                for _col in range(self._width):
                    if old_grid[_row][_col] != self._grid[_row][_col]:
                        flag = False
            if flag == False:
                self.new_tile()

        if direction == LEFT or direction == RIGHT:
            for element in self._indice[direction]:
                for step in range(self._width):
                    row_int = element[0] + step * OFFSETS[direction][0]
                    col_int = element[1] + step * OFFSETS[direction][1]
                    tmp_lst.append(self.get_tile(row_int, col_int))
                merge_lst = merge(tmp_lst)
                tmp_lst = []
                for step in range(self._width):
                    self.set_tile(element[0] + step * OFFSETS[direction][0], element[1] + step * OFFSETS[direction][1],
                                  merge_lst[step])
            self._grid = [[self.get_tile(each_row, each_col) for each_col in range(self._width)] for each_row in
                          range(self._height)]
            for _row in range(self._height):
                for _col in range(self._width):
                    if old_grid[_row][_col] != self._grid[_row][_col]:
                        flag = False
            if flag == False:
                self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        init_row = random.randrange(0, self._height)
        init_col = random.randrange(0, self._width)
        if random.randint(0, 9) == 9:
            init_value = 4
        else:
            init_value = 2
        while self._grid[init_row][init_col] != 0:
            init_row = random.randrange(0, self._height)
            init_col = random.randrange(0, self._width)
        self.set_tile(init_row, init_col, init_value)

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(3, 4))
