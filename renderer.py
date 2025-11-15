from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QBrush, QVector3D, QImage
from PySide6.QtCore import QPointF, Qt
from algorithms import scanline_filling
from geometry.lighting import interpolate_point_params
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

        self.framebuffer: QImage = None

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
        self._ensure_framebuffer()
        self.framebuffer.fill(Qt.transparent)

        ls = self.lighting_model.light_source
        ls.update_cache()
        light_pos = ls.position_cache

        # Kolor obiektu (stały w tej wersji)
        Io_r = self.surf_color.redF()
        Io_g = self.surf_color.greenF()
        Io_b = self.surf_color.blueF()

        w, h = self.framebuffer.width(), self.framebuffer.height()

        for triangle in self.bezier_surf.mesh:
            v0, v1, v2 = triangle.vertices
            p0 = self.project_point(v0.P_rot)
            p1 = self.project_point(v1.P_rot)
            p2 = self.project_point(v2.P_rot)

            polygon = [p0, p1, p2]
            pixel_spans = scanline_filling(polygon)

            x0f, y0f = p0.x(), p0.y()
            x1f, y1f = p1.x(), p1.y()
            x2f, y2f = p2.x(), p2.y()

            denom = (y1f - y2f) * (x0f - x2f) + (x2f - x1f) * (y0f - y2f)
            if abs(denom) < 1e-12:
                continue

            A0 = (y1f - y2f); B0 = (x2f - x1f); C0 = -A0 * x2f - B0 * y2f
            A1 = (y2f - y0f); B1 = (x0f - x2f); C1 = -A1 * x2f - B1 * y2f
            dw0_dx = A0 / denom
            dw1_dx = A1 / denom

            N0 = v0.N_rot; N1 = v1.N_rot; N2 = v2.N_rot
            DN0 = N0 - N2; DN1 = N1 - N2

            z0 = v0.P_rot.z(); z1 = v1.P_rot.z(); z2 = v2.P_rot.z()
            Dz0 = z0 - z2; Dz1 = z1 - z2

            for (y_scan, x_start, x_end) in pixel_spans:
                y_float = float(y_scan)
                w0 = (A0 * x_start + B0 * y_float + C0) / denom
                w1 = (A1 * x_start + B1 * y_float + C1) / denom

                for x in range(x_start, x_end + 1):
                    # Interpolacja normalnych i z
                    N = N2 + DN0 * w0 + DN1 * w1
                    Nx, Ny, Nz = N.x(), N.y(), N.z()
                    z = z2 + Dz0 * w0 + Dz1 * w1

                    xi = int(x + self.width() / 2)
                    yi = int(self.height() / 2 - y_scan)
                    if 0 <= xi < w and 0 <= yi < h:
                        pixel = self.lighting_model.compute_lighting_pixel(
                            x, y_scan, z, Nx, Ny, Nz,
                            Io_r, Io_g, Io_b, light_pos
                        )
                        self.framebuffer.setPixel(xi, yi, pixel)

                    w0 += dw0_dx
                    w1 += dw1_dx

        painter.save()
        painter.resetTransform()
        painter.drawImage(0, 0, self.framebuffer)
        painter.restore()
            
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
        self.lighting_model.light_source.Z = light_source_Z
        self.update()

    # 3D -> 2D projection (orthogonal projection onto XY plane)
    def project_point(self, point: QVector3D) -> QPointF:
        x = point.x() * self.scale
        y = point.y() * self.scale
        return QPointF(x, y)
    
    # Pomocnicze: alokacja/realokacja bufora po zmianie rozmiaru
    def _ensure_framebuffer(self):
        w, h = self.width(), self.height()
        if self.framebuffer is None or self.framebuffer.width() != w or self.framebuffer.height() != h:
            # ARGB32_Premultiplied — szybkie blendowanie i przezroczystość
            self.framebuffer = QImage(w, h, QImage.Format_ARGB32_Premultiplied)