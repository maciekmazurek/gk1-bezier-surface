from PySide6.QtWidgets import QApplication, QMainWindow, QColorDialog
from ui.mainwindow_ui import Ui_MainWindow
from pathlib import Path

import sys
import utils

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setupSlots()
        control_points_path = str(Path(__file__).resolve().parent / "resources" / "control_points.txt")
        self.render(control_points_path)

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

    def on_lighting_model_changed(self):
        kd = self.kdSlider.value() / 100
        ks = self.ksSlider.value() / 100
        m = self.mSlider.value()
        self.kdValueLabel.setText(str(kd))
        self.ksValueLabel.setText(str(ks))
        self.mValueLabel.setText(str(m))
        self.canvas.update_on_lighting_model_changed(kd, ks, m)

    def on_light_source_changed(self):
        light_source_Z = self.lightSlider.value()
        self.lightValueLabel.setText(str(light_source_Z))
        self.canvas.update_on_light_source_changed(light_source_Z)

    def on_light_color_changed(self):
        new_color = QColorDialog.getColor(self.canvas.lighting_model.light_source.color, self, "Select light color")
        if new_color.isValid():
            self.canvas.update_on_light_color_changed(new_color)

    def on_surface_color_changed(self):
        new_color = QColorDialog.getColor(self.canvas.surf_color, self, "Select surface color")
        if new_color.isValid():
            self.canvas.update_on_surface_color_changed(new_color)

    def on_animation_paused_resumed(self):
        animation_paused = self.canvas.update_on_animation_paused_resumed()
        if animation_paused:
            self.animationButton.setText("Resume animation")
        else:
            self.animationButton.setText("Pause animation")

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
        # lighting parameters change
        self.kdSlider.valueChanged.connect(self.on_lighting_model_changed)
        self.ksSlider.valueChanged.connect(self.on_lighting_model_changed)
        self.mSlider.valueChanged.connect(self.on_lighting_model_changed)
        self.lightSlider.valueChanged.connect(self.on_light_source_changed)
        # Surface color selection
        self.surfaceColorButton.clicked.connect(self.on_surface_color_changed)
        # Light color selection
        self.lightColorButton.clicked.connect(self.on_light_color_changed)
        # Animation pause/resume
        self.animationButton.clicked.connect(self.on_animation_paused_resumed)

    def render(self, control_points_filename: str):
        control_points = utils.load_control_points(control_points_filename)
        divisions = self.triangulationSlider.value()
        alpha = self.alphaSlider.value()
        beta = self.betaSlider.value()
        kd = self.kdSlider.value() / 100
        ks = self.ksSlider.value() / 100
        m = self.mSlider.value()
        light_source_Z = self.lightSlider.value()
        self.canvas.initialize(control_points, divisions, alpha, beta, kd, ks, m, light_source_Z)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
