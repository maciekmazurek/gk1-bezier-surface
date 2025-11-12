from PySide6.QtWidgets import QApplication, QMainWindow
from ui.mainwindow_ui import Ui_MainWindow

import sys
import utils

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setupSlots()
        self.setupCanvas()

    def on_triangulation_changed(self, value):
        self.triangulationValueLabel.setText(str(value))
        alpha = self.alphaSlider.value()
        beta = self.betaSlider.value()
        self.canvas.update_on_triangulation(value, alpha, beta)

    def on_rotation_changed(self):
        alpha = self.alphaSlider.value()
        beta = self.betaSlider.value()
        self.alphaValueLabel.setText(str(alpha))
        self.betaValueLabel.setText(str(beta))
        self.canvas.update_on_rotation(alpha, beta)

    def on_display_changed(self):
        self.canvas.show_polygon = self.polygonCheckBox.isChecked()
        self.canvas.show_mesh = self.meshCheckBox.isChecked()
        self.canvas.show_fill = self.fillCheckBox.isChecked()
        self.canvas.update()

    def on_lightning_changed(self):
        kd = self.kdSlider.value() / 100
        ks = self.ksSlider.value() / 100
        m = self.mSlider.value()
        light_source_position = self.lightSlider.value()
        self.kdValueLabel.setText(str(kd))
        self.ksValueLabel.setText(str(ks))
        self.mValueLabel.setText(str(m))
        self.lightValueLabel.setText(str(light_source_position))
        self.canvas.update_on_lightning_change(kd, ks, m, light_source_position)
    
    def setupSlots(self):
        # Triangulation changes
        self.triangulationSlider.valueChanged.connect(self.on_triangulation_changed)
        # Rotation parameters change
        self.alphaSlider.valueChanged.connect(self.on_rotation_changed)
        self.betaSlider.valueChanged.connect(self.on_rotation_changed)
        # Display parameters change
        self.polygonCheckBox.stateChanged.connect(self.on_display_changed)
        self.meshCheckBox.stateChanged.connect(self.on_display_changed)
        self.fillCheckBox.stateChanged.connect(self.on_display_changed)
        # Lightning parameters change
        self.kdSlider.valueChanged.connect(self.on_lightning_changed)
        self.ksSlider.valueChanged.connect(self.on_lightning_changed)
        self.mSlider.valueChanged.connect(self.on_lightning_changed)
        self.lightSlider.valueChanged.connect(self.on_lightning_changed)

    def setupCanvas(self):
        control_points = utils.load_control_points("control_points.txt")
        divisions = self.triangulationSlider.value()
        alpha = self.alphaSlider.value()
        beta = self.betaSlider.value()
        self.canvas.initialize(control_points, divisions, alpha, beta)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
