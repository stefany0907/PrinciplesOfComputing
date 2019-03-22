"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

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

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

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

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        
        if self.get_number(target_row, target_col) != 0: 
            return False
        
            #if (target_row + 1) < self.get_height() and (target_col + 1) < self.get_width(): 
        for dummy_row in range(target_row + 1, self.get_height()):                   
            for dummy_col in range(self.get_width()):
                if self.current_position(dummy_row, dummy_col) != (dummy_row, dummy_col):   
                    return False
                
        for dummy_col in range(target_col + 1, self.get_width()):
            if self.current_position(target_row, dummy_col) != (target_row, dummy_col):                                
                return False
        return True
    
    def down_path(self, row_diff, col_diff):
        """
        by "dru", 0 tile position is adjusted from horizentally next to target tile 
        to vertically next to target tile
        """
        move = ""
        if col_diff > 0:
            move += "dru"
        else:
            move += "dlu"
        move += "lddru" * (row_diff - 1)
        move += "ld"
        return move
    
    def position_tile(self, cur_pos, tar_pos):
        """
        Reposition tile at cur_pos to tar_pos and move the original tile at tar_pos (tile 0)
        will sit left to its original pos (cur_pos)
        """
        
        #assert self.lower_row_invariant(tar_pos[0], tar_pos[1]), "invalid invariant"
        d_row = tar_pos[0] - cur_pos[0]
        d_col = tar_pos[1] - cur_pos[1]
        # move 0 tile to targeting tile's current position
        # print "tar_pos, cur_pos", tar_pos, cur_pos
        # print "d_row, d_col", d_row, d_col
        move = "u" * d_row
        move += "l" * d_col + "r" * (-d_col)
        #print move
        if d_col != 0:
            # horizontal move to target_col
            if cur_pos[0] == 0:
                move += ("drrul" * (d_col - 1)) + ("dllur" * ((-d_col) - 1))
#                print move
            else:
                move += ("urrdl" * (d_col - 1)) + ("ulldr" * ((-d_col) - 1))
            # adjust and then vertical move to target_row
            #print cur_pos
            if cur_pos[0] == 0:
                move += self.down_path(d_row, d_col)
                #print move
            elif d_row == 1:
                if d_col > 0:
                    move += "ur"
                else:
                    move += "ul"
                move += "lddru" * d_row
                move += "ld"
            elif d_row != 0:
                move += self.down_path(d_row, d_col)
            return move
        elif d_col == 0 and d_row == 1:
            move += "ld"
            return move
        else:
            move += "lddru" * (d_row - 1)
            move += "ld"
            return move
        
    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, target_col), "invalid invariant"
        cur_pos = self.current_position(target_row, target_col)
        # print "current_pos", cur_pos
        move = self.position_tile(cur_pos, (target_row, target_col))
        self.update_puzzle(move)
        assert self.lower_row_invariant(target_row, target_col - 1), "invalid invariant"
        return move
        
        #lddrulddru


    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        
        move = "ur"
        move1 = ""
        self.update_puzzle(move)
        #print "self1"
        #print self
        if self.get_number(target_row, 0) != target_row * self.get_width():                    
            cur_pos = self.current_position(target_row, 0)
#            print "col0_cur_pos=", cur_pos
            move1 += self.position_tile(cur_pos, (target_row - 1, 1))
            print "col0_move1", move1
            #zero_pos = (target_row - 1, 1)
            #zero_move = self.position_tile(zero_pos, (target_row - 1, 0))
            move1 += "ruldrdlurdluurddlur"
        move1 += "r" * (self.get_width() - 2)
        self.update_puzzle(move1)
        #print "self2"
        #print self
        assert self.lower_row_invariant(target_row - 1, self.get_width() - 1), "invalid invariant"
        return move + move1

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self.get_number(0, target_col) != 0: 
            return False
        for dummy_row in range(2, self.get_height()):                   
            for dummy_col in range(self.get_width()):
                if self.current_position(dummy_row, dummy_col) != (dummy_row, dummy_col):   
                    return False 
        for dummy_row in range(2):                 
            for dummy_col in range(target_col + 1, self.get_width()):
                if self.current_position(dummy_row, dummy_col) != (dummy_row, dummy_col):                                
                    return False        
        if (1, target_col) != self.current_position(1, target_col):        
            #print self.get_number(1, target_col), self.current_position(1, target_col)
            return False
        return True
    
    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self.get_number(1, target_col) != 0: 
            return False
        for dummy_row in range(2, self.get_height()):                   
            for dummy_col in range(self.get_width()):
                if self.current_position(dummy_row, dummy_col) != (dummy_row, dummy_col):   
                    return False        
        for dummy_row in range(2):            
            for dummy_col in range(target_col + 1, self.get_width()):
                if self.current_position(dummy_row, dummy_col) != (dummy_row, dummy_col):                                
                    return False			             
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row0_invariant(target_col), "invalid invariant"
        move = "ld"
        move1 = ""
        self.update_puzzle(move)
        #print "self1"
        #print self
        if self.get_number(0, target_col) != target_col:                    
            cur_pos = self.current_position(0, target_col)
