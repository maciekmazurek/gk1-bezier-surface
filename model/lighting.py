from PySide6.QtGui import QVector3D
from geometry.general import position_on_circle

import config

class LightSource:
    def __init__(self, Z: int, 
                 radius=config.LIGHT_SOURCE_RADIUS, 
                 angular_speed=config.LIGHT_SOURCE_SPEED, 
                 color=config.DEFAULT_LIGHT_COLOR):
        self.Z = Z
        self.radius = radius
        self.angular_speed = angular_speed
        self.color = color
        self.position_cache = self.position(0)

    def position(self, time) -> QVector3D:
        angle = (time / 1000) * self.angular_speed
        x, y = position_on_circle(self.radius, angle)
        return QVector3D(x, y, self.Z)
    
    def update_cache(self, time):
        self.position_cache = self.position(time)

class LightingModel:
    def __init__(self, kd: float, ks: float, m: int, source: LightSource):
        self.kd = kd
        self.ks = ks
        self.m = m
        self.light_source = source
