from PySide6.QtWidgets import QApplication, QMainWindow
from ui.mainwindow_ui import Ui_MainWindow

import sys
import utils

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._load_surface()

    def _load_surface(self):
        control_points = utils.load_control_points("control_points.txt")
        self.canvas.set_control_points(control_points)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
