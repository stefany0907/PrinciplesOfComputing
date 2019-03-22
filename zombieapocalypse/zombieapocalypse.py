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
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
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
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        ##self._obstacle_list = []
        ##obstacle = poc_grid.Grid(self._grid_height, self._grid_width)
        ##obstacle.clear()
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
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
        num = 0
        while num < len(self._zombie_list):
            yield self._zombie_list[num]
            num = num + 1
        #return 0

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list) 
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        num = 0
        while num < len(self._human_list):
            yield self._human_list[num]
            num = num + 1
        #return 0

        
    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        ##print "obstacle_list", self.obstacle_list
        distance_field = [[(self._grid_height * self._grid_width) for dummy_col in range(self._grid_width)] 
                           for dummy_row in range(self._grid_height)]
        visited = poc_grid.Grid(self._grid_height, self._grid_width)         
        for row in range(self._grid_height):
            for col in range(self._grid_width):
                visited.set_empty(row, col)                
        #print visited               
        boundary = poc_queue.Queue()
        if entity_type == "human":
            print "stalk"
            for item in self._human_list:
                boundary.enqueue(item)                 
        elif entity_type == "zombie":
            print "flee"
            for item in self._zombie_list:
                boundary.enqueue(item)         
        else:
            print "none"

        for cell in boundary:             
            visited.set_full(cell[0], cell[1])
            distance_field[cell[0]][cell[1]] = 0
            
        #print "boundary=", boundary
        while boundary.__len__() != 0:            
            current_cell = boundary.dequeue()            
            neighbors = self.four_neighbors(current_cell[0], current_cell[1])            
            
            #neighbors = self.eight_neighbors(cell[0], cell[1])
            for neighbor_cell in neighbors: 
                #print "neighbor_cell", neighbor_cell
                #print "test", self.is_empty(neighbor_cell[0], neighbor_cell[1])
                if not self.is_empty(neighbor_cell[0], neighbor_cell[1]):
                    visited.set_full(neighbor_cell[0], neighbor_cell[1])
                if visited.is_empty(neighbor_cell[0], neighbor_cell[1]): 
                    visited.set_full(neighbor_cell[0], neighbor_cell[1])                    
                    boundary.enqueue(neighbor_cell)
                    distance_field[neighbor_cell[0]][neighbor_cell[1]] = distance_field[current_cell[0]][current_cell[1]] + 1
                #print "visited=", visited
                #print "distance_field=", distance_field
        return distance_field
    
    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """        
        update_human_lst = []
        max_human_lst = []
        
        for human in self.humans():
            print "human=", human
            max_distance = zombie_distance[human[0]][human[1]]
            max_human = (human[0], human[1])  
            print max_distance, max_human
            neighbors = self.eight_neighbors(human[0], human[1])                         
            for neighbor_cell in neighbors:  
#                print "neighbor_cell", neighbor_cell
#                print zombie_distance[neighbor_cell[0]][neighbor_cell[1]]
                if self.is_empty(neighbor_cell[0], neighbor_cell[1]):                	
                    if max_distance < zombie_distance[neighbor_cell[0]][neighbor_cell[1]]:
                        max_distance = zombie_distance[neighbor_cell[0]][neighbor_cell[1]]
                        max_human = (neighbor_cell[0], neighbor_cell[1])
                        max_human_lst = [(neighbor_cell[0], neighbor_cell[1])]                    
                    elif max_distance == zombie_distance[neighbor_cell[0]][neighbor_cell[1]]:
                        max_human_lst.append((neighbor_cell[0], neighbor_cell[1])) 
#            print max_human_lst
#            print type(update_human_lst)
            if len(max_human_lst) != 0:                
                update_human_lst.append(random.choice(max_human_lst))
            else:
                update_human_lst.append(max_human)
                print update_human_lst
        #print "update_human_lst", update_human_lst    
        self._human_list = update_human_lst
        
        
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        update_zombie_lst = []
        min_zombie_lst = []
        
        for zombie in self.zombies():
            min_distance = human_distance[zombie[0]][zombie[1]]
            min_zombie = (zombie[0], zombie[1])
            neighbors = self.four_neighbors(zombie[0], zombie[1])   
            
            for neighbor_cell in neighbors:
                if self.is_empty(neighbor_cell[0], neighbor_cell[1]):
                    if min_distance > human_distance[neighbor_cell[0]][neighbor_cell[1]]:
                        min_distance = human_distance[neighbor_cell[0]][neighbor_cell[1]]
                        min_zombie = (neighbor_cell[0], neighbor_cell[1])
                        min_zombie_lst = [(neighbor_cell[0], neighbor_cell[1])]
                    elif min_distance == human_distance[neighbor_cell[0]][neighbor_cell[1]]:               
                        min_zombie_lst.append((neighbor_cell[0], neighbor_cell[1]))
            if min_distance != 0:
#                print "min_zombie_lst=", min_zombie_lst  
                update_zombie_lst.append(random.choice(min_zombie_lst))
            else:
                update_zombie_lst.append(min_zombie)
#            print "update_zombie_lst", update_zombie_lst
        self._zombie_list = update_zombie_lst       

# Start up gui for simulation - You will need to write some code above
# before this will work without errors
#obj = Zombie(3, 3, [(0, 0), (0, 1), (0, 2), (1, 0)], [(2, 1)], [(1, 1)])
#dist = [[9, 9, 9], [9, 1, 2], [1, 0, 1]]
#obj.move_humans(dist)
#print obj._human_list
poc_zombie_gui.run_gui(Zombie(15, 3))

