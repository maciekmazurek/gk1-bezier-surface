from PySide6.QtGui import QVector3D

class Vertex:
    def __init__(self):
        self.P = QVector3D(0, 0, 0)
        self.Pu = QVector3D(0, 0, 0) # u tangent
        self.Pv = QVector3D(0, 0, 0) # v tangent
        self.N = QVector3D(0, 0, 0)

        # After rotation
        self.P_rot = QVector3D(0, 0, 0)
        self.Pu_rot = QVector3D(0, 0, 0)
        self.Pv_rot = QVector3D(0, 0, 0)
        self.N_rot = QVector3D(0, 0, 0)

        self.u = 0.0
        self.v = 0.0

class Triangle:
    def __init__(self, v0: Vertex, v1: Vertex, v2: Vertex):
        self.vertices = [v0, v1, v2]

class Mesh:
    def __init__(self):
        self.triangles = []

class BezierSurface:
    def __init__(self, control_points: list[list[QVector3D]]):
        self.control_points = control_points
        self.mesh: Mesh = None
        self.alpha = None
        self.beta = None