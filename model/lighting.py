from PySide6.QtGui import QVector3D, QColor
from geometry.general import position_on_circle
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
