from PySide2 import QtCore, QtWidgets, QtGui
import numpy as np
import math
import maze
import sys


class MazeGameWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.game_maze = maze.Maze()
        self.init_UI()

    def init_UI(self):
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        maze_graphic = MazeGraphic(self.game_maze)
        self.layout.addWidget(maze_graphic)

        button_pane = QtWidgets.QHBoxLayout()
        button_pane = self.init_button_pane(button_pane)
        self.layout.addLayout(button_pane)

    def init_button_pane(self, pane):
        # Buttons along the bottom
        pane.setAlignment(QtCore.Qt.AlignRight)
        side_margin = 20
        height_margin = 10
        pane.setContentsMargins(side_margin, height_margin, side_margin, height_margin)
        quit_b = QtWidgets.QPushButton("QUIT")
        quit_b.clicked.connect(QtCore.QCoreApplication.instance().quit)
        pane.addWidget(quit_b)
        return pane


class MazeGraphic(QtWidgets.QWidget):
    def __init__(self, maze):
        super().__init__()
        self.maze = maze
        self.pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        self.pen.setWidth(2)

    def paintEvent(self, *args, **kwargs):
        painter = QtGui.QPainter(self)
        painter.setPen(self.pen)
        self.draw_maze(painter)

    def draw_maze(self, painter):
        MAX_WIDTH = 600
        top_padding = 20
        cell_size = MAX_WIDTH / math.sqrt(np.size(self.maze.maze_map))
        base_x = (self.width()/2) - (MAX_WIDTH/2)
        base_y = self.y() + top_padding
        maze_h = np.shape(self.maze.maze_map)[0]
        maze_w = np.shape(self.maze.maze_map)[1]

        # Draw the uppermost boundary
        painter.drawLine(base_x + cell_size, base_y, base_x + (cell_size * maze_w), base_y)

        # Iterate through maze data and draw walls as they appear
        for row in range(maze_h):
            uppper_y = base_y + (row * cell_size)
            lower_y = uppper_y + cell_size
            painter.drawLine(base_x, uppper_y, base_x, lower_y)
            for col in range(maze_w):
                left_x = base_x + (col * cell_size)
                right_x = left_x + cell_size
                if self.maze.maze_map[row][col] & self.maze.right == 0:
                    painter.drawLine(right_x, uppper_y, right_x, lower_y)
                if self.maze.maze_map[row][col] & self.maze.down == 0:
                    painter.drawLine(left_x, lower_y, right_x, lower_y)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    with open('retro_style.css', 'r') as stylesheet:
        app.setStyleSheet(stylesheet.read())

    main_window = MazeGameWindow()
    main_window.setGeometry(100, 100, 1500, 1000)
    main_window.show()

    sys.exit(app.exec_())
