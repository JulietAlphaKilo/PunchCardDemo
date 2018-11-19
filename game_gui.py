from PySide2 import QtCore, QtWidgets, QtGui
import maze
import sys


class MazeGameWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.game_maze = maze.Maze()
        self.layout = QtWidgets.QVBoxLayout()

        self.text = QtWidgets.QLabel(str(self.game_maze))
        self.text.setFont(QtGui.QFont('Consolas', 14))

        self.layout.addWidget(self.text)
        self.setLayout(self.layout)
        # TODO Create event to escape from fullscreen
        # self.showFullScreen()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    with open('retro_style.css', 'r') as stylesheet:
        app.setStyleSheet(stylesheet.read())

    widget = MazeGameWindow()
    widget.show()

    sys.exit(app.exec_())
