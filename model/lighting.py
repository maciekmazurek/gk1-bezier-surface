from PySide6.QtGui import QVector3D, QColor
from geometry.lighting import position_on_circle
import time, math

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
        # Stałe kanały światła (uaktualniane gdy zmienisz kolor światła)
        self._update_light_channels()

    def _update_light_channels(self):
        c = self.light_source.color
        self.Il_r = c.redF()
        self.Il_g = c.greenF()
        self.Il_b = c.blueF()

    def compute_lighting_pixel(self, x: float, y: float, z: float,
                               Nx: float, Ny: float, Nz: float,
                               Io_r: float, Io_g: float, Io_b: float,
                               light_pos: QVector3D) -> int:
        # Normalizacja N
        lenN = math.sqrt(Nx*Nx + Ny*Ny + Nz*Nz)
        if lenN == 0.0:
            return 0xFF000000  # czarny
        invLenN = 1.0 / lenN
        Nx *= invLenN; Ny *= invLenN; Nz *= invLenN

        # Wektor L = light_pos - point (x,y,z)
        Lx = light_pos.x() - x
        Ly = light_pos.y() - y
        Lz = light_pos.z() - z
        lenL = math.sqrt(Lx*Lx + Ly*Ly + Lz*Lz)
        if lenL == 0.0:
            return 0xFF000000
        invLenL = 1.0 / lenL
        Lx *= invLenL; Ly *= invLenL; Lz *= invLenL

        # cos(N,L)
        cos_NL = Nx*Lx + Ny*Ly + Nz*Lz

        if cos_NL > 0.0:
            # R = 2 cos(N,L) N - L
            Rx = 2.0 * cos_NL * Nx - Lx
            Ry = 2.0 * cos_NL * Ny - Ly
            Rz = 2.0 * cos_NL * Nz - Lz
            # Normalizacja R
            lenR = math.sqrt(Rx*Rx + Ry*Ry + Rz*Rz)
            if lenR != 0.0:
                invLenR = 1.0 / lenR
                Rz *= invLenR  # potrzebny tylko Rz
            else:
                Rz = -1.0
            cos_VR = Rz  # V = (0,0,1)
        else:
            cos_NL = 0.0
            cos_VR = -1.0

        # Diffuse
        diffuse_r = self.kd * self.Il_r * Io_r * cos_NL
        diffuse_g = self.kd * self.Il_g * Io_g * cos_NL
        diffuse_b = self.kd * self.Il_b * Io_b * cos_NL

        # Specular
        if cos_VR > 0.0:
            spec = self.ks * (cos_VR ** self.m)
            spec_r = spec * self.Il_r * Io_r
            spec_g = spec * self.Il_g * Io_g
            spec_b = spec * self.Il_b * Io_b
        else:
            spec_r = spec_g = spec_b = 0.0

        r = int(min(diffuse_r + spec_r, 1.0) * 255)
        g = int(min(diffuse_g + spec_g, 1.0) * 255)
        b = int(min(diffuse_b + spec_b, 1.0) * 255)
        return 0xFF000000 | (r << 16) | (g << 8) | b
