from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QBrush, QVector3D
from PySide6.QtCore import QPointF
from algorithms import scanline_filling
from geometry.lightning import interpolate_point_params
from model.bezier import BezierSurface, ControlPoint
from model.lighting import LightingModel, LightSource

class BezierCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.bezier_surf: BezierSurface = None
        self.lighting_model = None
        # Display options
        self.show_polygon: bool = True
        self.show_mesh: bool = True
        self.show_fill: bool = False
        # Parameter for scaling the size of the bezier surface
        self.scale = 50
        self.surf_color = QColor(0, 255, 255)
        self.surf_texture = None

    def initialize(self, control_points: list[list[ControlPoint]], 
                   divisions: int, alpha: float, beta: float, 
                   kd: float, ks: float, m: int, light_source_Z: int):
        self.bezier_surf = BezierSurface(control_points)
        self.bezier_surf.generate_mesh(divisions)
        self.bezier_surf.rotate(alpha, beta)
        light_source = LightSource(radius=5.0, angular_speed=0.5, Z=light_source_Z)
        self.lighting_model = LightingModel(kd, ks, m, light_source)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        try:
            if not painter.isActive():
                return
            painter.setRenderHint(QPainter.Antialiasing)
            # Move origin to the center of the canvas
            painter.translate(self.width() / 2, self.height() / 2)
            painter.scale(1, -1)  # Flip Y axis (in Qt Y grows downwards)

            if self.bezier_surf is None:
                return
            if self.show_fill:
                self.draw_fill(painter)
            if self.show_mesh:
                self.draw_mesh(painter)
            if self.show_polygon:
                self.draw_polygon(painter)
        finally:
            painter.end()

    def draw_polygon(self, painter: QPainter):
        pen = QPen(QColor(0, 0, 0), 2)
        painter.setPen(pen)

        control_points_rot = self.bezier_surf.cpoints_rot()

        # Lines along u direction
        for i in range(4):
            for j in range(3):
                p1 = self.project_point(control_points_rot[i][j])
                p2 = self.project_point(control_points_rot[i][j + 1])
                painter.drawLine(p1, p2)

        # Lines along v direction
        for j in range(4):
            for i in range(3):
                p1 = self.project_point(control_points_rot[i][j])
                p2 = self.project_point(control_points_rot[i + 1][j])
                painter.drawLine(p1, p2)

        # Control points
        painter.setBrush(QBrush(QColor(0, 0, 255)))
        for row in control_points_rot:
            for cp in row:
                p = self.project_point(cp)
                painter.drawEllipse(p, 5, 5)

    def draw_mesh(self, painter: QPainter):
        pen = QPen(QColor(128, 128, 255), 1)
        painter.setPen(pen)

        for triangle in self.bezier_surf.mesh:
            v0, v1, v2 = triangle.vertices
            
            p0 = self.project_point(v0.P_rot)
            p1 = self.project_point(v1.P_rot)
            p2 = self.project_point(v2.P_rot)
            
            painter.drawLine(p0, p1)
            painter.drawLine(p1, p2)
            painter.drawLine(p2, p0)

    def draw_fill(self, painter: QPainter):
        for triangle in self.bezier_surf.mesh:
            v0, v1, v2 = triangle.vertices
            
            p0 = self.project_point(v0.P_rot)
            p1 = self.project_point(v1.P_rot)
            p2 = self.project_point(v2.P_rot)

            polygon = [p0, p1, p2]
            pixels = scanline_filling(polygon)
            ipp = lambda x, y: interpolate_point_params(x, y, p0, p1, p2, v0, v1, v2)
            for (x, y) in pixels:
                N, z = ipp(x, y)
                color = self.lighting_model.compute_lighting(QVector3D(x, y, z), N, self.surf_color)
                painter.setPen(QPen(color))
                painter.drawPoint(x, y)
            
    def update_on_triangulation(self, divisions: int, alpha: float, beta: float):
        if self.bezier_surf is not None:
            self.bezier_surf.generate_mesh(divisions)
            self.bezier_surf.rotate(alpha, beta)
            self.update()

    def update_on_rotation(self, alpha: float, beta: float):
        if self.bezier_surf is not None:
            self.bezier_surf.rotate(alpha, beta)
            self.update()

    def update_on_lighting_model_change(self, kd: float, ks: float, m: int):
        self.lighting_model.kd = kd
        self.lighting_model.ks = ks
        self.lighting_model.m = m
        self.update()

    def update_on_light_source_change(self, light_source_Z: int):
        self.lighting_model.lighting_source.Z = light_source_Z
        self.update()

    # 3D -> 2D projection (orthogonal projection onto XY plane)
    def project_point(self, point: QVector3D) -> QPointF:
        x = point.x() * self.scale
        y = point.y() * self.scale
        return QPointF(x, y)
