from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QBrush, QVector3D
from PySide6.QtCore import QPointF
from model import BezierSurface, ControlPoint

class BezierCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._bezier_surf: BezierSurface = None
        # Display options
        self.show_polygon: bool = True
        self.show_mesh: bool = True
        self.show_fill: bool = False

        # Skala dla rysowania (piksele na jednostkę)
        self.scale = 50

    def initialize(self, control_points: list[list[ControlPoint]], 
                   divisions: int, alpha: float, beta: float):
        self._bezier_surf = BezierSurface(control_points)
        self._bezier_surf.generate_mesh(divisions)
        self._bezier_surf.rotate(alpha, beta)
        self.update()  # wywołuje ponowne malowanie

    # Rysowanie
    def paintEvent(self, event):
        painter = QPainter(self)
        try:
            if not painter.isActive():
                return
            painter.setRenderHint(QPainter.Antialiasing)
            # Ustawienie początku układu w środku canvasu
            painter.translate(self.width() / 2, self.height() / 2)
            painter.scale(1, -1)  # Odwrócenie osi Y (w Qt Y rośnie w dół)

            if self._bezier_surf is None:
                return  # Brak danych do rysowania

            if self.show_polygon:
                self._draw_polygon(painter)
            if self.show_mesh:
                self._draw_mesh(painter)
            if self.show_fill:
                pass  # TODO
        finally:
            painter.end()

    def _draw_polygon(self, painter: QPainter):
        pen = QPen(QColor(0, 200, 0), 2)
        painter.setPen(pen)

        control_points_rot = self._bezier_surf.cpoints_rot()

        # Linie w kierunku u
        for i in range(4):
            for j in range(3):
                p1 = self.project_point(control_points_rot[i][j])
                p2 = self.project_point(control_points_rot[i][j + 1])
                painter.drawLine(p1, p2)

        # Linie w kierunku v
        for j in range(4):
            for i in range(3):
                p1 = self.project_point(control_points_rot[i][j])
                p2 = self.project_point(control_points_rot[i + 1][j])
                painter.drawLine(p1, p2)

        # Punkty kontrolne
        painter.setBrush(QBrush(QColor(0, 255, 0)))
        for row in control_points_rot:
            for cp in row:
                p = self.project_point(cp)
                painter.drawEllipse(p, 5, 5)

    def _draw_mesh(self, painter: QPainter):
        pen = QPen(QColor(120, 120, 255), 1)
        painter.setPen(pen)

        for triangle in self._bezier_surf.mesh:
            v0, v1, v2 = triangle.vertices
            
            p0 = self.project_point(v0.P_rot)
            p1 = self.project_point(v1.P_rot)
            p2 = self.project_point(v2.P_rot)
            
            painter.drawLine(p0, p1)
            painter.drawLine(p1, p2)
            painter.drawLine(p2, p0)

    def update_on_triangulation(self, divisions: int, alpha: float, beta: float):
        if self._bezier_surf is not None:
            self._bezier_surf.generate_mesh(divisions)
            self._bezier_surf.rotate(alpha, beta)
            self.update()

    def update_on_rotation(self, alpha: float, beta: float):
        if self._bezier_surf is not None:
            self._bezier_surf.rotate(alpha, beta)
            self.update()

    # Projekcja 3D -> 2D (rzut prostopadły na XY)
    def project_point(self, point: QVector3D) -> QPointF:
        x = point.x() * self.scale
        y = point.y() * self.scale
        return QPointF(x, y)
