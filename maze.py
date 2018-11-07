import random
import numpy as np
import queue


class Maze:

    def __init__(self, side_length=5, start_row=0, start_col=0):
        self.start_row = start_row
        self.start_col = start_col
        # Initialise constants to represent each direction
        self.up, self.down, self.left, self.right = 1, 2, 4, 8
        self.opposite_directions = {self.up: self.down, self.down: self.up, self.left: self.right, self.right: self.left}
        self.row_move = {self.up: -1, self.down: 1, self.left: 0, self.right: 0}
        self.col_move = {self.up: 0, self.down: 0, self.left: -1, self.right: 1}
        # Initialise randomly generated path through the maze
        self.maze_map = self.generate_path(np.zeros((side_length, side_length), dtype=int), self.start_row, self.start_col)
        self.end_row, self.end_col = self.find_finish_cell()

    def generate_path(self, map, current_row, current_col):
        """
        Randomly generates a square maze using a Recursive Backtracking algorithm. Returns the maze as an ndarray.
        :param map: current layout of the map as a numpy array.
        :param current_row: Row index for first cell in the maze (default is 0)
        :param current_col: Column index for first cell in the maze(default is 0)
        :return maze: maze as a 2D ndarray. The value of each datapoint corresponds to what paths are possible in that cell
        relative to the starting point. To create a new maze, this should be a zero matrix).
        """
        # Randomise directions order to remove bias when plotting a route.
        directions = [self.up, self.down, self.left, self.right]
        random.shuffle(directions)

        # Use Recursive Backtracking to populate the maze:
        # 1. For each cell in the maze, iterate through the list of directions, until an unvisited neighbouring cell is
        #    found.
        # 2. Update the value in the current cell with the value for that direction.
        # 3. Do recursive backtracking on that neighbour.
        # 4. Stop when all four directions have been checked.
        for direction in directions:
            new_row = current_row + self.row_move[direction]
            new_col = current_col + self.col_move[direction]
            if 0 <= new_row < np.shape(map)[0] and 0 <= new_col < np.shape(map)[1] and map[new_row][new_col] == 0:
                map[current_row][current_col] |= direction
                map[new_row][new_col] |= self.opposite_directions[direction]
                map = self.generate_path(map, new_row, new_col)

        return map

    def find_finish_cell(self):
        """
        Finds the row and column indices for the end of the longest path in the maze using a breadth-first search.
        :return : Row and column indices for the final cell visited in the search.
        """
        # Initialise a queue to maintain the order that each cell of the maze is to be checked. Initialise a matirx to
        # keep track of which cells have already been visited, and variables to keep track of indices, starting from the
        # predefined starting point.
        to_check = queue.Queue()
        current_row = self.start_row
        current_col = self.start_col
        visited = np.full((np.shape(self.maze_map)[0], np.shape(self.maze_map)[1]), False, dtype=bool)
        to_check.put((current_row, current_col))
        directions = [self.up, self.down, self.left, self.right]

        # Breadth-first search algorithm is used to find the longest path:
        # 1. While there are still cells to be checked:
        #   1.1 Get the next cell from the queue
        #   1.2 For each neighbouring cell, add it to the queue if it's accessible and not already visited.
        # 2. The last cell visited will be at the end of the longest path. Return its row and column indices.
        while not to_check.empty():
            current_cell = to_check.get()
            current_row = current_cell[0]
            current_col = current_cell[1]
            visited[current_row][current_col] = True

            for direction in directions:
                if self.maze_map[current_row][current_col] & direction != 0 and not visited[current_row + self.row_move[direction]][current_col + self.col_move[direction]]:
                    to_check.put((current_row + self.row_move[direction], current_col + self.col_move[direction]))
        return current_row, current_col

    def traverse(self, user_directions):
        current_row = self.start_row
        current_col = self.start_col
        encode_directions = {'up': self.up, 'down': self.down, 'left': self.left, 'right': self.right}
        for step in user_directions:
            step = step.lower()
            try:
                direction = encode_directions[step]
            except KeyError:
                print('\"%s\" not a valid direction - should be either \"up\", \"down\", \"left\", or \"right\"' % step)
                return False

            poss_row = current_row + self.row_move[direction]
            poss_col = current_col + self.col_move[direction]
            if self.maze_map[current_row][current_col] & direction == 0:
                print('Wrong turn at [%d, %d], direction %s' % (current_row, current_col, step))
                return False
            else:
                current_row = poss_row
                current_col = poss_col

        # Once at the end of the user inputted directions, return True if they have reached the finish point.
        if current_row == self.end_row and current_col == self.end_col:
            return True
        else:
            return False

    def __str__(self):
        top_edge = "+   +"
        for column in range(np.shape(self.maze_map)[0] - 1):
            top_edge += "---+"

        body = top_edge + "\n"
        for row in range(np.shape(self.maze_map)[0]):
            row_string = "|"
            bound_string = "+"
            for col in range(np.shape(self.maze_map)[1]):
                # If the current cell has a right turn, or the right-hand neighbour (if there is one) has a left turn,
                # remove the right-hand wall.
                if self.maze_map[row][col] & self.right != 0:
                    row_string += "    "
                else:
                    if col + 1 < np.shape(self.maze_map)[1] and self.maze_map[row][col+1] & self.left != 0:
                        row_string += "    "
                    else:
                        row_string += "   |"

                # If the current cell has a downward turn, or the cell below (if there is one) has an upward turn, then
                # remove the lower wall.
                if self.maze_map[row][col] & self.down != 0:
                    bound_string += "   +"
                else:
                    if row + 1 > np.shape(self.maze_map)[0] and self.maze_map[row+1][col] & self.up != 0:
                        bound_string += "   +"
                    else:
                        bound_string += "---+"
            row_string += "\n"
            bound_string += "\n"
            body += row_string + bound_string

        return body