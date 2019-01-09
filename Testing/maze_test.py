import unittest
import numpy as np
import maze

class TestingMazeMethods(unittest.TestCase):

    def setUp(self):
        """
        Instantiates a maze.Maze object
        :return:
        """
        self.test_maze = maze.Maze()

    def test_default_constructor(self):
        """
        Tests that the __init__ function sets the expected default values when not passing any arguments.
        :return:
        """
        default_starting_pos = (0,0)
        self.assertEqual(self.test_maze.start_row, default_starting_pos[0], "Start point in row %d, should be %d" % (self.test_maze.start_row, default_starting_pos[0]))
        self.assertEqual(self.test_maze.start_col, default_starting_pos[1], "Start point is in column %d, should be %d" % (self.test_maze.start_row, default_starting_pos[0]))

    def test_maze_values_valid(self):
        """
        Tests whether all values in the maze are of type int, and there are no NaN values.
        :return:
        """
        self.assertTrue(np.issubdtype(self.test_maze.maze_map.dtype, np.signedinteger))
        for row in self.test_maze.maze_map:
            for cell in row:
                self.assertIsNotNone(cell, "None object found")
                self.assertFalse(np.isnan(cell))

    def test_maze_fully_populated(self):
        """
        Tests that every square in the maze haze been visited and populated in the constructor.
        :return:
        """
        for row in self.test_maze.maze_map:
            for cell in row:
                self.assertNotEqual(cell, 0, "Maze path not fully populated.")

    def test_valid_end_point(self):
        """
        Tests that the start and end points are not in the same cell.
        :return:
        """
        self.assertNotEqual((self.test_maze.start_row, self.test_maze.start_col), (self.test_maze.end_row, self.test_maze.end_col), "Maze path cannot start and end on the same cell.")

if __name__ == '__main__':
    unittest.unittest_main()
