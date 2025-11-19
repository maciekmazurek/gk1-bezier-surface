from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QBrush, QVector3D, QImage
from PySide6.QtCore import QPointF, Qt
from model.bezier import ControlPoint
from model.lighting import LightingModel, LightSource
from lighting_wrapper import fill_surface_c
from model.animation import Animation
from graphics.bezier import BezierSurfaceGraphics

import config

class Canvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.bezier_surface_graphics = None
        self.lighting_model = None
        self.framebuffer: QImage = None
        self.scale = config.SCALE
        self.animation = Animation(self._on_anim_tick)

    def initialize(self, control_points: list[list[ControlPoint]], 
                   texture: QImage, divisions: int, alpha: float, 
                   beta: float, show_polygon: bool, show_mesh:bool, 
                   show_fill:bool, kd: float, ks: float, m: int, 
                   light_source_Z: int):
        self.bezier_surface_graphics = BezierSurfaceGraphics(control_points,
            texture, show_polygon, show_mesh, show_fill)
        self.bezier_surface_graphics.generate_mesh(divisions)
        self.bezier_surface_graphics.rotate(alpha, beta)
        light_source = LightSource(light_source_Z)
        self.lighting_model = LightingModel(kd, ks, m, light_source)
        self.animation.run()
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

            if self.bezier_surface_graphics is None:
                return
            if self.bezier_surface_graphics.show_fill:
                self.draw_fill(painter)
            if self.bezier_surface_graphics.show_mesh:
                self.draw_mesh(painter)
            if self.bezier_surface_graphics.show_polygon:
                self.draw_polygon(painter)
        finally:
            painter.end()

    def draw_polygon(self, painter: QPainter):
        pen = QPen(QColor(0, 0, 0), 2)
        painter.setPen(pen)

        control_points_rot = self.bezier_surface_graphics.bezier_surface.cpoints_rot()

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

        for triangle in self.bezier_surface_graphics.bezier_surface.mesh:
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

        if not self.animation.paused:
            self.lighting_model.light_source.update_cache(self.animation.get_active_time())

        texture = None
        if self.bezier_surface_graphics.texture_enabled:
            texture = self.bezier_surface_graphics.texture

        fill_surface_c(
            triangles_list=self.bezier_surface_graphics.bezier_surface.mesh,
            kd=self.lighting_model.kd,
            ks=self.lighting_model.ks,
            m=self.lighting_model.m,
            light_pos=self.lighting_model.light_source.position_cache,
            io_color=self.bezier_surface_graphics.color,
            il_color=self.lighting_model.light_source.color,
            framebuffer=self.framebuffer,
            scale=self.scale,
            texture_qimage=texture,
        )

        painter.save()
        painter.resetTransform()
        painter.drawImage(0, 0, self.framebuffer)
        painter.restore()

    def _on_anim_tick(self):
        if self.bezier_surface_graphics.show_fill:
            self.update()

    def update_on_triangulation(self, divisions: int, alpha: float, beta: float):
        if self.bezier_surface_graphics is not None:
            self.bezier_surface_graphics.generate_mesh(divisions)
            self.bezier_surface_graphics.rotate(alpha, beta)
            self.update()

    def update_on_rotation(self, alpha: float, beta: float):
        if self.bezier_surface_graphics is not None:
            self.bezier_surface_graphics.rotate(alpha, beta)
            self.update()

    def update_on_show_params_changed(self, show_polygon: bool, show_mesh: bool, show_fill: bool):
        if self.bezier_surface_graphics is not None:
            self.bezier_surface_graphics.show_polygon = show_polygon
            self.bezier_surface_graphics.show_mesh = show_mesh
            self.bezier_surface_graphics.show_fill = show_fill
            self.update()

    def update_on_lighting_model_changed(self, kd: float, ks: float, m: int):
        self.lighting_model.kd = kd
        self.lighting_model.ks = ks
        self.lighting_model.m = m
        self.update()

    def update_on_light_source_changed(self, light_source_Z: int):
        self.lighting_model.light_source.Z = light_source_Z
        self.update()

    def update_on_light_color_changed(self, new_color: QColor):
        self.lighting_model.light_source.color = new_color
        self.update()

    def update_on_surface_color_changed(self, new_color: QColor):
        self.bezier_surface_graphics.color = new_color
        self.update()

    def update_on_animation_paused_resumed(self):
        if self.animation.paused:
            self.animation.resume()
        else:
            self.animation.pause()
        self.update()

        return self.animation.paused

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
