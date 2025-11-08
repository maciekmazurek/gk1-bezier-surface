from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QBrush, QVector3D
from PySide6.QtCore import QPointF

from model import BezierSurface


class BezierCanvas(QWidget):
    def __init__(self, parent=None, control_points: list[list[QVector3D]] | None = None):
        super().__init__(parent)
        self._bezier_surf: BezierSurface | None = None

        # Display options
        self._show_polygon: bool = True
        self._show_mesh: bool = True
        self._show_fill: bool = False

        # Skala dla rysowania (piksele na jednostkę)
        self.scale = 50

    def set_control_points(self, control_points: list[list[QVector3D]]):
        """Ustawia punkty kontrolne i tworzy obiekt powierzchni."""
        self._bezier_surf = BezierSurface(control_points)
        self.update()  # wywołuje ponowne malowanie

    # Rysowanie
    def paintEvent(self, event):
        painter = QPainter(self)

        # Ustawienia transformacji
        painter.setRenderHint(QPainter.Antialiasing)
        # Ustawienie początku układu w środku canvasu
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(1, -1)  # Odwrócenie osi Y (w Qt rośnie w dół)

        if self._bezier_surf is None:
            return  # Brak danych do rysowania

        if self._show_polygon:
            self._draw_polygon(painter)
        if self._show_mesh:
            pass  # TODO
        if self._show_fill:
            pass  # TODO

    def _draw_polygon(self, painter: QPainter):
        pen = QPen(QColor(0, 200, 0), 2)
        painter.setPen(pen)

        # Linie w kierunku u
        for i in range(4):
            for j in range(3):
                p1 = self.project_point(self._bezier_surf.control_points[i][j])
                p2 = self.project_point(self._bezier_surf.control_points[i][j + 1])
                painter.drawLine(p1, p2)

        # Linie w kierunku v
        for j in range(4):
            for i in range(3):
                p1 = self.project_point(self._bezier_surf.control_points[i][j])
                p2 = self.project_point(self._bezier_surf.control_points[i + 1][j])
                painter.drawLine(p1, p2)

        # Punkty kontrolne
        painter.setBrush(QBrush(QColor(0, 255, 0)))
        for row in self._bezier_surf.control_points:
            for point in row:
                p = self.project_point(point)
                painter.drawEllipse(p, 5, 5)

    # Projekcja 3D -> 2D (rzut prostopadły na XY)
    def project_point(self, point: QVector3D) -> QPointF:
        x = point.x() * self.scale
        y = point.y() * self.scale
        return QPointF(x, y)

    def project_vertex(self, vertex):  # Zachowane jeśli będzie potrzebne później
        return self.project_point(vertex.P_rot)