#            print "row0_cur_pos=", cur_pos
            move1 += self.position_tile(cur_pos, (1, target_col - 1))
            print "row0_move", move1
            #zero_pos = (target_row - 1, 1)
            #zero_move = self.position_tile(zero_pos, (target_row - 1, 0))
            move1 += "urdlurrdluldrruld"
            print move1
        #move += "r" * (self.get_width() - 2)
        self.update_puzzle(move1)
        return move + move1

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row1_invariant(target_col), "invalid invariant"
        cur_pos = self.current_position(1, target_col)
#        print "cur_pos", cur_pos
        move = self.position_tile(cur_pos, (1, target_col))
        move += "ur"
        self.update_puzzle(move)
        
        return move

    ###########################################################
    # Phase 3 methods
    
    def ready_2x2(self):
        """
        check if the upper left 2x2 part of the puzzle
        is solved
        """        
        for row in range(2):
            for col in range(2):
                if self.get_number(row, col) != (row * self.get_width() + col):
                    return False
                
                    
        return True
    
    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        assert self.row1_invariant(1), "invalid invariant"
        move = "ul"
        move1 = ""
        self.update_puzzle(move)
#        print "self1"
#        print self
        if self.ready_2x2():
            return move
        else:
            while self.ready_2x2() != True:                  
                move1 += "rdlu" 
                move2 = "rdlu"
                self.update_puzzle(move2)
#                print "self.ready_2x2()", self.ready_2x2()
#                print "self2", move1
#                print self
            return move + move1           
                
        

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # move 0 to right bottom corner
        move, move1, move2, move3 = "", "", "" , ""
        for row in range(self.get_height()):
            for col in range(self.get_width()):                
                if self.get_number(row, col) == 0:                    
                    zero_grid = (row, col)
        move += "d" * (self.get_height() - zero_grid[0] - 1) + "r" * (self.get_width() - zero_grid[1] - 1)            
        
        self.update_puzzle(move)
        
        for tar_row in range(self.get_height() - 1, 1, -1):
            for tar_col in range(self.get_width() - 1, 0, -1):                
                assert self.lower_row_invariant(tar_row, tar_col)   
                move1 += self.solve_interior_tile(tar_row, tar_col)
                
            move1 += self.solve_col0_tile(tar_row)
#            print "row done"
#            print self        
             
        for dummy_col in range(self.get_width() - 1, 1, -1):            
            move2 += self.solve_row1_tile(dummy_col)
            move2 += self.solve_row0_tile(dummy_col)        
        move3 = self.solve_2x2()        
        return move + move1 + move2 + move3

# Start interactive simulation
poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))
#obj = Puzzle(3, 3, [[4, 1, 6], [5, 7, 3], [2, 0, 8]])

#obj = Puzzle(4, 4, [[1, 6, 2, 3], [5, 10, 4, 7], [8, 9, 0, 11], [12, 13, 14, 15]])
#print obj
#
#move1 = obj.solve_interior_tile(2, 2)
#print obj
#move2 = obj.solve_interior_tile(2, 1)
#print obj
#move3 = obj.solve_col0_tile(2)
#
#print obj
#
#print "==========================================="
#obj1 = Puzzle(4, 4, [[6, 2, 1, 3], [5, 4, 0, 7], [8, 9, 10, 11], [12, 13, 14, 15]])
#print obj1
#print obj1.row1_invariant(2)
#obj1.solve_row1_tile(2)
#print "solve row1"
#print obj1
#obj1.solve_row0_tile(2)
#print obj1
#print obj1.ready_2x2()
#obj1.solve_2x2()
#print obj1
#
#print "==========================================="
#obj2 = Puzzle(4, 4, [[2, 6, 1, 3], [5, 4, 0, 7], [8, 9, 15, 11], [12, 13, 14, 10]])
#print obj2
#obj2.solve_puzzle()
#print obj2
