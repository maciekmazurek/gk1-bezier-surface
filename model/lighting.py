from PySide6.QtGui import QVector3D
from PySide6.QtGui import QColor
from geometry.lighting import cos_between_vectors, position_on_circle

import time

class LightSource:
    def __init__(self, radius: float, angular_speed: float, Z: int):
        self.radius = radius
        self.angular_speed = angular_speed
        self.Z = Z
        self.color = QColor(255, 255, 255)  # White light
        self.start_time = time.time()
        self.position_cache = self.position()

    def elapsed(self) -> float:
        return time.time() - self.start_time

    def position(self) -> QVector3D:
        angle = self.elapsed() * self.angular_speed
        x, y = position_on_circle(self.radius, angle)
        return QVector3D(x, y, self.Z)
    
    def update_cache(self):
        self.position_cache = self.position()

class LightingModel:
    def __init__(self, kd: float, ks: float, m: int, source: LightSource):
        self.kd = kd
        self.ks = ks
        self.m = m
        self.light_source = source
        self.V = QVector3D(0, 0, 1)  # Assuming viewer is along Z axis

    def compute_lighting(self, point: QVector3D, N: QVector3D, object_color: QColor):
        N = N.normalized()
        L = self.compute_L(point)
        R = self.compute_R(N, L)

        light_color_rF = self.light_source.color.redF()
        light_color_gF = self.light_source.color.greenF()
        light_color_bF = self.light_source.color.blueF()
        object_color_rF = object_color.redF()
        object_color_gF = object_color.greenF()
        object_color_bF = object_color.blueF()

        red_diffuse = self.compute_diffuse(light_color_rF, object_color_rF, N, L)
        red_specular = self.compute_specular(light_color_rF, object_color_rF, R)
        red = int(min(red_diffuse + red_specular, 1.0) * 255)

        green_diffuse = self.compute_diffuse(light_color_gF, object_color_gF, N, L)
        green_specular = self.compute_specular(light_color_gF, object_color_gF, R)
        green = int(min(green_diffuse + green_specular, 1.0) * 255)

        blue_diffuse = self.compute_diffuse(light_color_bF, object_color_bF, N, L)
        blue_specular = self.compute_specular(light_color_bF, object_color_bF, R)
        blue = int(min(blue_diffuse + blue_specular, 1.0) * 255)

        return QColor(red, green, blue)

    def compute_diffuse(self, light_color: float, object_color: float, N: QVector3D, L: QVector3D):
        cos_NL = cos_between_vectors(N, L)
        if cos_NL < 0:
            return 0
        return self.kd * light_color * object_color * cos_NL

    def compute_specular(self, light_color: float, object_color: float, R: QVector3D):
        cos_VR = cos_between_vectors(self.V, R)
        if cos_VR < 0:
            return 0
        return self.ks * light_color * object_color * (cos_VR ** self.m)

    def compute_L(self, point: QVector3D) -> QVector3D:
        light_pos = self.light_source.position_cache
        L = light_pos - point
        L.normalize()
        return L
    
    def compute_R(self, N: QVector3D, L: QVector3D) -> QVector3D:
        cos_NL = cos_between_vectors(N, L)
        R = 2 * cos_NL * N - L
        R.normalize()
        return R
